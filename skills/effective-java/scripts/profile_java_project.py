#!/usr/bin/env python3
"""Profile a Java/Quarkus repository without modifying it.

The output is evidence for an agent, not a substitute for effective build-tool
configuration. The script uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0.0"
SKIP_DIRS = {
    ".git",
    ".gradle",
    ".idea",
    ".mvn/wrapper",
    ".settings",
    ".vscode",
    "node_modules",
    "target",
    "build",
    "out",
    "dist",
    "vendor",
    "coverage",
    ".cache",
    ".quarkus",
}
MAX_TEXT_BYTES = 2_000_000

QUALITY_TOKENS = {
    "spotless": "Spotless",
    "checkstyle": "Checkstyle",
    "spotbugs": "SpotBugs",
    "pmd": "PMD",
    "error_prone": "Error Prone",
    "errorprone": "Error Prone",
    "jacoco": "JaCoCo",
    "pitest": "PIT",
    "archunit": "ArchUnit",
    "sonarqube": "SonarQube",
    "sonar-maven-plugin": "SonarQube",
    "revapi": "Revapi",
    "japicmp": "japicmp",
    "nullaway": "NullAway",
    "forbiddenapis": "Forbidden APIs",
}

CONFIG_NAMES = {
    "application.properties",
    "application.yml",
    "application.yaml",
    "microprofile-config.properties",
    "logback.xml",
    "log4j2.xml",
    "beans.xml",
    "persistence.xml",
    "module-info.java",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument(
        "--format", choices=("markdown", "json"), default="markdown"
    )
    parser.add_argument("--output", type=Path, help="write output to this file")
    parser.add_argument(
        "--max-files",
        type=int,
        default=50_000,
        help="safety limit for traversed files (default: 50000)",
    )
    return parser.parse_args()


def is_skipped(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    for idx, part in enumerate(parts):
        candidate = "/".join(parts[: idx + 1])
        if part in SKIP_DIRS or candidate in SKIP_DIRS:
            return True
    return False


def iter_files(root: Path, max_files: int) -> Iterable[Path]:
    count = 0
    for current, dirnames, filenames in os.walk(root):
        current_path = Path(current)
        dirnames[:] = [
            name
            for name in dirnames
            if not is_skipped(current_path / name, root)
        ]
        for name in filenames:
            path = current_path / name
            if is_skipped(path, root):
                continue
            count += 1
            if count > max_files:
                raise RuntimeError(
                    f"file traversal exceeded --max-files={max_files}; narrow the root"
                )
            yield path


def read_text(path: Path) -> str:
    try:
        if path.stat().st_size > MAX_TEXT_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def strip_xml_namespace(tag: str) -> str:
    return tag.split("}", 1)[-1]


def xml_children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element.iter() if strip_xml_namespace(child.tag) == name]


def xml_text(element: ET.Element | None) -> str | None:
    if element is None or element.text is None:
        return None
    value = element.text.strip()
    return value or None


def first_child_text(parent: ET.Element, name: str) -> str | None:
    for child in parent:
        if strip_xml_namespace(child.tag) == name:
            return xml_text(child)
    return None


def parse_pom(path: Path, root: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": rel(path, root),
        "modules": [],
        "java_candidates": [],
        "quarkus_versions": [],
        "quarkus_extensions": [],
        "quality_tools": [],
        "preview": False,
    }
    text = read_text(path)
    if not text:
        result["warning"] = "could not read POM"
        return result
    result["preview"] = "--enable-preview" in text
    lowered = text.lower()
    for token, label in QUALITY_TOKENS.items():
        if token in lowered:
            result["quality_tools"].append(label)
    try:
        project = ET.fromstring(text)
    except ET.ParseError as exc:
        result["warning"] = f"XML parse error: {exc}"
        return result

    properties: dict[str, str] = {}
    for props in xml_children(project, "properties"):
        for child in props:
            value = xml_text(child)
            if value:
                properties[strip_xml_namespace(child.tag)] = value

    java_property_names = (
        "maven.compiler.release",
        "maven.compiler.source",
        "maven.compiler.target",
        "java.version",
        "jdk.version",
        "java.release",
    )
    for name in java_property_names:
        if name in properties:
            result["java_candidates"].append(f"{name}={properties[name]}")

    for release in xml_children(project, "release"):
        value = xml_text(release)
        if value:
            result["java_candidates"].append(f"plugin.release={value}")
    for source in xml_children(project, "source"):
        value = xml_text(source)
        if value and re.fullmatch(r"(?:1\.)?\d+|\$\{[^}]+\}", value):
            result["java_candidates"].append(f"plugin.source={value}")
    for target in xml_children(project, "target"):
        value = xml_text(target)
        if value and re.fullmatch(r"(?:1\.)?\d+|\$\{[^}]+\}", value):
            result["java_candidates"].append(f"plugin.target={value}")

    for module_parent in xml_children(project, "modules"):
        for module in module_parent:
            if strip_xml_namespace(module.tag) == "module":
                value = xml_text(module)
                if value:
                    result["modules"].append(value)

    for name, value in properties.items():
        lowered_name = name.lower()
        if "quarkus" in lowered_name and "version" in lowered_name:
            result["quarkus_versions"].append(f"{name}={value}")

    for dependency in xml_children(project, "dependency"):
        group = first_child_text(dependency, "groupId")
        artifact = first_child_text(dependency, "artifactId")
        version = first_child_text(dependency, "version")
        dep_type = first_child_text(dependency, "type")
        scope = first_child_text(dependency, "scope")
        if group and artifact and group.startswith("io.quarkus"):
            coordinate = f"{group}:{artifact}"
            if artifact.startswith("quarkus-") and "bom" not in artifact:
                result["quarkus_extensions"].append(coordinate)
            if "bom" in artifact and version:
                result["quarkus_versions"].append(
                    f"{coordinate}={version} ({scope or dep_type or 'dependency'})"
                )

    for plugin in xml_children(project, "plugin"):
        group = first_child_text(plugin, "groupId") or "org.apache.maven.plugins"
        artifact = first_child_text(plugin, "artifactId")
        version = first_child_text(plugin, "version")
        if artifact == "quarkus-maven-plugin":
            result["quarkus_versions"].append(
                f"{group}:{artifact}={version or '(managed/property)'}"
            )

    for key in (
        "modules",
        "java_candidates",
        "quarkus_versions",
        "quarkus_extensions",
        "quality_tools",
    ):
        result[key] = sorted(set(result[key]))
    return result


def parse_gradle(path: Path, root: Path) -> dict[str, Any]:
    text = read_text(path)
    result: dict[str, Any] = {
        "path": rel(path, root),
        "java_candidates": [],
        "quarkus_versions": [],
        "quarkus_extensions": [],
        "quality_tools": [],
        "preview": "--enable-preview" in text,
    }
    lowered = text.lower()
    for token, label in QUALITY_TOKENS.items():
        if token in lowered:
            result["quality_tools"].append(label)

    java_patterns = {
        "sourceCompatibility": r"sourceCompatibility\s*=\s*['\"]?([^'\"\s}]+)",
        "targetCompatibility": r"targetCompatibility\s*=\s*['\"]?([^'\"\s}]+)",
        "languageVersion": r"JavaLanguageVersion\.of\s*\(\s*([^\)]+)\)",
        "options.release": r"options\.release(?:\.set)?\s*\(?\s*([^\)\n]+)",
    }
    for label, pattern in java_patterns.items():
        for match in re.finditer(pattern, text):
            value = match.group(1).strip().rstrip(")")
            if len(value) < 100:
                result["java_candidates"].append(f"{label}={value}")

    for match in re.finditer(
        r"id\s*\(?\s*['\"]io\.quarkus['\"]\s*\)?(?:\s*version\s*['\"]([^'\"]+)['\"])?",
        text,
    ):
        result["quarkus_versions"].append(
            f"io.quarkus plugin={match.group(1) or '(property/managed)'}"
        )
    for match in re.finditer(
        r"['\"]((?:io\.quarkus(?:\.platform)?):([^:'\"]+)(?::([^'\"]+))?)['\"]",
        text,
    ):
        coordinate, artifact, version = match.groups()
        if artifact.startswith("quarkus-") and "bom" not in artifact:
            result["quarkus_extensions"].append(
                ":".join(coordinate.split(":")[:2])
            )
        if "bom" in artifact and version:
            result["quarkus_versions"].append(f"{coordinate}")

    for key in (
        "java_candidates",
        "quarkus_versions",
        "quarkus_extensions",
        "quality_tools",
    ):
        result[key] = sorted(set(result[key]))
    return result


def extract_gradle_modules(settings_files: list[Path], root: Path) -> list[str]:
    modules: set[str] = set()
    for path in settings_files:
        text = read_text(path)
        for match in re.finditer(r"\binclude\s*\(?([^\n]+)", text):
            for value in re.findall(r"['\"]([^'\"]+)['\"]", match.group(1)):
                modules.add(value.lstrip(":"))
    return sorted(modules)


def detect_generated_paths(root: Path) -> list[str]:
    candidates = (
        "target/generated-sources",
        "target/generated-test-sources",
        "build/generated",
        "src/generated",
        "src/main/generated",
        "generated-sources",
    )
    return [name for name in candidates if (root / name).exists()]


def count_sources(files: list[Path], root: Path) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for path in files:
        suffix = path.suffix.lower()
        parts = set(path.relative_to(root).parts)
        if suffix == ".java":
            if "test" in parts or "tests" in parts:
                counts["java_test"] += 1
            else:
                counts["java_main"] += 1
        elif suffix == ".kt":
            if "test" in parts or "tests" in parts:
                counts["kotlin_test"] += 1
            else:
                counts["kotlin_main"] += 1
        elif suffix in {".properties", ".yml", ".yaml"}:
            counts["configuration"] += 1
        elif suffix in {".sql", ".xml"} and (
            "migration" in "/".join(path.relative_to(root).parts).lower()
            or "db" in parts
        ):
            counts["migration_or_db"] += 1
    return dict(sorted(counts.items()))


def profile(root: Path, max_files: int) -> dict[str, Any]:
    files = list(iter_files(root, max_files))
    poms = sorted(path for path in files if path.name == "pom.xml")
    gradle_builds = sorted(
        path for path in files if path.name in {"build.gradle", "build.gradle.kts"}
    )
    settings = sorted(
        path for path in files if path.name in {"settings.gradle", "settings.gradle.kts"}
    )

    build_systems: list[str] = []
    if poms:
        build_systems.append("maven")
    if gradle_builds:
        build_systems.append("gradle")

    wrappers: list[str] = []
    for name in ("mvnw", "mvnw.cmd", "gradlew", "gradlew.bat"):
        if (root / name).exists():
            wrappers.append(name)

    pom_profiles = [parse_pom(path, root) for path in poms]
    gradle_profiles = [parse_gradle(path, root) for path in gradle_builds]

    modules: set[str] = set(extract_gradle_modules(settings, root))
    for item in pom_profiles:
        parent = Path(item["path"]).parent
        for module in item["modules"]:
            modules.add((parent / module).as_posix().lstrip("./"))

    java_candidates = sorted(
        {
            value
            for item in pom_profiles + gradle_profiles
            for value in item["java_candidates"]
        }
    )
    quarkus_versions = sorted(
        {
            value
            for item in pom_profiles + gradle_profiles
            for value in item["quarkus_versions"]
        }
    )
    quarkus_extensions = sorted(
        {
            value
            for item in pom_profiles + gradle_profiles
            for value in item["quarkus_extensions"]
        }
    )
    quality_tools = sorted(
        {
            value
            for item in pom_profiles + gradle_profiles
            for value in item["quality_tools"]
        }
    )
    preview = any(item["preview"] for item in pom_profiles + gradle_profiles)

    config_files = sorted(
        rel(path, root)
        for path in files
        if path.name in CONFIG_NAMES
        or (
            path.suffix.lower() in {".properties", ".yml", ".yaml"}
            and "application" in path.name
        )
    )
    toolchain_files = sorted(
        rel(path, root)
        for path in files
        if path.name
        in {
            "toolchains.xml",
            "gradle.properties",
            "libs.versions.toml",
            "jvm.config",
            ".java-version",
            ".sdkmanrc",
        }
    )

    signals: list[str] = []
    if quarkus_versions or quarkus_extensions:
        signals.append("Quarkus build metadata detected")
    joined_extensions = " ".join(quarkus_extensions)
    extension_signals = {
        "hibernate-reactive": "Hibernate Reactive detected",
        "hibernate-orm": "Hibernate ORM detected",
        "rest-client": "Quarkus REST Client detected",
        "quarkus-rest": "Quarkus REST detected",
        "smallrye-reactive-messaging": "Reactive Messaging detected",
        "oidc": "OIDC/security extension detected",
        "opentelemetry": "OpenTelemetry extension detected",
        "smallrye-health": "Health extension detected",
        "scheduler": "Scheduler extension detected",
    }
    for token, message in extension_signals.items():
        if token in joined_extensions:
            signals.append(message)
    if preview:
        signals.append("Java preview flag detected")
    if any("native" in read_text(path).lower() for path in poms + gradle_builds):
        signals.append("Native build configuration token detected")

    java_files = [path for path in files if path.suffix == ".java"]
    javax_count = 0
    jakarta_count = 0
    for path in java_files:
        text = read_text(path)
        javax_count += len(re.findall(r"^\s*import\s+javax\.", text, re.MULTILINE))
        jakarta_count += len(re.findall(r"^\s*import\s+jakarta\.", text, re.MULTILINE))
    if javax_count:
        signals.append(f"javax imports: {javax_count}")
    if jakarta_count:
        signals.append(f"jakarta imports: {jakarta_count}")

    warnings: list[str] = []
    if not build_systems:
        warnings.append("No pom.xml or Gradle build file found under the selected root")
    if "maven" in build_systems and not any(name.startswith("mvnw") for name in wrappers):
        warnings.append("Maven build detected without a checked-in Maven wrapper")
    if "gradle" in build_systems and not any(name.startswith("gradlew") for name in wrappers):
        warnings.append("Gradle build detected without a checked-in Gradle wrapper")
    normalized_releases = {
        match.group(1)
        for value in java_candidates
        if (match := re.search(r"(?<!\d)(\d{1,2})(?!\d)", value))
    }
    if len(normalized_releases) > 1:
        warnings.append(
            "Multiple Java release candidates were found; inspect effective configuration: "
            + ", ".join(java_candidates)
        )
    if javax_count and jakarta_count and (quarkus_versions or quarkus_extensions):
        warnings.append(
            "Both javax and jakarta imports occur in a Quarkus project; this may be intentional migration/legacy code"
        )
    for item in pom_profiles + gradle_profiles:
        if "warning" in item:
            warnings.append(f"{item['path']}: {item['warning']}")

    return {
        "schema_version": SCHEMA_VERSION,
        "root": str(root),
        "build_systems": build_systems,
        "wrappers": sorted(wrappers),
        "build_files": [rel(path, root) for path in poms + gradle_builds + settings],
        "modules": sorted(modules),
        "java": {
            "release_candidates": java_candidates,
            "toolchain_files": toolchain_files,
            "preview_enabled": preview,
        },
        "quarkus": {
            "detected": bool(quarkus_versions or quarkus_extensions),
            "version_candidates": quarkus_versions,
            "extensions": quarkus_extensions,
        },
        "source_counts": count_sources(files, root),
        "quality_tools": quality_tools,
        "generated_paths": detect_generated_paths(root),
        "config_files": config_files,
        "signals": sorted(set(signals)),
        "warnings": warnings,
    }


def bullets(values: list[str], empty: str = "None detected") -> str:
    if not values:
        return f"- {empty}"
    return "\n".join(f"- `{value}`" for value in values)


def to_markdown(data: dict[str, Any]) -> str:
    q = data["quarkus"]
    j = data["java"]
    counts = data["source_counts"]
    lines = [
        "# Java Project Profile",
        "",
        f"- **Root:** `{data['root']}`",
        f"- **Build systems:** {', '.join(data['build_systems']) or 'none detected'}",
        f"- **Wrappers:** {', '.join(f'`{x}`' for x in data['wrappers']) or 'none detected'}",
        f"- **Quarkus detected:** {'yes' if q['detected'] else 'no'}",
        f"- **Preview enabled token:** {'yes' if j['preview_enabled'] else 'no'}",
        "",
        "## Source counts",
        "",
        "| Kind | Count |",
        "|---|---:|",
    ]
    if counts:
        lines.extend(f"| {key} | {value} |" for key, value in counts.items())
    else:
        lines.append("| no recognized sources | 0 |")
    lines.extend(
        [
            "",
            "## Java release/toolchain candidates",
            "",
            bullets(j["release_candidates"], "No explicit release candidate detected"),
            "",
            "### Toolchain-related files",
            "",
            bullets(j["toolchain_files"]),
            "",
            "## Quarkus version candidates",
            "",
            bullets(q["version_candidates"], "No Quarkus version candidate detected"),
            "",
            "## Quarkus extensions",
            "",
            bullets(q["extensions"], "No Quarkus extension detected"),
            "",
            "## Modules",
            "",
            bullets(data["modules"], "No declared modules detected"),
            "",
            "## Quality tools",
            "",
            bullets(data["quality_tools"]),
            "",
            "## Generated paths",
            "",
            bullets(data["generated_paths"]),
            "",
            "## Configuration files",
            "",
            bullets(data["config_files"]),
            "",
            "## Signals",
            "",
            bullets(data["signals"]),
            "",
            "## Warnings and manual checks",
            "",
            bullets(data["warnings"], "No profiler warning"),
            "",
            "> Values are static candidates. Confirm effective Maven/Gradle configuration and runtime deployment before editing.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    try:
        data = profile(root, args.max_files)
    except (OSError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    rendered = (
        json.dumps(data, indent=2, sort_keys=True) + "\n"
        if args.format == "json"
        else to_markdown(data)
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
