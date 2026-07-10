#!/usr/bin/env python3
"""Create or verify the portable bundle's SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

MANIFEST = "BUNDLE-MANIFEST.txt"
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
SKIP_SUFFIXES = {".pyc", ".class", ".jar", ".zip"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="skill root")
    parser.add_argument("--check", action="store_true", help="verify instead of writing")
    return parser.parse_args()


def included_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if not path.is_file() or path.is_symlink():
            continue
        if relative.as_posix() == MANIFEST or path.suffix in SKIP_SUFFIXES:
            continue
        files.append(path)
    return sorted(files, key=lambda value: value.relative_to(root).as_posix())


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def render(root: Path) -> str:
    lines = [
        "# Effective Java Bundle Manifest",
        "# sha256  bytes  path",
        "# BUNDLE-MANIFEST.txt is intentionally excluded to avoid a self-hash.",
    ]
    for path in included_files(root):
        relative = path.relative_to(root).as_posix()
        lines.append(f"{digest(path)}  {path.stat().st_size}  {relative}")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    expected = render(root)
    manifest = root / MANIFEST
    if args.check:
        if not manifest.is_file():
            print(f"error: missing {MANIFEST}", file=sys.stderr)
            return 1
        actual = manifest.read_text(encoding="utf-8")
        if actual != expected:
            print(f"error: {MANIFEST} is stale; run scripts/build_manifest.py .", file=sys.stderr)
            return 1
        print(f"OK: {MANIFEST} covers {len(included_files(root))} files")
        return 0
    temporary = manifest.with_suffix(".tmp")
    temporary.write_text(expected, encoding="utf-8")
    temporary.replace(manifest)
    print(f"WROTE: {MANIFEST} with {len(included_files(root))} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
