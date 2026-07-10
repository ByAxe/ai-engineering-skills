# Effective Java Bundle Map

Use this page for maintainers of the skill. Agents should normally start with `SKILL.md` and follow `references/00-reference-router.md`.

## Runtime surfaces

- `SKILL.md` — activation metadata and the always-loaded workflow
- `references/` — focused knowledge loaded only when a trigger applies
- `scripts/` — deterministic project inspection and verification helpers
- `assets/` — assessment, plan, and implementation output contracts
- `schemas/` — interoperable JSON structures for project profiles and findings
- `examples/` — compact before/after patterns, not universal recipes

## Quality surfaces

- `evals/evals.json` — Agent Skills output-quality prompts and assertions
- `evals/activation.json` — trigger and near-miss prompt set
- numbered Tessl weighted scenario directories under `evals/`
- `tests/` — executable tests for bundled scripts
- `references/source-index.md` — source provenance and update checklist
- `VALIDATION.md` — checks actually run and external gates explicitly not claimed
- `BUNDLE-MANIFEST.txt` — SHA-256 and byte-size inventory for portable payload files

## Distribution surfaces

- `tile.json` — Tessl manifest; change `byaxe` if the publishing workspace differs
- `agents/openai.yaml` — OpenAI agent presentation metadata
- `migration/` — safe replacement of the two legacy Java skills
- `scripts/build_manifest.py` — deterministic manifest regeneration and verification
- `MIGRATION.md` and `CHANGELOG.md` — lifecycle documentation

## Design constraints

The main skill stays below 500 lines and routes to one-level-deep references. Detailed rules live outside `SKILL.md`; repeated mechanical work lives in tested scripts. Version-sensitive guidance instructs the agent to inspect the target project rather than assuming the documentation site’s current release.
