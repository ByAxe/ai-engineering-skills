# Migration from the Legacy Java Skills

## Replaced skills

Delete these directories after reviewing the replacement:

- `skills/java-refactoring`
- `skills/java-21-refactor-assessor`

Install this bundle as:

- `skills/effective-java`

The new skill subsumes general smell detection, SOLID-aware refactoring, Java 21 modernization, Python-shaped Java cleanup, testing, and build validation. It adds agent-specific failure controls, executable diagnostics, API and semantic compatibility checks, security, concurrency, persistence, and a full Quarkus reference pack.

## Automated replacement

Dry run:

```bash
skills/effective-java/migration/replace-legacy-skills.sh --repo .
```

Apply from an unpacked bundle that is not already inside the destination:

```bash
/path/to/effective-java/migration/replace-legacy-skills.sh --repo . --apply
```

The script refuses to overwrite an existing non-identical `skills/effective-java` unless `--force` is supplied. It creates a timestamped backup under `.effective-java-migration-backup/` before deleting legacy directories.

## README changes

Replace the two Java rows with the snippet in `migration/README-java-section.md`. The migration script handles the known current README wording and reports when a manual edit is needed.

## Validation

```bash
./scripts/run_skill_validation.sh skills/effective-java
python3 skills/effective-java/scripts/validate_skill.py skills/effective-java
```

Also run `skills-ref validate`, `tessl skill lint`, `tessl skill review`, and scenario evals when those external CLIs are available.

## Activation migration

Prompts that previously named either old skill should use `$effective-java`. The description intentionally includes refactor, assess, Java 21, modernization, Maven, Gradle, and Quarkus trigger terms while excluding Kotlin-only, Android, and non-Java work.
