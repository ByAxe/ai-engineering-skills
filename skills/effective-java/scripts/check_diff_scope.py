#!/usr/bin/env python3
"""Inspect a Git diff for scope, generated-file, and mixed-risk candidates.

Default mode is advisory and returns zero. Use --strict to return one when a
high-severity scope candidate is present. The script never changes the repo.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
MAX_UNTRACKED_FILE_BYTES = 1_000_000
MAX_UNTRACKED_TOTAL_BYTES = 5_000_000

GENERATED_SEGMENTS = {
    "target",
    "build",
    "out",
    "dist",
    "generated",
    "generated-sources",
    "generated-test-sources",
    ".quarkus",
}
BUILD_FILES = {
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "gradle.properties",
    "libs.versions.toml",
    "mvnw",
    "mvnw.cmd",
    "gradlew",
    "gradlew.bat",
}
API_SCHEMA_SUFFIXES = {
    ".proto",
    ".avsc",
    ".graphql",
    ".graphqls",
    ".xsd",
    ".wsdl",
}
SECRET_LINE = re.compile(
    r"(?i)(?:password|passwd|secret|api[_-]?key|access[_-]?key|private[_-]?key|client[_-]?secret|bearer|authorization)\s*[:=]\s*[^\s${][^\s]*"
)
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
PUBLIC_API = re.compile(
    r"^\+\s*public\s+(?:(?:sealed|non-sealed|final|abstract|static)\s+)*(?:class|interface|record|enum|@interface|[\w.$<>?, \[\]]+\s+[A-Za-z_$][\w$]*\s*\()"
)


@dataclass(frozen=True)
class Change:
    status: str
    path: str
    old_path: str | None = None
    added: int | None = None
    deleted: int | None = None
    untracked: bool = False


@dataclass(frozen=True)
class Candidate:
    severity: str
    code: str
    message: str
    paths: tuple[str, ...]
    next_step: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="path inside a Git repository")
    parser.add_argument(
        "--base",
        help="base commit/ref (default: HEAD; uses empty tree for an unborn repository)",
    )
    parser.add_argument(
        "--format", choices=("markdown", "json"), default="markdown"
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument(
        "--no-untracked", action="store_true", help="do not include untracked files"
    )
    parser.add_argument("--max-files", type=int, default=40)
    parser.add_argument("--large-change-lines", type=int, default=500)
    return parser.parse_args()


def run_git(repo: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def repository_root(path: Path) -> Path:
    result = run_git(path, ["rev-parse", "--show-toplevel"])
    return Path(result.stdout.strip()).resolve()


def resolve_base(repo: Path, explicit: str | None) -> str:
    if explicit:
        run_git(repo, ["rev-parse", "--verify", f"{explicit}^{{commit}}"])
        return explicit
    result = run_git(repo, ["rev-parse", "--verify", "HEAD"], check=False)
    return "HEAD" if result.returncode == 0 else EMPTY_TREE


def parse_name_status(text: str) -> list[Change]:
    changes: list[Change] = []
    for line in text.splitlines():
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            changes.append(Change(status=status, old_path=parts[1], path=parts[2]))
        elif len(parts) >= 2:
            changes.append(Change(status=status, path=parts[1]))
    return changes


def parse_numstat(text: str) -> dict[str, tuple[int | None, int | None]]:
    result: dict[str, tuple[int | None, int | None]] = {}
    for line in text.splitlines():
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added_text, deleted_text = parts[0], parts[1]
        path = parts[-1]
        added = int(added_text) if added_text.isdigit() else None
        deleted = int(deleted_text) if deleted_text.isdigit() else None
        result[path] = (added, deleted)
    return result


def untracked_files(repo: Path) -> list[str]:
    result = run_git(
        repo, ["ls-files", "--others", "--exclude-standard", "-z"], check=False
    )
    return [value for value in result.stdout.split("\0") if value]


def with_stats(changes: list[Change], stats: dict[str, tuple[int | None, int | None]]) -> list[Change]:
    result: list[Change] = []
    for change in changes:
        added, deleted = stats.get(change.path, (None, None))
        result.append(
            Change(
                status=change.status,
                path=change.path,
                old_path=change.old_path,
                added=added,
                deleted=deleted,
                untracked=change.untracked,
            )
        )
    return result


def parts(path: str) -> set[str]:
    return {part.lower() for part in PurePosixPath(path).parts}


def is_generated(path: str) -> bool:
    path_parts = parts(path)
    if path_parts & GENERATED_SEGMENTS:
        return True
    lowered = path.lower()
    return "/generated/" in f"/{lowered}/" or lowered.endswith(".generated.java")


def is_test(path: str) -> bool:
    p = parts(path)
    return "test" in p or "tests" in p or path.endswith("Test.java") or path.endswith("IT.java")


def is_migration(path: str) -> bool:
    lowered = path.lower()
    suffix = PurePosixPath(path).suffix.lower()
    return suffix == ".sql" and any(
        token in lowered for token in ("migration", "migrations", "flyway", "liquibase", "db/")
    )


def is_api_schema(path: str) -> bool:
    p = PurePosixPath(path)
    lowered = path.lower()
    return p.suffix.lower() in API_SCHEMA_SUFFIXES or any(
        token in lowered for token in ("openapi", "asyncapi", "swagger")
    )


def is_build_file(path: str) -> bool:
    p = PurePosixPath(path)
    return p.name in BUILD_FILES or ".mvn/" in path or "gradle/wrapper/" in path


def is_java_source(path: str) -> bool:
    return path.endswith(".java") and not is_test(path)


def is_config(path: str) -> bool:
    p = PurePosixPath(path)
    lowered = path.lower()
    return p.suffix.lower() in {".properties", ".yml", ".yaml", ".xml"} and any(
        token in lowered
        for token in ("application", "config", "logback", "log4j", "persistence", "beans")
    )


def paths_matching(changes: Iterable[Change], predicate) -> list[str]:
    return sorted(change.path for change in changes if predicate(change.path))


def added_diff(repo: Path, base: str) -> str:
    result = run_git(repo, ["diff", "--unified=0", "--no-color", base, "--"], check=False)
    return result.stdout


def untracked_text_as_diff(repo: Path, paths: Iterable[str]) -> str:
    """Render bounded UTF-8 untracked files as added lines for content checks.

    Git's normal diff excludes untracked files. Listing them without scanning
    their content would miss exactly the new source/config files where leaked
    credentials or debug output often appear. Symlinks, binary data, oversized
    files, and paths that resolve outside the repository are skipped.
    """
    sections: list[str] = []
    total_bytes = 0
    resolved_repo = repo.resolve()
    for relative in paths:
        path = repo / relative
        try:
            if path.is_symlink() or not path.is_file():
                continue
            resolved = path.resolve()
            if resolved != resolved_repo and resolved_repo not in resolved.parents:
                continue
            size = path.stat().st_size
            if size > MAX_UNTRACKED_FILE_BYTES:
                continue
            if total_bytes + size > MAX_UNTRACKED_TOTAL_BYTES:
                break
            raw = path.read_bytes()
        except OSError:
            continue
        if b"\0" in raw:
            continue
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        total_bytes += len(raw)
        sections.extend(
            [
                f"diff --git a/{relative} b/{relative}",
                "new file mode 100644",
                "--- /dev/null",
                f"+++ b/{relative}",
                *[f"+{line}" for line in content.splitlines()],
            ]
        )
    return "\n".join(sections) + ("\n" if sections else "")


def candidate(
    severity: str, code: str, message: str, paths_: Iterable[str], next_step: str
) -> Candidate:
    return Candidate(severity, code, message, tuple(sorted(set(paths_))), next_step)


def analyze(
    repo: Path,
    changes: list[Change],
    diff: str,
    max_files: int,
    large_change_lines: int,
) -> list[Candidate]:
    candidates: list[Candidate] = []
    all_paths = [change.path for change in changes]
    generated = paths_matching(changes, is_generated)
    build = paths_matching(changes, is_build_file)
    sources = paths_matching(changes, is_java_source)
    tests = paths_matching(changes, is_test)
    migrations = paths_matching(changes, is_migration)
    schemas = paths_matching(changes, is_api_schema)
    configs = paths_matching(changes, is_config)

    if generated:
        candidates.append(
            candidate(
                "high",
                "DIFF-GENERATED",
                "Generated/build output is changed",
                generated,
                "Confirm repository policy and edit/regenerate from the source of truth instead of patching output.",
            )
        )
    if len(changes) > max_files:
        candidates.append(
            candidate(
                "medium",
                "DIFF-MASS-SCOPE",
                f"Diff touches {len(changes)} files (threshold {max_files})",
                all_paths[: min(len(all_paths), 20)],
                "Trace every file to the requirement; split formatting, moves, upgrades, and behavior into independent changes.",
            )
        )
    large = [
        change.path
        for change in changes
        if change.added is not None
        and change.deleted is not None
        and change.added + change.deleted >= large_change_lines
    ]
    if large:
        candidates.append(
            candidate(
                "medium",
                "DIFF-LARGE-FILE",
                f"One or more files change at least {large_change_lines} lines",
                large,
                "Inspect for generated output, formatter churn, or mixed mechanical and semantic edits.",
            )
        )
    deleted_tests = [
        change.path
        for change in changes
        if is_test(change.path) and change.status.startswith("D")
    ]
    if deleted_tests:
        candidates.append(
            candidate(
                "high",
                "DIFF-TEST-DELETION",
                "Tests are deleted",
                deleted_tests,
                "Prove the contract is obsolete or replaced; do not remove regression coverage just to make a gate pass.",
            )
        )
    if build and sources:
        candidates.append(
            candidate(
                "medium",
                "DIFF-BUILD-AND-CODE",
                "Build/dependency files and production Java change together",
                build + sources[:10],
                "Verify the build change is strictly required and not a drive-by upgrade; compile immediately and consider a separate change.",
            )
        )
    if migrations and sources:
        candidates.append(
            candidate(
                "medium",
                "DIFF-SCHEMA-AND-CODE",
                "Database migrations and application code change together",
                migrations + sources[:10],
                "Check expand/migrate/contract compatibility, deployment order, rollback/forward-fix, and old/new application coexistence.",
            )
        )
    if schemas and sources:
        candidates.append(
            candidate(
                "medium",
                "DIFF-CONTRACT-AND-CODE",
                "API/message schema and implementation change together",
                schemas + sources[:10],
                "Review generated artifacts and backward/forward compatibility; add a consumer/contract test.",
            )
        )
    if configs and sources:
        candidates.append(
            candidate(
                "low",
                "DIFF-CONFIG-AND-CODE",
                "Configuration and production code change together",
                configs + sources[:10],
                "Check defaults, aliases, build-time/runtime phase, profile behavior, secrets, and rollout order.",
            )
        )
    if sources and not tests:
        candidates.append(
            candidate(
                "low",
                "DIFF-NO-TEST-CHANGE",
                "Production Java changes without test-file changes",
                sources[:20],
                "Existing tests may be sufficient; identify the exact test that proves changed and preserved behavior.",
            )
        )

    current_path = ""
    public_paths: set[str] = set()
    secret_paths: set[str] = set()
    debug_paths: set[str] = set()
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current_path = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if PUBLIC_API.search(line):
            public_paths.add(current_path or "(unknown)")
        if SECRET_LINE.search(line) or PRIVATE_KEY.search(line):
            secret_paths.add(current_path or "(unknown)")
        if re.search(r"\b(?:System\.(?:out|err)\.|printStackTrace\s*\()", line):
            debug_paths.add(current_path or "(unknown)")
    if public_paths:
        candidates.append(
            candidate(
                "medium",
                "DIFF-PUBLIC-API",
                "Added lines appear to change public Java API",
                public_paths,
                "Assess source/binary/behavioral/serialization compatibility and compile affected consumers.",
            )
        )
    if secret_paths:
        candidates.append(
            candidate(
                "critical",
                "DIFF-POSSIBLE-SECRET",
                "Possible credential/private-key material appears in added lines",
                secret_paths,
                "Stop, inspect without copying the value, remove it from the full Git history as needed, and rotate any exposed credential.",
            )
        )
    if debug_paths:
        candidates.append(
            candidate(
                "medium",
                "DIFF-DEBUG-OUTPUT",
                "Direct process/debug output is added",
                debug_paths,
                "Use repository logging with redaction/correlation or remove temporary output.",
            )
        )

    renamed_packages = [
        change.path
        for change in changes
        if change.status.startswith("R")
        and change.old_path
        and PurePosixPath(change.old_path).parent != PurePosixPath(change.path).parent
    ]
    if renamed_packages and sources:
        candidates.append(
            candidate(
                "low",
                "DIFF-PACKAGE-MOVE",
                "Java files move across directories/packages",
                renamed_packages,
                "Keep mechanical moves separate from semantic edits and compile all dependents/reflection/config references.",
            )
        )
    return sorted(
        candidates,
        key=lambda item: (-SEVERITY_ORDER[item.severity], item.code),
    )


def markdown(repo: Path, base: str, changes: list[Change], candidates: list[Candidate]) -> str:
    total_add = sum(change.added or 0 for change in changes)
    total_del = sum(change.deleted or 0 for change in changes)
    lines = [
        "# Diff Scope Review",
        "",
        "> Findings are review candidates. Inspect intent and repository policy before changing the patch.",
        "",
        f"- **Repository:** `{repo}`",
        f"- **Base:** `{base}`",
        f"- **Changed/untracked files:** {len(changes)}",
        f"- **Tracked line delta:** +{total_add} / -{total_del}",
        f"- **Candidates:** {len(candidates)}",
        "",
        "## Files",
        "",
        "| Status | Added | Deleted | Path |",
        "|---|---:|---:|---|",
    ]
    for change in changes:
        status = "??" if change.untracked else change.status
        old = f" (from `{change.old_path}`)" if change.old_path else ""
        lines.append(
            f"| {status} | {change.added if change.added is not None else '-'} | "
            f"{change.deleted if change.deleted is not None else '-'} | `{change.path}`{old} |"
        )
    if not changes:
        lines.append("| - | - | - | no changes detected |")
    lines.extend(["", "## Candidates", ""])
    if not candidates:
        lines.append("No scope candidates detected. This does not prove semantic correctness.")
    for item in candidates:
        lines.extend(
            [
                f"### {item.code} — {item.message}",
                "",
                f"- **Severity:** {item.severity}",
                f"- **Paths:** {', '.join(f'`{p}`' for p in item.paths) or 'n/a'}",
                f"- **Next step:** {item.next_step}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def json_output(repo: Path, base: str, changes: list[Change], candidates: list[Candidate]) -> str:
    return json.dumps(
        {
            "schema_version": "1.0.0",
            "repository": str(repo),
            "base": base,
            "advisory": True,
            "changes": [asdict(item) for item in changes],
            "candidates": [asdict(item) for item in candidates],
        },
        indent=2,
        sort_keys=True,
    ) + "\n"


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        repo = repository_root(root)
        base = resolve_base(repo, args.base)
    except (subprocess.CalledProcessError, OSError) as exc:
        detail = exc.stderr.strip() if isinstance(exc, subprocess.CalledProcessError) else str(exc)
        print(f"error: not a usable Git repository: {detail}", file=sys.stderr)
        return 2

    name_status = run_git(repo, ["diff", "--name-status", "--find-renames", base, "--"])
    numstat = run_git(repo, ["diff", "--numstat", "--find-renames", base, "--"])
    changes = with_stats(parse_name_status(name_status.stdout), parse_numstat(numstat.stdout))
    untracked: list[str] = []
    if not args.no_untracked:
        untracked = untracked_files(repo)
        changes.extend(
            Change(status="??", path=path, untracked=True) for path in untracked
        )
    changes.sort(key=lambda item: item.path)
    diff = added_diff(repo, base) + untracked_text_as_diff(repo, untracked)
    candidates = analyze(repo, changes, diff, args.max_files, args.large_change_lines)
    rendered = (
        json_output(repo, base, changes, candidates)
        if args.format == "json"
        else markdown(repo, base, changes, candidates)
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    if args.strict and any(SEVERITY_ORDER[item.severity] >= SEVERITY_ORDER["high"] for item in candidates):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
