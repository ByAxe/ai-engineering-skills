# Suggested repository README entry

Use one catalog row in place of the two legacy Java skills:

```markdown
| **effective-java** | Evidence-first Java 21 and Quarkus implementation, review, debugging, refactoring, modernization, testing, security, performance, and native-readiness |
```

Suggested structure entry:

```text
│ # Java
├── effective-java/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   ├── scripts/
│   ├── assets/
│   ├── schemas/
│   ├── examples/
│   ├── evals/
│   ├── tests/
│   └── migration/
```

Suggested installation/validation examples:

```bash
npx skills add ByAxe/ai-engineering-skills --skill effective-java
./scripts/run_skill_validation.sh skills/effective-java
python3 skills/effective-java/scripts/validate_skill.py skills/effective-java --strict-warnings
python3 skills/effective-java/scripts/build_manifest.py skills/effective-java --check
```

For Tessl, change `tile.json`’s workspace prefix if `byaxe` is not the publishing workspace, then run the repository’s current Tessl lint/review/eval commands.
