#!/usr/bin/env python3
"""Validate skills in this repository using the skill-creator quick checks."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
}


def parse_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        raise ValueError("No YAML frontmatter found")

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("Invalid frontmatter format")

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML in frontmatter: {error}") from error

    if not isinstance(frontmatter, dict):
        raise ValueError("Frontmatter must be a YAML dictionary")

    return frontmatter


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    try:
        frontmatter = parse_frontmatter(skill_md.read_text())
    except ValueError as error:
        return False, str(error)

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_KEYS
    if unexpected_keys:
        allowed = ", ".join(sorted(ALLOWED_FRONTMATTER_KEYS))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            "Unexpected key(s) in SKILL.md frontmatter: "
            f"{unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"

    name = name.strip()
    if not re.match(r"^[a-z0-9-]+$", name):
        return (
            False,
            f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
        )
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return (
            False,
            f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
        )
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return (
            False,
            f"Name is too long ({len(name)} characters). Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
        )

    description = frontmatter.get("description")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"

    description = description.strip()
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return (
            False,
            f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
        )

    return True, "Skill is valid!"


def iter_skill_paths(skills_root: Path) -> list[Path]:
    return sorted(path for path in skills_root.iterdir() if path.is_dir())


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    skills_root = repo_root / "skills"

    if len(sys.argv) > 1:
        skill_paths = [Path(arg).resolve() for arg in sys.argv[1:]]
    else:
        skill_paths = iter_skill_paths(skills_root)

    failures: list[tuple[str, str]] = []
    for skill_path in skill_paths:
        valid, message = validate_skill(skill_path)
        skill_name = skill_path.name
        if valid:
            print(f"[OK] {skill_name}: {message}")
            continue

        print(f"[FAIL] {skill_name}: {message}", file=sys.stderr)
        failures.append((skill_name, message))

    if failures:
        print(
            f"\nSkill validation failed for {len(failures)} skill(s).",
            file=sys.stderr,
        )
        return 1

    print(f"\nValidated {len(skill_paths)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
