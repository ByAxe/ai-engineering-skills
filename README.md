# AI Engineering Skills

Custom Claude Code skills for software engineering workflows.

## Installation

```bash
npx skills add ByAxe/ai-engineering-skills
```

Install globally (available in all projects):

```bash
npx skills add ByAxe/ai-engineering-skills -g
```

Install a specific skill:

```bash
npx skills add ByAxe/ai-engineering-skills --skill reflect
```

## Validation

This repo includes a repo-managed pre-commit hook that validates all skills with the same quick checks used from `skill-creator`.

Enable the hook path once per clone:

```bash
git config core.hooksPath .githooks
```

Run the validator manually:

```bash
./scripts/run_skill_validation.sh
```

## Skills

### Flutter

| Skill | Description |
|---|---|
| **figma-to-flutter** | Converts Figma designs to pixel-perfect Flutter code using figma-console-mcp. Extracts design metadata, exports assets, implements UI, and iteratively validates. Uses live Desktop Bridge tools when REST-backed Figma calls hit `403 Token expired`. |
| **flutter-cleanup-assessor** | Assesses and refactors Flutter/Dart codebases into idiomatic, maintainable Flutter. Covers bloc/cubit, clean architecture, rebuilds, layering, testing, accessibility, localization, and package hygiene. |

### Frontend

| Skill | Description |
|---|---|
| **frontend-typescript-code-smells** | Identifies and refactors frontend TypeScript code smells in React, Angular, Vue, or vanilla TS. Covers re-renders, effect bugs, unsafe `any`, state/data flow, component boundaries, and type strengthening. |

### Java

| Skill | Description |
|---|---|
| **java-refactoring** | Review Java code for maintainability issues, code smells, and SOLID violations. Creates behavior-preserving refactoring plans. |
| **java-21-refactor-assessor** | Assesses and refactors Java 21 codebases into idiomatic, maintainable Java. Removes Pythonic anti-patterns, improves architecture, concurrency, testing, and error handling. |

### General

| Skill | Description |
|---|---|
| **reflect** | Analyze conversation for learnings and update project instructions with confidence-scored, evidence-backed patterns. Integrates claude-flow concepts: uncertainty ledger, EWC++ anti-forgetting, temporal validity, evolution proposals. |
| **feature-demo-recorder** | Records, trims, and publishes a short reviewer-facing demo of a completed feature. Produces GIF/MP4 assets, uploads them to GitHub, updates the PR `## Demo` section, and cleans local scratch artifacts. |

## Structure

```
skills/
│
│ # Flutter
├── figma-to-flutter/
│   ├── SKILL.md
│   └── references/
│       ├── figma-mcp-tools.md
│       ├── flutter-implementation.md
│       ├── testing-comparison.md
│       └── troubleshooting.md
├── flutter-cleanup-assessor/
│   ├── SKILL.md
│   ├── references/    (15 reference files)
│   └── assets/        (assessment template, analysis_options sample)
│
│ # Frontend
├── frontend-typescript-code-smells/
│   ├── SKILL.md
│   ├── references/    (14 reference files)
│   ├── scripts/       (quality gates)
│   └── assets/        (report template)
│
│ # Java
├── java-refactoring/
│   ├── SKILL.md
│   └── references/
│       ├── code-smells-catalog.md
│       └── solid-principles.md
├── java-21-refactor-assessor/
│   ├── SKILL.md
│   └── references/
│       └── java-21-best-practices.md
│
│ # General
├── reflect/
│   ├── SKILL.md
│   └── references/
│       ├── confidence-scoring.md
│       ├── reflection-categories.md
│       └── update-targets.md
└── feature-demo-recorder/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   └── feature_demo_playbook.md
    └── scripts/
        ├── make_demo_assets.sh
        └── publish_pr_demo.py
```

## Updating

Re-run the install command to pull the latest version:

```bash
npx skills add ByAxe/ai-engineering-skills
```

To update a single skill:

```bash
npx skills add ByAxe/ai-engineering-skills --skill java-refactoring
```

### Manual update

If you installed skills by copying files directly, sync from the repo:

```bash
git clone https://github.com/ByAxe/ai-engineering-skills.git /tmp/ai-skills

# Claude Code (~/.claude/skills/)
cp -r /tmp/ai-skills/skills/* ~/.claude/skills/

# Codex (~/.codex/skills/)
cp -r /tmp/ai-skills/skills/* ~/.codex/skills/

rm -rf /tmp/ai-skills
```

## Usage

Skills activate automatically based on conversation context. You can also invoke them explicitly:

- **Flutter** — "convert this Figma design to Flutter" or `/figma-to-flutter` · "clean up this Flutter code" or "assess this Flutter codebase for smells"
- **Frontend** — "review this TypeScript for code smells"
- **Java** — "refactor this Java code" · "modernize this Java 21 codebase"
- **General** — `/reflect` · "record a short feature demo and attach it to the PR"

## License

MIT
