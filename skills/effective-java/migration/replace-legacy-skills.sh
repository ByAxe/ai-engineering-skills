#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: replace-legacy-skills.sh --repo PATH [--apply] [--force]

Dry-run is the default. On --apply the script:
  1. copies this bundle to skills/effective-java (unless already there)
  2. removes skills/java-21-refactor-assessor and skills/java-refactoring
  3. replaces their README catalog rows with one effective-java row
  4. runs the repository skill validator when available

--force permits a dirty Git worktree and replacement of an existing destination.
Review the resulting Git diff before committing.
EOF
}

repo=""
apply=false
force=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      [[ $# -ge 2 ]] || { echo "error: --repo requires a value" >&2; exit 2; }
      repo="$2"; shift 2 ;;
    --apply)
      apply=true; shift ;;
    --force)
      force=true; shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 2 ;;
  esac
done

[[ -n "$repo" ]] || { echo "error: --repo is required" >&2; usage >&2; exit 2; }
repo="$(cd "$repo" 2>/dev/null && pwd)" || { echo "error: repository path is invalid" >&2; exit 2; }
[[ -d "$repo/skills" && -f "$repo/README.md" ]] || {
  echo "error: expected a repository with skills/ and README.md: $repo" >&2
  exit 2
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_skill="$(cd "$script_dir/.." && pwd)"
destination="$repo/skills/effective-java"
legacy_one="$repo/skills/java-21-refactor-assessor"
legacy_two="$repo/skills/java-refactoring"

if [[ ! -f "$source_skill/SKILL.md" || ! -f "$source_skill/tile.json" ]]; then
  echo "error: source bundle is incomplete: $source_skill" >&2
  exit 2
fi

same_location=false
if [[ -e "$destination" ]]; then
  destination_real="$(cd "$destination" && pwd)"
  [[ "$destination_real" == "$source_skill" ]] && same_location=true
fi

if $apply && command -v git >/dev/null 2>&1 && git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if [[ -n "$(git -C "$repo" status --porcelain)" ]] && ! $force; then
    echo "error: Git worktree is not clean; commit/stash changes or pass --force" >&2
    exit 2
  fi
fi

cat <<EOF
Effective Java migration
  repository: $repo
  source:     $source_skill
  destination:$destination
  mode:       $($apply && echo apply || echo dry-run)

Planned actions:
EOF
if $same_location; then
  echo "  - keep existing skills/effective-java source in place"
elif [[ -e "$destination" ]]; then
  if $force; then
    echo "  - replace existing skills/effective-java"
  else
    echo "  - ERROR: destination exists (pass --force to replace)"
    exit 2
  fi
else
  echo "  - copy bundle to skills/effective-java"
fi
[[ -d "$legacy_one" ]] && echo "  - remove skills/java-21-refactor-assessor" || echo "  - legacy java-21-refactor-assessor already absent"
[[ -d "$legacy_two" ]] && echo "  - remove skills/java-refactoring" || echo "  - legacy java-refactoring already absent"
echo "  - update README catalog/tree references"
echo "  - run standalone and repository validators when available"

if ! $apply; then
  echo
  echo "Dry-run only. Re-run with --apply after reviewing these actions."
  exit 0
fi

backup_root="$repo/.effective-java-migration-backup/$(date -u +%Y%m%dT%H%M%SZ)"
backup_created=false
for backup_source in "$legacy_one" "$legacy_two"; do
  if [[ -d "$backup_source" ]]; then
    mkdir -p "$backup_root"
    cp -a "$backup_source" "$backup_root/"
    backup_created=true
  fi
done
if ! $same_location && [[ -e "$destination" ]]; then
  mkdir -p "$backup_root"
  cp -a "$destination" "$backup_root/effective-java-existing"
  backup_created=true
fi
$backup_created && echo "Backup created: $backup_root"

if ! $same_location; then
  if [[ -e "$destination" ]]; then
    rm -rf "$destination"
  fi
  mkdir -p "$destination"
  # Copy ordinary and dot files without requiring rsync. The bundle validator
  # rejects VCS/cache directories, so a direct archival copy is safe here.
  cp -a "$source_skill"/. "$destination"/
fi

rm -rf "$legacy_one" "$legacy_two"

python3 - "$repo/README.md" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
lines = path.read_text(encoding="utf-8").splitlines()
legacy = re.compile(r"java-(?:21-refactor-assessor|refactoring)")
catalog_row = "| **effective-java** | Evidence-first Java 21 and Quarkus implementation, review, debugging, refactoring, modernization, testing, security, performance, and native-readiness |"

# Replace the Java catalog rows while preserving unrelated tables and prose.
rewritten: list[str] = []
catalog_inserted = False
for line in lines:
    if line.lstrip().startswith("|") and legacy.search(line):
        if not catalog_inserted:
            rewritten.append(catalog_row)
            catalog_inserted = True
        continue
    replaced = line.replace("java-21-refactor-assessor", "effective-java")
    replaced = replaced.replace("java-refactoring", "effective-java")
    replaced = replaced.replace("effective-java and effective-java", "effective-java")
    rewritten.append(replaced)

# If the legacy rows were already absent, insert into the Java catalog table,
# not the first unrelated table in the README.
if not catalog_inserted:
    java_heading = next(
        (index for index, line in enumerate(rewritten) if line.strip() == "### Java"),
        None,
    )
    insertion = None
    if java_heading is not None:
        for index in range(java_heading + 1, min(len(rewritten) - 1, java_heading + 12)):
            if rewritten[index].lstrip().startswith("|") and re.match(
                r"^\s*\|\s*:?-+", rewritten[index + 1]
            ):
                insertion = index + 2
                break
    if insertion is not None:
        rewritten.insert(insertion, catalog_row)
    else:
        rewritten.extend(["", "## Effective Java skill", "", catalog_row])

# Replace the complete Java tree subsection. Removing only the two root lines
# would leave their old child entries behind and corrupt the README tree.
java_tree = next(
    (index for index, line in enumerate(rewritten) if line.strip() in {"│ # Java", "# Java"}),
    None,
)
kotlin_tree = None
if java_tree is not None:
    kotlin_tree = next(
        (
            index
            for index in range(java_tree + 1, len(rewritten))
            if "# Kotlin / JVM" in rewritten[index]
        ),
        None,
    )
if java_tree is not None and kotlin_tree is not None:
    tree_block = [
        rewritten[java_tree],
        "├── effective-java/",
        "│   ├── SKILL.md",
        "│   ├── agents/",
        "│   ├── references/    (focused Java and Quarkus guidance)",
        "│   ├── scripts/       (profiling, risk, diff, gates, validation)",
        "│   ├── assets/        (assessment, plan, implementation templates)",
        "│   ├── schemas/",
        "│   ├── examples/",
        "│   ├── evals/         (activation, Agent Skills, Tessl scenarios)",
        "│   ├── tests/",
        "│   └── migration/",
        "│",
    ]
    rewritten = rewritten[:java_tree] + tree_block + rewritten[kotlin_tree:]

# Make repeated migrations idempotent for the catalog row.
deduped: list[str] = []
seen_catalog = False
for line in rewritten:
    if line == catalog_row:
        if seen_catalog:
            continue
        seen_catalog = True
    deduped.append(line)

path.write_text("\n".join(deduped) + "\n", encoding="utf-8")
PY

python3 "$destination/scripts/validate_skill.py" "$destination"
if [[ -x "$repo/scripts/run_skill_validation.sh" ]]; then
  "$repo/scripts/run_skill_validation.sh" "$destination"
elif [[ -f "$repo/scripts/validate_skills.py" ]]; then
  python3 "$repo/scripts/validate_skills.py" "$destination"
fi

echo
echo "Migration applied. Review:"
echo "  git -C '$repo' status --short"
echo "  git -C '$repo' diff -- README.md skills/"
