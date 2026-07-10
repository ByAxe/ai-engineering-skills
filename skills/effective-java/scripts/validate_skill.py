#!/usr/bin/env python3
"""Validate this Effective Java skill bundle with no third-party dependencies."""

from __future__ import annotations

import argparse
import hashlib
import ast
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
}
REQUIRED_BUNDLE_PATHS = {
    "SKILL.md",
    "BUNDLE-MANIFEST.txt",
    "VALIDATION.md",
    "README.md",
    "tile.json",
    "agents/openai.yaml",
    "references/00-reference-router.md",
    "references/agent-failure-modes.md",
    "references/source-index.md",
    "assets/assessment-template.md",
    "assets/refactor-plan-template.md",
    "assets/implementation-report-template.md",
    "scripts/profile_java_project.py",
    "scripts/scan_java_risks.py",
    "scripts/check_diff_scope.py",
    "scripts/build_manifest.py",
    "scripts/run_quality_gates.sh",
    "evals/evals.json",
    "evals/instructions.json",
}
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_PATH = re.compile(
    r"(?<![A-Za-z0-9_./-])((?:references|assets|scripts|schemas|evals|docs|migration|examples)/[A-Za-z0-9_./-]+)"
)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    message: str
    path: str | None = None


class Validation:
    def __init__(self) -> None:
        self.issues: list[Issue] = []

    def error(self, code: str, message: str, path: str | None = None) -> None:
        self.issues.append(Issue("error", code, message, path))

    def warning(self, code: str, message: str, path: str | None = None) -> None:
        self.issues.append(Issue("warning", code, message, path))

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.level == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.level == "warning"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="skill directory")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    parser.add_argument(
        "--strict-warnings", action="store_true", help="fail when warnings exist"
    )
    return parser.parse_args()


def unquote(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value[0] in {'"', "'"}:
        try:
            parsed = ast.literal_eval(value)
            return str(parsed)
        except (ValueError, SyntaxError):
            return value.strip("\"'")
    if value in {"true", "false"}:
        return value
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter closing delimiter not found")
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, Any] = {}
    lines = raw.splitlines()
    i = 0
    current_mapping: dict[str, str] | None = None
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            if ":" not in line:
                raise ValueError(f"invalid frontmatter line: {line}")
            key, raw_value = line.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            current_mapping = None
            if value in {"|", ">", "|-", ">-", "|+", ">+"}:
                block: list[str] = []
                while i < len(lines):
                    next_line = lines[i]
                    next_indent = len(next_line) - len(next_line.lstrip(" "))
                    if next_line.strip() and next_indent == 0:
                        break
                    i += 1
                    block.append(next_line[2:] if next_line.startswith("  ") else next_line.lstrip())
                data[key] = ("\n" if value.startswith("|") else " ").join(block).strip()
            elif value == "":
                mapping: dict[str, str] = {}
                data[key] = mapping
                current_mapping = mapping
            else:
                data[key] = unquote(value)
        else:
            if current_mapping is None or ":" not in line:
                raise ValueError(f"unsupported nested frontmatter line: {line}")
            key, value = line.strip().split(":", 1)
            current_mapping[key.strip()] = unquote(value)
    return data, body


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def validate_frontmatter(root: Path, result: Validation) -> dict[str, Any] | None:
    path = root / "SKILL.md"
    if not path.is_file():
        result.error("SKILL-MISSING", "SKILL.md is missing", "SKILL.md")
        return None
    text = path.read_text(encoding="utf-8")
    try:
        data, body = parse_frontmatter(text)
    except ValueError as exc:
        result.error("SKILL-FRONTMATTER", str(exc), "SKILL.md")
        return None
    unexpected = sorted(set(data) - ALLOWED_FRONTMATTER_KEYS)
    if unexpected:
        result.error(
            "SKILL-KEYS",
            "Unexpected frontmatter keys for this repository validator: " + ", ".join(unexpected),
            "SKILL.md",
    "BUNDLE-MANIFEST.txt",
    "VALIDATION.md",
        )
    name = data.get("name")
    if not isinstance(name, str) or not SKILL_NAME.fullmatch(name):
        result.error("SKILL-NAME", "name must be lowercase hyphen-case", "SKILL.md")
    elif len(name) > 64:
        result.error("SKILL-NAME-LENGTH", "name exceeds 64 characters", "SKILL.md")
    elif root.name != name:
        result.warning(
            "SKILL-DIRECTORY",
            f"directory name '{root.name}' differs from skill name '{name}'",
            "SKILL.md",
    "BUNDLE-MANIFEST.txt",
    "VALIDATION.md",
        )
    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        result.error("SKILL-DESCRIPTION", "description is required", "SKILL.md")
    elif len(description.strip()) > 1024:
        result.error("SKILL-DESCRIPTION-LENGTH", "description exceeds 1024 characters", "SKILL.md")
    elif "<" in description or ">" in description:
        result.error("SKILL-DESCRIPTION-ANGLE", "description contains angle brackets", "SKILL.md")
    else:
        trigger_tokens = ("java", "quarkus", "use for", "not for")
        if not all(token in description.lower() for token in trigger_tokens):
            result.warning(
                "SKILL-ACTIVATION",
                "description may not fully state Java/Quarkus positive and negative activation boundaries",
                "SKILL.md",
    "BUNDLE-MANIFEST.txt",
    "VALIDATION.md",
            )
    metadata = data.get("metadata")
    if metadata is not None:
        if not isinstance(metadata, dict):
            result.error("SKILL-METADATA", "metadata must be a string-to-string mapping", "SKILL.md")
        else:
            for key, value in metadata.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    result.error(
                        "SKILL-METADATA-TYPE",
                        "metadata keys and values must be strings",
                        "SKILL.md",
    "BUNDLE-MANIFEST.txt",
    "VALIDATION.md",
                    )
    line_count = len(text.splitlines())
    if line_count > 500:
        result.error(
            "SKILL-LENGTH",
            f"SKILL.md has {line_count} lines; keep it under 500 and move details to references",
            "SKILL.md",
    "BUNDLE-MANIFEST.txt",
    "VALIDATION.md",
        )
    token_estimate = len(re.findall(r"\w+|[^\w\s]", text))
    if token_estimate > 5000:
        result.warning(
            "SKILL-TOKENS",
            f"rough token estimate {token_estimate} exceeds the recommended 5000",
            "SKILL.md",
    "BUNDLE-MANIFEST.txt",
    "VALIDATION.md",
        )
    if not re.search(r"(?m)^#\s+", body):
        result.error("SKILL-BODY", "SKILL.md body needs a level-one heading", "SKILL.md")
    return data


def validate_required(root: Path, result: Validation) -> None:
    for item in sorted(REQUIRED_BUNDLE_PATHS):
        if not (root / item).is_file():
            result.error("BUNDLE-REQUIRED", f"required bundle file is missing: {item}", item)


def validate_tile(root: Path, result: Validation, skill_name: str | None) -> None:
    path = root / "tile.json"
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.error("TILE-JSON", f"invalid JSON: {exc}", "tile.json")
        return
    name = data.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9._-]+/[a-z0-9._-]+", name):
        result.error("TILE-NAME", "tile name must be workspace/name", "tile.json")
    elif skill_name and not name.endswith(f"/{skill_name}"):
        result.warning("TILE-NAME-MISMATCH", "tile name does not end with skill name", "tile.json")
    version = data.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        result.error("TILE-VERSION", "tile version must be semantic versioning", "tile.json")
    summary = data.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        result.error("TILE-SUMMARY", "tile summary is required", "tile.json")
    skills = data.get("skills")
    if not isinstance(skills, dict) or not skills:
        result.error("TILE-SKILLS", "tile skills mapping is required", "tile.json")
        return
    if skill_name and skill_name not in skills:
        result.error("TILE-SKILL-NAME", f"tile does not expose '{skill_name}'", "tile.json")
    for exposed, config in skills.items():
        if not isinstance(config, dict) or not isinstance(config.get("path"), str):
            result.error("TILE-SKILL-PATH", f"invalid path for skill '{exposed}'", "tile.json")
            continue
        target = root / config["path"]
        if not target.is_file():
            result.error(
                "TILE-SKILL-MISSING",
                f"tile skill path does not exist: {config['path']}",
                "tile.json",
            )


def validate_openai_yaml(root: Path, result: Validation, skill_name: str | None) -> None:
    path = root / "agents/openai.yaml"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for key in ("interface:", "display_name:", "short_description:", "default_prompt:"):
        if key not in text:
            result.error("OPENAI-YAML", f"missing key {key}", relative(path, root))
    if skill_name and f"${skill_name}" not in text:
        result.warning(
            "OPENAI-PROMPT",
            f"default_prompt does not mention ${skill_name}",
            relative(path, root),
        )


def clean_reference(value: str) -> str:
    value = value.strip().strip("`'")
    value = value.split("#", 1)[0]
    return value.rstrip(".,;:)]}")


def validate_links(root: Path, result: Validation) -> None:
    markdown_files = sorted(root.rglob("*.md"))
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        candidates: set[tuple[str, bool]] = set()
        for match in LOCAL_PATH.finditer(text):
            candidates.add((clean_reference(match.group(1)), True))
        for match in MARKDOWN_LINK.finditer(text):
            value = match.group(1).strip()
            if value.startswith(("http://", "https://", "mailto:", "#")):
                continue
            candidates.add((clean_reference(value), False))
        for value, root_relative in candidates:
            if not value or any(char in value for char in ("*", "<", ">", "$")):
                continue
            target = root / value if root_relative else path.parent / value
            if not target.exists():
                result.error(
                    "LINK-MISSING",
                    f"local reference does not exist: {value}",
                    relative(path, root),
                )


def validate_json_files(root: Path, result: Validation) -> None:
    for path in sorted(root.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            result.error("JSON-INVALID", str(exc), relative(path, root))


def validate_scripts(root: Path, result: Validation) -> None:
    for path in sorted((root / "scripts").glob("*.py")) if (root / "scripts").is_dir() else []:
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            result.error("PYTHON-SYNTAX", str(exc), relative(path, root))
        if not os.access(path, os.X_OK):
            result.warning("SCRIPT-EXECUTABLE", "Python script is not executable", relative(path, root))
    bash = shutil.which("bash")
    for path in sorted((root / "scripts").glob("*.sh")) if (root / "scripts").is_dir() else []:
        if not os.access(path, os.X_OK):
            result.warning("SCRIPT-EXECUTABLE", "shell script is not executable", relative(path, root))
        if bash:
            completed = subprocess.run(
                [bash, "-n", str(path)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if completed.returncode:
                result.error("SHELL-SYNTAX", completed.stderr.strip(), relative(path, root))
        else:
            result.warning("SHELL-NO-BASH", "bash unavailable; syntax not checked", relative(path, root))
    migration = root / "migration"
    if migration.is_dir():
        for path in sorted(migration.glob("*.sh")):
            if not os.access(path, os.X_OK):
                result.warning("SCRIPT-EXECUTABLE", "migration script is not executable", relative(path, root))
            if bash:
                completed = subprocess.run(
                    [bash, "-n", str(path)],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                if completed.returncode:
                    result.error("SHELL-SYNTAX", completed.stderr.strip(), relative(path, root))


def validate_evals(root: Path, result: Validation, skill_name: str | None) -> None:
    eval_root = root / "evals"
    eval_file = eval_root / "evals.json"
    if eval_file.is_file():
        try:
            data = json.loads(eval_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return
        if data.get("skill_name") != skill_name:
            result.error("EVAL-SKILL-NAME", "evals.json skill_name mismatch", relative(eval_file, root))
        evals = data.get("evals")
        if not isinstance(evals, list) or not evals:
            result.error("EVAL-LIST", "evals.json needs a non-empty evals list", relative(eval_file, root))
        else:
            ids: set[int | str] = set()
            for index, item in enumerate(evals):
                if not isinstance(item, dict):
                    result.error("EVAL-ITEM", f"eval #{index + 1} is not an object", relative(eval_file, root))
                    continue
                for key in ("id", "prompt", "expected_output"):
                    if key not in item:
                        result.error("EVAL-FIELD", f"eval #{index + 1} missing {key}", relative(eval_file, root))
                if item.get("id") in ids:
                    result.error("EVAL-DUPLICATE", f"duplicate eval id {item.get('id')}", relative(eval_file, root))
                ids.add(item.get("id"))
    instruction_file = eval_root / "instructions.json"
    if instruction_file.is_file():
        try:
            instructions = json.loads(instruction_file.read_text(encoding="utf-8")).get("instructions")
        except json.JSONDecodeError:
            instructions = None
        if not isinstance(instructions, list) or not instructions:
            result.error("EVAL-INSTRUCTIONS", "instructions.json needs a non-empty instructions list", relative(instruction_file, root))
        else:
            for index, item in enumerate(instructions):
                if not isinstance(item, dict) or not all(
                    key in item
                    for key in ("instruction", "original_snippets", "relevant_when", "why_given")
                ):
                    result.error(
                        "EVAL-INSTRUCTION-FIELD",
                        f"instruction #{index + 1} is incomplete",
                        relative(instruction_file, root),
                    )
    scenario_dirs = sorted(path for path in eval_root.glob("scenario-*") if path.is_dir())
    if not scenario_dirs:
        result.warning("EVAL-SCENARIOS", "no Tessl scenario directories found", "evals")
    for scenario in scenario_dirs:
        for name in ("capability.txt", "task.md", "criteria.json"):
            if not (scenario / name).is_file():
                result.error("EVAL-SCENARIO-FILE", f"missing {name}", relative(scenario, root))
        criteria_path = scenario / "criteria.json"
        if not criteria_path.is_file():
            continue
        try:
            criteria = json.loads(criteria_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        checklist = criteria.get("checklist")
        if criteria.get("type") != "weighted_checklist" or not isinstance(checklist, list):
            result.error("EVAL-CRITERIA", "criteria must be a weighted_checklist", relative(criteria_path, root))
            continue
        score = sum(
            item.get("max_score", 0)
            for item in checklist
            if isinstance(item, dict) and isinstance(item.get("max_score"), (int, float))
        )
        if score != 100:
            result.error(
                "EVAL-SCORE",
                f"criteria max_score total is {score}, expected 100",
                relative(criteria_path, root),
            )


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def validate_manifest(root: Path, result: Validation) -> None:
    path = root / "BUNDLE-MANIFEST.txt"
    if not path.is_file():
        return
    entries: dict[str, tuple[str, int]] = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line or line.startswith("#"):
            continue
        parts = line.split("  ", 2)
        if len(parts) != 3 or not re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            result.error("MANIFEST-FORMAT", f"invalid manifest line {number}", "BUNDLE-MANIFEST.txt")
            continue
        try:
            size = int(parts[1])
        except ValueError:
            result.error("MANIFEST-SIZE", f"invalid byte size on line {number}", "BUNDLE-MANIFEST.txt")
            continue
        entries[parts[2]] = (parts[0], size)

    actual_files = {
        relative(file, root): file
        for file in root.rglob("*")
        if file.is_file()
        and not file.is_symlink()
        and relative(file, root) != "BUNDLE-MANIFEST.txt"
        and not any(part in {".git", "__pycache__", ".pytest_cache", ".mypy_cache"} for part in file.relative_to(root).parts)
        and file.suffix not in {".pyc", ".class", ".jar", ".zip"}
    }
    missing = sorted(set(actual_files) - set(entries))
    extra = sorted(set(entries) - set(actual_files))
    if missing:
        result.error("MANIFEST-MISSING", "manifest omits: " + ", ".join(missing[:10]), "BUNDLE-MANIFEST.txt")
    if extra:
        result.error("MANIFEST-EXTRA", "manifest lists missing files: " + ", ".join(extra[:10]), "BUNDLE-MANIFEST.txt")
    for relative_path, file in actual_files.items():
        expected = entries.get(relative_path)
        if expected is None:
            continue
        digest, size = expected
        actual_size = file.stat().st_size
        if actual_size != size:
            result.error("MANIFEST-BYTES", f"byte-size mismatch for {relative_path}", "BUNDLE-MANIFEST.txt")
        if sha256(file) != digest:
            result.error("MANIFEST-HASH", f"SHA-256 mismatch for {relative_path}", "BUNDLE-MANIFEST.txt")


def validate_hygiene(root: Path, result: Validation) -> None:
    for path in sorted(root.rglob("*")):
        rel = relative(path, root)
        if path.is_symlink():
            result.error("BUNDLE-SYMLINK", "symlinks are not allowed in the portable bundle", rel)
            continue
        if path.is_dir():
            if path.name in {"__pycache__", ".pytest_cache", ".mypy_cache", ".git"}:
                result.error("BUNDLE-CACHE", "cache/VCS directory must not be bundled", rel)
            continue
        if path.name in {".DS_Store", "Thumbs.db"} or path.suffix in {".pyc", ".class", ".jar"}:
            result.error("BUNDLE-BINARY", "generated/binary file must not be bundled", rel)
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > 1_000_000:
            result.warning("BUNDLE-LARGE", f"file is {size} bytes", rel)
    for path in sorted((root / "references").glob("*.md")) if (root / "references").is_dir() else []:
        lines = len(path.read_text(encoding="utf-8").splitlines())
        if lines > 650:
            result.warning(
                "REFERENCE-LENGTH",
                f"reference has {lines} lines; consider splitting for deferred disclosure",
                relative(path, root),
            )


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    result = Validation()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    validate_required(root, result)
    frontmatter = validate_frontmatter(root, result)
    skill_name = frontmatter.get("name") if isinstance(frontmatter, dict) else None
    validate_tile(root, result, skill_name if isinstance(skill_name, str) else None)
    validate_openai_yaml(root, result, skill_name if isinstance(skill_name, str) else None)
    validate_links(root, result)
    validate_json_files(root, result)
    validate_scripts(root, result)
    validate_evals(root, result, skill_name if isinstance(skill_name, str) else None)
    validate_hygiene(root, result)

    status = "valid" if not result.errors else "invalid"
    if args.json:
        payload = {
            "status": status,
            "root": str(root),
            "errors": len(result.errors),
            "warnings": len(result.warnings),
            "issues": [asdict(issue) for issue in result.issues],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for issue in result.issues:
            location = f" [{issue.path}]" if issue.path else ""
            print(f"[{issue.level.upper()}] {issue.code}{location}: {issue.message}")
        print(
            f"\n{status.upper()}: {len(result.errors)} error(s), {len(result.warnings)} warning(s)"
        )
    if result.errors or (args.strict_warnings and result.warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
