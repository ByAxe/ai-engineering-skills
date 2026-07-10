#!/usr/bin/env python3
"""Conservative heuristic scanner for Java and Quarkus risk candidates.

Findings are candidates for semantic review, never proof of a defect. The script
uses only the Python standard library and never modifies the target repository.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Pattern

SCHEMA_VERSION = "1.0.0"
SKIP_DIRS = {
    ".git",
    ".gradle",
    ".idea",
    ".mvn",
    "node_modules",
    "target",
    "build",
    "out",
    "dist",
    "generated",
    "generated-sources",
    "vendor",
    ".cache",
    ".quarkus",
}
SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}
MAX_FILE_BYTES = 3_000_000


@dataclass(frozen=True)
class Context:
    quarkus: bool
    reactive: bool
    virtual_threads: bool
    java_release: int | None
    entity: bool
    rest_resource: bool
    application_scoped: bool
    test_file: bool


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    confidence: str
    category: str
    path: str
    line: int
    message: str
    rationale: str
    remediation: str
    excerpt: str
    heuristic: bool = True


@dataclass(frozen=True)
class LineRule:
    rule_id: str
    pattern: Pattern[str]
    severity: str
    confidence: str
    category: str
    message: str
    rationale: str
    remediation: str
    condition: Callable[[Context], bool] = lambda _ctx: True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="repository or source root")
    parser.add_argument(
        "--format", choices=("markdown", "json", "sarif"), default="markdown"
    )
    parser.add_argument("--output", type=Path, help="write output to a file")
    parser.add_argument(
        "--min-severity",
        choices=tuple(SEVERITY_ORDER),
        default="low",
        help="minimum reported severity",
    )
    parser.add_argument(
        "--exclude-tests", action="store_true", help="skip files under test source sets"
    )
    parser.add_argument(
        "--max-findings", type=int, default=1000, help="safety cap (default: 1000)"
    )
    parser.add_argument(
        "--fail-on",
        choices=("none", "medium", "high", "critical"),
        default="none",
        help="return 1 if a finding at or above this severity exists",
    )
    return parser.parse_args()


def is_skipped(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in SKIP_DIRS for part in parts)


def iter_java_files(root: Path) -> Iterable[Path]:
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        dirnames[:] = [
            name for name in dirnames if not is_skipped(current_path / name, root)
        ]
        for name in filenames:
            path = current_path / name
            if name.endswith(".java") and not is_skipped(path, root):
                yield path


def read_text(path: Path) -> str:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def sanitize_java(text: str) -> str:
    """Replace comments with spaces while preserving strings and line positions."""
    chars = list(text)
    i = 0
    state = "normal"
    while i < len(chars):
        ch = chars[i]
        nxt = chars[i + 1] if i + 1 < len(chars) else ""
        if state == "normal":
            if ch == "/" and nxt == "/":
                chars[i] = chars[i + 1] = " "
                i += 2
                while i < len(chars) and chars[i] != "\n":
                    chars[i] = " "
                    i += 1
                continue
            if ch == "/" and nxt == "*":
                chars[i] = chars[i + 1] = " "
                state = "block"
                i += 2
                continue
            if text.startswith('"""', i):
                state = "textblock"
                i += 3
                continue
            if ch == '"':
                state = "string"
            elif ch == "'":
                state = "char"
        elif state == "block":
            if ch == "*" and nxt == "/":
                chars[i] = chars[i + 1] = " "
                state = "normal"
                i += 2
                continue
            if ch != "\n":
                chars[i] = " "
        elif state == "string":
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                state = "normal"
        elif state == "char":
            if ch == "\\":
                i += 2
                continue
            if ch == "'":
                state = "normal"
        elif state == "textblock":
            if text.startswith('"""', i):
                state = "normal"
                i += 3
                continue
        i += 1
    return "".join(chars)


def detect_project(root: Path) -> tuple[bool, int | None, bool]:
    build_names = {
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "gradle.properties",
        "libs.versions.toml",
    }
    texts: list[str] = []
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        dirnames[:] = [
            name for name in dirnames if not is_skipped(current_path / name, root)
        ]
        for name in filenames:
            if name in build_names:
                text = read_text(current_path / name)
                if text:
                    texts.append(text)
        if len(texts) > 100:
            break
    joined = "\n".join(texts)
    quarkus = bool(re.search(r"\bio\.quarkus\b|quarkus-maven-plugin", joined))
    virtual = bool(
        re.search(r"RunOnVirtualThread|newVirtualThreadPerTaskExecutor|Thread\.ofVirtual", joined)
    )
    candidates: list[int] = []
    patterns = (
        r"<maven\.compiler\.release>\s*(\d+)",
        r"<java\.version>\s*(\d+)",
        r"<release>\s*(\d+)",
        r"JavaLanguageVersion\.of\s*\(\s*(\d+)",
        r"sourceCompatibility\s*=\s*['\"]?(?:JavaVersion\.VERSION_)?(\d+)",
    )
    for pattern in patterns:
        candidates.extend(int(value) for value in re.findall(pattern, joined))
    release = max(candidates) if candidates else None
    return quarkus, release, virtual


def context_for(
    text: str,
    path: Path,
    root: Path,
    project_quarkus: bool,
    java_release: int | None,
    project_virtual: bool,
) -> Context:
    rel_parts = {part.lower() for part in path.relative_to(root).parts}
    test_file = "test" in rel_parts or "tests" in rel_parts
    reactive = bool(
        re.search(
            r"\b(?:io\.smallrye\.mutiny\.(?:Uni|Multi)|Uni\s*<|Multi\s*<|CompletionStage\s*<|Publisher\s*<)",
            text,
        )
    )
    virtual = project_virtual or bool(
        re.search(r"@RunOnVirtualThread|newVirtualThreadPerTaskExecutor|Thread\.ofVirtual", text)
    )
    return Context(
        quarkus=project_quarkus or "io.quarkus" in text,
        reactive=reactive,
        virtual_threads=virtual,
        java_release=java_release,
        entity=bool(re.search(r"(?m)^\s*@(?:jakarta\.persistence\.)?Entity\b", text)),
        rest_resource=bool(re.search(r"(?m)^\s*@(?:jakarta\.ws\.rs\.)?Path\s*\(", text)),
        application_scoped="@ApplicationScoped" in text,
        test_file=test_file,
    )


def excerpt(line: str) -> str:
    value = re.sub(r"\s+", " ", line.strip())
    return value[:237] + "..." if len(value) > 240 else value


def make_line_rules() -> list[LineRule]:
    return [
        LineRule(
            "EJ-TYPE-001",
            re.compile(r"\bMap\s*<\s*String\s*,\s*(?:Object|\?)\s*>"),
            "medium",
            "medium",
            "domain-model",
            "Dynamic map schema crosses a typed Java boundary",
            "String/object maps defer schema, nullness, and conversion errors to runtime.",
            "Confirm whether this is a boundary-only payload; introduce a typed DTO/value model when it crosses layers.",
        ),
        LineRule(
            "EJ-TYPE-002",
            re.compile(r"\b(?:List|Set|Map|Collection|Optional|Class)\s+[A-Za-z_$][\w$]*\s*(?:[=;,)]|$)"),
            "medium",
            "medium",
            "generics",
            "Raw generic type candidate",
            "Raw types disable generic type checks and can create heap pollution.",
            "Parameterize the type or localize/document an unavoidable legacy bridge.",
        ),
        LineRule(
            "EJ-NULL-001",
            re.compile(r"\breturn\s+null\s*;"),
            "low",
            "low",
            "nullness",
            "Null return requires contract review",
            "Null may be valid internally, but public absence semantics are often unclear.",
            "Inspect callers and API policy; keep, annotate, or replace with an explicit absence/result model as warranted.",
        ),
        LineRule(
            "EJ-ERR-001",
            re.compile(r"\bcatch\s*\(\s*(?:final\s+)?(?:Exception|Throwable)\b"),
            "medium",
            "high",
            "exceptions",
            "Broad catch candidate",
            "Broad catches can mask programming errors, cancellation, and distinct recovery policies.",
            "Catch only failures the boundary can handle; preserve cause and fatal/cancellation semantics.",
        ),
        LineRule(
            "EJ-ERR-002",
            re.compile(r"\.printStackTrace\s*\(|\bSystem\.(?:out|err)\."),
            "medium",
            "high",
            "observability",
            "Unmanaged process output in Java code",
            "Direct output bypasses structured logging, redaction, routing, and correlation.",
            "Use the repository logger at the owning boundary and avoid duplicate failure logs.",
        ),
        LineRule(
            "EJ-ERR-003",
            re.compile(r"\bcatch\s*\(\s*(?:final\s+)?InterruptedException\b"),
            "medium",
            "medium",
            "concurrency",
            "InterruptedException handling requires inspection",
            "Swallowing interruption breaks cancellation and orderly shutdown.",
            "Propagate or restore the interrupt unless the API fully consumes cancellation by contract.",
        ),
        LineRule(
            "EJ-NUM-001",
            re.compile(r"new\s+BigDecimal\s*\(\s*[+-]?(?:\d+\.\d*|\.\d+)(?:[dDfF])?\s*\)"),
            "high",
            "high",
            "numeric",
            "BigDecimal is constructed from a floating-point literal",
            "The binary floating-point value may not equal the intended decimal value.",
            "Use a decimal string, BigDecimal.valueOf, or integer minor units according to the domain contract.",
        ),
        LineRule(
            "EJ-TEXT-001",
            re.compile(r"\.getBytes\s*\(\s*\)"),
            "medium",
            "high",
            "text-io",
            "Platform-default charset used by getBytes()",
            "Encoding changes across hosts and containers.",
            "Pass StandardCharsets or the protocol-defined charset explicitly.",
        ),
        LineRule(
            "EJ-TEXT-002",
            re.compile(r"new\s+String\s*\(\s*[^,()]+\s*\)"),
            "medium",
            "medium",
            "text-io",
            "One-argument String construction may use the default charset",
            "Byte-to-text decoding without a charset is host-dependent; this match needs constructor-type inspection.",
            "If the argument is bytes, pass the protocol charset explicitly.",
        ),
        LineRule(
            "EJ-TEXT-003",
            re.compile(r"\b(?:Charset\.defaultCharset|Locale\.getDefault|ZoneId\.systemDefault)\s*\("),
            "low",
            "high",
            "locale-time",
            "System-default locale/charset/zone is part of behavior",
            "Defaults vary by host and may be wrong for machine contracts.",
            "Use an explicit contract value or inject the user/business setting; retain defaults only when intended.",
        ),
        LineRule(
            "EJ-TIME-001",
            re.compile(r"\b(?:LocalDateTime|LocalDate|ZonedDateTime|OffsetDateTime|Instant)\.now\s*\(\s*\)"),
            "low",
            "high",
            "time",
            "Direct system-clock read reduces determinism",
            "Time-sensitive logic becomes host- and timing-dependent.",
            "Inject Clock or confine the system read to a clear boundary when tests/business rules need control.",
        ),
        LineRule(
            "EJ-COL-001",
            re.compile(r"\.parallelStream\s*\("),
            "high",
            "high",
            "concurrency",
            "parallelStream uses shared parallel execution implicitly",
            "Server code can contend on the common pool and lose request context; benefit is workload-dependent.",
            "Prefer sequential code unless measured; use an explicit bounded design for true CPU parallelism.",
        ),
        LineRule(
            "EJ-CON-001",
            re.compile(r"\bExecutors\.new(?:Fixed|Cached|Single|Scheduled|WorkStealing|VirtualThread)[A-Za-z]*\s*\("),
            "medium",
            "high",
            "concurrency",
            "Executor creation introduces a lifecycle and execution boundary",
            "A new executor can bypass framework context and needs an owner; try-with-resources bounds lifetime but does not define workload, capacity, or context policy.",
            "Keep explicit close for bounded local work or use managed execution; make ownership, bounds, rejection, cancellation, and shutdown explicit.",
        ),
        LineRule(
            "EJ-CON-002",
            re.compile(r"\bnew\s+Thread\s*\(|\bThread\.startVirtualThread\s*\("),
            "medium",
            "high",
            "concurrency",
            "Ad-hoc thread creation needs lifecycle review",
            "Detached threads complicate cancellation, error propagation, context, and shutdown.",
            "Use structured/framework-managed execution or document explicit ownership and completion.",
        ),
        LineRule(
            "EJ-CON-003",
            re.compile(r"\bThreadLocal\s*<|\bThreadLocal\.withInitial\s*\("),
            "medium",
            "high",
            "concurrency",
            "ThreadLocal use requires context and virtual-thread review",
            "Values can leak across pooled work or allocate per short-lived virtual thread.",
            "Use supported context propagation/scoped explicit data and ensure cleanup; retain only with measured justification.",
        ),
        LineRule(
            "EJ-CON-004",
            re.compile(r"\bThread\.sleep\s*\("),
            "low",
            "high",
            "concurrency",
            "Thread.sleep may encode timing instead of synchronization",
            "In tests it causes flakiness; in production it consumes request/task lifetime and ignores richer scheduling.",
            "Use a deterministic signal/scheduler/backoff abstraction with a deadline where appropriate.",
        ),
        LineRule(
            "EJ-CON-005",
            re.compile(r"\bCompletableFuture\.(?:supplyAsync|runAsync)\s*\("),
            "medium",
            "medium",
            "concurrency",
            "CompletableFuture async call requires executor/context inspection",
            "The no-executor overload uses the common pool; even explicit executors need ownership and context policy.",
            "Confirm overload and executor; prefer managed execution and compose cancellation/failure.",
        ),
        LineRule(
            "EJ-DB-001",
            re.compile(r"^\s*@Transactional\b"),
            "low",
            "low",
            "transactions",
            "Transaction annotation requires invocation-boundary review",
            "Interception, reactive completion, rollback, and external side effects are semantic.",
            "Trace the actual CDI call path and transaction model; keep this finding only when a concrete risk is present.",
        ),
        LineRule(
            "EJ-QUA-001",
            re.compile(r"^\s*import\s+javax\.(?:enterprise|inject|persistence|transaction|validation|ws\.rs)\."),
            "high",
            "high",
            "quarkus-versioning",
            "Legacy javax API imported in a Quarkus project",
            "Modern Quarkus generations use Jakarta APIs; mixed generations can fail augmentation or indicate incomplete migration.",
            "Confirm the project generation and replace only when the dependency/API migration is supported.",
            condition=lambda ctx: ctx.quarkus,
        ),
        LineRule(
            "EJ-QUA-002",
            re.compile(r"^\s*@Named(?:\s*\(|\s*$)"),
            "medium",
            "high",
            "quarkus-cdi",
            "@Named used in Quarkus CDI",
            "As a sole qualifier it can also confer @Default and create ambiguity; names are not type-safe.",
            "Use a type-safe qualifier or supported identifier unless an external language/template needs the bean name.",
            condition=lambda ctx: ctx.quarkus,
        ),
        LineRule(
            "EJ-QUA-003",
            re.compile(r"\.await\s*\(\s*\)\s*\.indefinitely\s*\(|\.await\s*\(\s*\)\s*\.atMost\s*\("),
            "high",
            "high",
            "quarkus-execution",
            "Reactive value is synchronously awaited",
            "Blocking an event-loop path can cause starvation/deadlock and loses reactive cancellation semantics.",
            "Compose the reactive chain or explicitly dispatch a truly blocking boundary on an appropriate worker/virtual thread.",
            condition=lambda ctx: ctx.quarkus and ctx.reactive,
        ),
        LineRule(
            "EJ-QUA-004",
            re.compile(r"^\s*@RegisterForReflection\s*(?:$|\(\s*\))"),
            "medium",
            "medium",
            "quarkus-native",
            "Broad implicit reflection registration candidate",
            "Unscoped registration can enlarge native images and mask the exact reflective access.",
            "Identify the consumer and register precise targets/members or use extension/generated support.",
            condition=lambda ctx: ctx.quarkus,
        ),
        LineRule(
            "EJ-SEC-001",
            re.compile(r"\b(?:Runtime\.getRuntime\(\)\.exec|new\s+ProcessBuilder)\s*\("),
            "high",
            "high",
            "security",
            "Process execution boundary requires input and lifecycle review",
            "Untrusted command composition enables injection; processes also need timeouts, I/O draining, and cleanup.",
            "Use fixed executable/argument lists, strict allowlists, bounded I/O/timeouts, and avoid shells.",
        ),
        LineRule(
            "EJ-SEC-002",
            re.compile(r"\b(?:SELECT|INSERT|UPDATE|DELETE)\b[^\n;]*[\"']\s*\+", re.IGNORECASE),
            "high",
            "medium",
            "security-persistence",
            "SQL-like text concatenation candidate",
            "Concatenating untrusted values can cause injection; dynamic identifiers also need allowlisting.",
            "Use parameters and a fixed/allowlisted query structure after inspecting the actual string source.",
        ),
    ]


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def brace_depth_at(text: str, offset: int) -> int:
    """Return Java brace depth while ignoring string, char, and text-block literals."""
    depth = 0
    i = 0
    state = "normal"
    while i < min(offset, len(text)):
        ch = text[i]
        if state == "normal":
            if text.startswith('"""', i):
                state = "textblock"
                i += 3
                continue
            if ch == '"':
                state = "string"
            elif ch == "'":
                state = "char"
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth = max(0, depth - 1)
        elif state in {"string", "char"}:
            if ch == "\\":
                i += 2
                continue
            if (state == "string" and ch == '"') or (state == "char" and ch == "'"):
                state = "normal"
        elif state == "textblock" and text.startswith('"""', i):
            state = "normal"
            i += 3
            continue
        i += 1
    return depth


def add_finding(
    findings: list[Finding],
    *,
    rule_id: str,
    severity: str,
    confidence: str,
    category: str,
    path: str,
    line: int,
    message: str,
    rationale: str,
    remediation: str,
    source_line: str,
) -> None:
    findings.append(
        Finding(
            rule_id=rule_id,
            severity=severity,
            confidence=confidence,
            category=category,
            path=path,
            line=max(1, line),
            message=message,
            rationale=rationale,
            remediation=remediation,
            excerpt=excerpt(source_line),
        )
    )


def scan_cross_patterns(
    text: str, sanitized: str, path: str, ctx: Context, findings: list[Finding]
) -> None:
    lines = text.splitlines()

    def source_line_at(offset: int) -> str:
        line = line_of(sanitized, offset)
        return lines[line - 1] if 0 < line <= len(lines) else ""

    optional_names = set(
        re.findall(
            r"\bOptional(?:Int|Long|Double)?(?:\s*<[^;=(){}\n]+>)?\s+([A-Za-z_$][\w$]*)",
            sanitized,
        )
    )
    for name in sorted(optional_names):
        access = re.compile(
            rf"\b{re.escape(name)}\.(?:get|getAsInt|getAsLong|getAsDouble)\s*\(\s*\)"
        )
        for match in access.finditer(sanitized):
            add_finding(
                findings,
                rule_id="EJ-NULL-002",
                severity="low",
                confidence="high",
                category="nullness",
                path=path,
                line=line_of(sanitized, match.start()),
                message="Optional value is read with an unchecked get",
                rationale="Optional.get and primitive Optional getters throw when absence is possible and can hide the intended absence contract.",
                remediation="Prove presence before access, use an explicit fallback/exception, or restructure the API around the actual absence policy.",
                source_line=source_line_at(match.start()),
            )

    for match in re.finditer(r"\bcatch\s*\([^)]*\)\s*\{\s*\}", sanitized, re.DOTALL):
        add_finding(
            findings,
            rule_id="EJ-ERR-004",
            severity="high",
            confidence="high",
            category="exceptions",
            path=path,
            line=line_of(sanitized, match.start()),
            message="Empty catch block",
            rationale="The failure is discarded and program state may be unknown.",
            remediation="Handle, compensate, translate, or propagate; document an intentionally ignored narrow exception.",
            source_line=source_line_at(match.start()),
        )

    for match in re.finditer(
        r"@Transactional(?:\s*\([^)]*\))?\s*(?:@[\w.]+(?:\([^)]*\))?\s*)*private\s+",
        sanitized,
        re.DOTALL,
    ):
        add_finding(
            findings,
            rule_id="EJ-TX-001",
            severity="high",
            confidence="medium",
            category="transactions",
            path=path,
            line=line_of(sanitized, match.start()),
            message="Transactional private method may not be intercepted as intended",
            rationale="Transaction semantics depend on container interception and the actual invocation path.",
            remediation="Move the boundary to an interceptable CDI method or verify project-specific interception with an integration rollback test.",
            source_line=source_line_at(match.start()),
        )

    for match in re.finditer(
        r"\brecord\s+[A-Za-z_$][\w$]*\s*\((?P<components>[^)]*\[\][^)]*)\)",
        sanitized,
        re.DOTALL,
    ):
        add_finding(
            findings,
            rule_id="EJ-REC-001",
            severity="high",
            confidence="high",
            category="java-language",
            path=path,
            line=line_of(sanitized, match.start()),
            message="Record contains an array component",
            rationale="Generated equality compares arrays by reference and the accessor exposes mutable storage.",
            remediation="Use an immutable collection/value type or implement defensive ownership and explicit deep equality in a class.",
            source_line=source_line_at(match.start()),
        )

    for match in re.finditer(
        r"\brecord\s+[A-Za-z_$][\w$]*\s*\((?P<components>[^)]*\b(?:List|Set|Map|Collection)\s*<[^)]*)\)",
        sanitized,
        re.DOTALL,
    ):
        add_finding(
            findings,
            rule_id="EJ-REC-002",
            severity="medium",
            confidence="medium",
            category="java-language",
            path=path,
            line=line_of(sanitized, match.start()),
            message="Record owns a potentially mutable collection component",
            rationale="A record is shallowly immutable; caller mutations can change its observable value and hash behavior.",
            remediation="Confirm ownership and use copyOf/immutable value semantics when mutation is not contractual.",
            source_line=source_line_at(match.start()),
        )

    assignment = re.compile(
        r"(?m)^\s*(?:var|List\s*<[^;=]+>)\s+([A-Za-z_$][\w$]*)\s*=\s*[^;]*(?:\.toList\s*\(\s*\)|List\.copyOf\s*\([^;]+\))\s*;"
    )
    for match in assignment.finditer(sanitized):
        variable = match.group(1)
        tail = sanitized[match.end() :]
        mutation = re.search(
            rf"\b{re.escape(variable)}\.(?:add|addAll|remove|removeIf|clear|sort|replaceAll|set)\s*\(",
            tail,
        )
        if mutation:
            add_finding(
                findings,
                rule_id="EJ-COL-002",
                severity="high",
                confidence="high",
                category="collections",
                path=path,
                line=line_of(sanitized, match.start()),
                message=f"Collection '{variable}' is created unmodifiable and later mutated",
                rationale="Stream.toList and List.copyOf produce unmodifiable lists; mutation throws at runtime.",
                remediation="Use a mutable collector/copy only if mutation is part of the contract, otherwise remove the mutation.",
                source_line=source_line_at(match.start()),
            )

    if ctx.entity and re.search(r"\brecord\s+", sanitized):
        match = re.search(r"\brecord\s+", sanitized)
        assert match is not None
        add_finding(
            findings,
            rule_id="EJ-DB-002",
            severity="high",
            confidence="high",
            category="persistence",
            path=path,
            line=line_of(sanitized, match.start()),
            message="Persistence entity is declared as a record",
            rationale="ORM identity, proxies/enhancement, lifecycle mutation, and generated record equality conflict in common JPA models.",
            remediation="Use a persistence-compatible class and reserve records for DTOs/value projections supported by the stack.",
            source_line=source_line_at(match.start()),
        )

    if ctx.entity and ctx.rest_resource:
        match = re.search(r"@(?:jakarta\.persistence\.)?Entity\b", sanitized)
        assert match is not None
        add_finding(
            findings,
            rule_id="EJ-QUA-005",
            severity="high",
            confidence="high",
            category="quarkus-rest-persistence",
            path=path,
            line=line_of(sanitized, match.start()),
            message="The same type is both a REST resource and a persistence entity",
            rationale="Transport and persistence lifecycles/contracts become inseparable and can expose lazy/internal state.",
            remediation="Separate the resource boundary from the entity; introduce only the smallest service/DTO boundary needed.",
            source_line=source_line_at(match.start()),
        )

    field_injection = re.compile(
        r"@Inject\s*(?:@[\w.]+(?:\([^)]*\))?\s*)*(?:(?:public|protected|private)\s+)?(?!static\b)(?:final\s+)?[\w.$<>?, \[\]]+\s+[A-Za-z_$][\w$]*\s*;",
        re.DOTALL,
    )
    if ctx.quarkus:
        for match in field_injection.finditer(sanitized):
            add_finding(
                findings,
                rule_id="EJ-QUA-006",
                severity="low",
                confidence="high",
                category="quarkus-cdi",
                path=path,
                line=line_of(sanitized, match.start()),
                message="Quarkus CDI field injection candidate",
                rationale="Field injection hides mandatory dependencies and makes plain unit construction harder; it may still be intentional.",
                remediation="Prefer constructor injection for required collaborators when proxy/framework constraints and local conventions allow it.",
                source_line=source_line_at(match.start()),
            )

    if ctx.application_scoped:
        mutable_field = re.compile(
            r"(?m)^[ \t]*(?:(?:public|protected|private)[ \t]+)?(?!static\b)(?!final\b)(?:volatile[ \t]+)?(?:Map|List|Set|Collection|HashMap|ArrayList|HashSet|int|long|boolean|[A-Z][\w$<>?, ]*)[ \t]+[A-Za-z_$][\w$]*[ \t]*(?:=|;)"
        )
        emitted = 0
        for match in mutable_field.finditer(sanitized):
            # Top-level bean fields are at brace depth one. This avoids flagging
            # ordinary mutable local variables inside methods.
            if brace_depth_at(sanitized, match.start()) != 1:
                continue
            line_number = line_of(sanitized, match.start())
            previous = line_number - 2
            injected = False
            while previous >= 0:
                value = lines[previous].strip()
                if not value:
                    break
                if not value.startswith("@"):
                    break
                injected = injected or bool(re.search(r"@(?:jakarta\.inject\.)?Inject\b", value))
                previous -= 1
            if injected:
                continue
            add_finding(
                findings,
                rule_id="EJ-QUA-007",
                severity="medium",
                confidence="low",
                category="quarkus-cdi-concurrency",
                path=path,
                line=line_number,
                message="Mutable field in application-scoped bean needs concurrency review",
                rationale="Application-scoped beans are shared and can receive concurrent calls; not every mutable field is unsafe.",
                remediation="Confirm state ownership and compound operations; prefer immutable/config state, confinement, or an explicit bounded synchronization design.",
                source_line=source_line_at(match.start()),
            )
            emitted += 1
            if emitted >= 5:
                break

    if ctx.reactive:
        # Prefer an actual invocation over an import or field declaration so the
        # finding points at evidence an agent can inspect. The fallback remains
        # deliberately low-confidence because a blocking API type can be used
        # only from a worker-dispatched method in the same file.
        blocking_operation = re.compile(
            r"(?:"
            r"\bFiles\.(?:copy|delete|lines|list|move|newInputStream|newOutputStream|"
            r"read|readAllBytes|readAllLines|readString|walk|write|writeString)\s*\("
            r"|\bThread\.sleep\s*\("
            r"|\.(?:join|get)\s*\(\s*\)"
            r"|\.(?:persist|merge|remove|flush|createQuery|createNativeQuery|"
            r"execute|query|queryForObject|update)\s*\("
            r")"
        )
        blocking_type = re.compile(
            r"\b(?:EntityManager|PanacheEntity|PanacheRepository|java\.sql\.|JdbcTemplate)\b"
        )
        match = blocking_operation.search(sanitized)
        if match is None:
            for candidate_match in blocking_type.finditer(sanitized):
                candidate_line = source_line_at(candidate_match.start()).lstrip()
                if candidate_line.startswith(("import ", "package ")):
                    continue
                match = candidate_match
                break
        if match:
            add_finding(
                findings,
                rule_id="EJ-QUA-008",
                severity="high",
                confidence="low",
                category="quarkus-execution",
                path=path,
                line=line_of(sanitized, match.start()),
                message="Reactive type and blocking-operation candidate coexist",
                rationale="If the call is on an event loop, blocking ORM/I/O/waits can starve it; file-level co-occurrence is only a candidate.",
                remediation="Trace the exact method and dispatch; use a consistent reactive stack or explicit worker/virtual-thread boundary.",
                source_line=source_line_at(match.start()),
            )

    config_count = len(re.findall(r"@ConfigProperty\b", sanitized))
    if ctx.quarkus and config_count >= 5:
        match = re.search(r"@ConfigProperty\b", sanitized)
        assert match is not None
        add_finding(
            findings,
            rule_id="EJ-QUA-009",
            severity="low",
            confidence="medium",
            category="quarkus-config",
            path=path,
            line=line_of(sanitized, match.start()),
            message=f"{config_count} scattered @ConfigProperty injections in one file",
            rationale="Related settings may drift in naming/defaults and be harder to validate as a unit.",
            remediation="Consider one cohesive Config Mapping; keep scalar injection when the settings are unrelated or migration risk is higher.",
            source_line=source_line_at(match.start()),
        )

    if ctx.virtual_threads and (ctx.java_release is None or ctx.java_release <= 23):
        match = re.search(r"\bsynchronized\b", sanitized)
        if match:
            add_finding(
                findings,
                rule_id="EJ-CON-006",
                severity="medium",
                confidence="low",
                category="virtual-threads",
                path=path,
                line=line_of(sanitized, match.start()),
                message="synchronized appears in a Java 21–23 virtual-thread context",
                rationale="Blocking while synchronized can pin a carrier on JDK 21–23; JDK 24 changes this behavior and native calls still need review.",
                remediation="Profile/trace actual pinning before replacing locks; use a runtime-specific remedy and keep critical sections small.",
                source_line=source_line_at(match.start()),
            )

    if re.search(r"\bsealed\s+(?:class|interface)\b", sanitized) and re.search(
        r"\bswitch\s*\([^)]*\)[^{]*\{[^}]*\bdefault\s*(?:->|:)", sanitized, re.DOTALL
    ):
        match = re.search(r"\bdefault\s*(?:->|:)", sanitized)
        assert match is not None
        add_finding(
            findings,
            rule_id="EJ-LANG-001",
            severity="medium",
            confidence="low",
            category="java-language",
            path=path,
            line=line_of(sanitized, match.start()),
            message="Default switch branch appears near a sealed hierarchy",
            rationale="A broad default can suppress compile-time exhaustiveness when new permitted variants are added; co-location is only a candidate.",
            remediation="Inspect the switched type; enumerate closed variants unless external/open values genuinely require a default.",
            source_line=source_line_at(match.start()),
        )

    for match in re.finditer(r"Collectors\.toMap\s*\(([^;\n]*)", sanitized):
        invocation = match.group(1)
        if invocation.count(",") <= 1:
            add_finding(
                findings,
                rule_id="EJ-COL-003",
                severity="medium",
                confidence="medium",
                category="collections",
                path=path,
                line=line_of(sanitized, match.start()),
                message="Two-argument toMap candidate lacks duplicate-key policy",
                rationale="Duplicate keys throw at runtime; commas in nested expressions can make this heuristic imprecise.",
                remediation="Define whether duplicates are impossible, should merge, or are an error; add a duplicate test.",
                source_line=source_line_at(match.start()),
            )

    if re.search(r"@(?:POST|jakarta\.ws\.rs\.POST)\b", sanitized) and re.search(
        r"@Retry\b", sanitized
    ):
        match = re.search(r"@Retry\b", sanitized)
        assert match is not None
        add_finding(
            findings,
            rule_id="EJ-FT-001",
            severity="high",
            confidence="low",
            category="fault-tolerance",
            path=path,
            line=line_of(sanitized, match.start()),
            message="Retry and POST coexist; idempotency must be proven",
            rationale="Retrying non-idempotent work can duplicate writes, payments, or messages; annotations may be on unrelated methods.",
            remediation="Trace annotation scope, bound attempts/deadline, and require an idempotency key or safe operation semantics.",
            source_line=source_line_at(match.start()),
        )


def scan_file(
    path: Path,
    root: Path,
    project_quarkus: bool,
    java_release: int | None,
    project_virtual: bool,
    line_rules: list[LineRule],
) -> list[Finding]:
    text = read_text(path)
    if not text:
        return []
    sanitized = sanitize_java(text)
    ctx = context_for(text, path, root, project_quarkus, java_release, project_virtual)
    rel_path = path.relative_to(root).as_posix()
    findings: list[Finding] = []
    original_lines = text.splitlines()
    sanitized_lines = sanitized.splitlines()
    for number, code_line in enumerate(sanitized_lines, start=1):
        original = original_lines[number - 1] if number <= len(original_lines) else code_line
        for rule in line_rules:
            if rule.condition(ctx) and rule.pattern.search(code_line):
                add_finding(
                    findings,
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    confidence=rule.confidence,
                    category=rule.category,
                    path=rel_path,
                    line=number,
                    message=rule.message,
                    rationale=rule.rationale,
                    remediation=rule.remediation,
                    source_line=original,
                )
    scan_cross_patterns(text, sanitized, rel_path, ctx, findings)
    return findings


def dedupe(findings: list[Finding]) -> list[Finding]:
    seen: set[tuple[str, str, int]] = set()
    result: list[Finding] = []
    for finding in findings:
        key = (finding.rule_id, finding.path, finding.line)
        if key not in seen:
            seen.add(key)
            result.append(finding)
    return result


def to_markdown(
    root: Path, findings: list[Finding], scanned: int, project: dict[str, object]
) -> str:
    counts = {level: 0 for level in ("critical", "high", "medium", "low")}
    for finding in findings:
        counts[finding.severity] += 1
    lines = [
        "# Effective Java Heuristic Risk Scan",
        "",
        "> Every item is a candidate for semantic review. A regex match is not proof of a defect.",
        "",
        f"- **Root:** `{root}`",
        f"- **Java files scanned:** {scanned}",
        f"- **Quarkus detected:** {'yes' if project['quarkus'] else 'no'}",
        f"- **Java release candidate:** {project['java_release'] or 'unknown'}",
        f"- **Findings:** {len(findings)} (critical {counts['critical']}, high {counts['high']}, medium {counts['medium']}, low {counts['low']})",
        "",
    ]
    if not findings:
        lines.append("No matches at the selected severity. This does not prove the code is defect-free.")
        return "\n".join(lines) + "\n"
    for index, finding in enumerate(findings, start=1):
        lines.extend(
            [
                f"## {index}. {finding.rule_id} — {finding.message}",
                "",
                f"- **Location:** `{finding.path}:{finding.line}`",
                f"- **Severity / confidence:** {finding.severity} / {finding.confidence}",
                f"- **Category:** {finding.category}",
                f"- **Excerpt:** `{finding.excerpt.replace('`', "'")}`",
                f"- **Why inspect:** {finding.rationale}",
                f"- **Next step:** {finding.remediation}",
                "",
            ]
        )
    return "\n".join(lines)


def to_json(
    root: Path, findings: list[Finding], scanned: int, project: dict[str, object]
) -> str:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "tool": "effective-java-risk-scanner",
        "root": str(root),
        "java_files_scanned": scanned,
        "project": project,
        "disclaimer": "Findings are heuristic candidates, not confirmed defects.",
        "findings": [asdict(item) for item in findings],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def to_sarif(findings: list[Finding]) -> str:
    rule_map: dict[str, Finding] = {}
    for item in findings:
        rule_map.setdefault(item.rule_id, item)
    sarif_levels = {"critical": "error", "high": "error", "medium": "warning", "low": "note"}
    payload = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "effective-java-risk-scanner",
                        "informationUri": "https://agentskills.io/",
                        "rules": [
                            {
                                "id": rule_id,
                                "shortDescription": {"text": sample.message},
                                "fullDescription": {"text": sample.rationale},
                                "help": {"text": sample.remediation},
                                "properties": {
                                    "category": sample.category,
                                    "confidence": sample.confidence,
                                    "heuristic": True,
                                },
                            }
                            for rule_id, sample in sorted(rule_map.items())
                        ],
                    }
                },
                "results": [
                    {
                        "ruleId": item.rule_id,
                        "level": sarif_levels[item.severity],
                        "message": {
                            "text": f"Heuristic candidate: {item.message}. {item.rationale}"
                        },
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {"uri": item.path},
                                    "region": {"startLine": item.line},
                                }
                            }
                        ],
                        "properties": {
                            "severity": item.severity,
                            "confidence": item.confidence,
                            "category": item.category,
                            "heuristic": True,
                            "remediation": item.remediation,
                        },
                    }
                    for item in findings
                ],
            }
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    project_quarkus, java_release, project_virtual = detect_project(root)
    line_rules = make_line_rules()
    findings: list[Finding] = []
    scanned = 0
    for path in iter_java_files(root):
        parts = {part.lower() for part in path.relative_to(root).parts}
        if args.exclude_tests and ("test" in parts or "tests" in parts):
            continue
        scanned += 1
        findings.extend(
            scan_file(
                path,
                root,
                project_quarkus,
                java_release,
                project_virtual,
                line_rules,
            )
        )
        if len(findings) > args.max_findings * 2:
            break
    findings = dedupe(findings)
    threshold = SEVERITY_ORDER[args.min_severity]
    findings = [item for item in findings if SEVERITY_ORDER[item.severity] >= threshold]
    findings.sort(
        key=lambda item: (-SEVERITY_ORDER[item.severity], item.path, item.line, item.rule_id)
    )
    truncated = len(findings) > args.max_findings
    findings = findings[: args.max_findings]
    project = {
        "quarkus": project_quarkus,
        "java_release": java_release,
        "virtual_thread_tokens": project_virtual,
        "truncated": truncated,
    }
    if args.format == "json":
        rendered = to_json(root, findings, scanned, project)
    elif args.format == "sarif":
        rendered = to_sarif(findings)
    else:
        rendered = to_markdown(root, findings, scanned, project)
        if truncated:
            rendered += f"\n> Output truncated to --max-findings={args.max_findings}.\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    if args.fail_on != "none":
        fail_level = SEVERITY_ORDER[args.fail_on]
        if any(SEVERITY_ORDER[item.severity] >= fail_level for item in findings):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
