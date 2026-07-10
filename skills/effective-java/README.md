# Effective Java Agent Skill

A production-oriented Agent Skills bundle for implementing, debugging, reviewing, refactoring, modernizing, and validating Java and Quarkus repositories. It replaces the narrower `java-refactoring` and `java-21-refactor-assessor` skills in `ByAxe/ai-engineering-skills`.

## What is included

- a concise, activation-focused `SKILL.md`
- focused on-demand Java and Quarkus references
- repository profiling, heuristic risk scanning, diff-scope, quality-gate, and bundle-validation scripts
- output templates and machine-readable schemas
- Agent Skills output evals, activation evals, and Tessl scenario evals
- executable unit tests and a representative Java 21 + Quarkus fixture
- migration tooling and a legacy coverage map
- a SHA-256 payload manifest and explicit validation record

The skill defaults to Java 21 concepts but never overrides the release configured by the target repository. It does not require Quarkus; Quarkus guidance activates only when the project or task uses it.

## Install in this repository

From the root of a clone of `ByAxe/ai-engineering-skills`:

```bash
unzip effective-java-skill-bundle.zip -d /tmp/effective-java-bundle
/tmp/effective-java-bundle/effective-java/migration/replace-legacy-skills.sh --repo . --apply
./scripts/run_skill_validation.sh skills/effective-java
```

The migration script is dry-run by default. It removes only the two legacy skill directories, copies this bundle to `skills/effective-java`, and updates the known README entries. Review the diff before committing.

## Validate standalone

```bash
python3 scripts/validate_skill.py . --strict-warnings
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/build_manifest.py . --check
```

When installed:

```bash
skills-ref validate ./effective-java
# Set tile.json name to a Tessl workspace you can publish to first.
tessl skill lint ./effective-java
tessl skill review ./effective-java
# Tessl finds scenario evals beside tile.json.
tessl eval run ./effective-java/tile.json
```

`skills-ref` and Tessl are external tools and are not bundled.

## Use with an agent

Typical prompts:

- “Use `$effective-java` to review this Java 21 service for semantic and maintainability risks.”
- “Use `$effective-java` to refactor this Quarkus resource without changing its HTTP or transaction behavior.”
- “Use `$effective-java` to implement this feature and run the repository’s relevant Maven gates.”
- “Use `$effective-java` to assess whether virtual threads are appropriate for this Quarkus path.”

See `docs/index.md` for the bundle map, `VALIDATION.md` for executed and deferred checks, and `MIGRATION.md` for replacement details.
