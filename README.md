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

Run Tessl standards and eval checks for a changed skill when relevant:

```bash
tessl skill review --threshold 90 skills/reflect
```

Tessl evals require a local Tessl project link (`tessl project create` or `tessl project link`):

```bash
tessl eval skills/reflect/evals --context skills/reflect --runs 1 --label reflect-check --yes --json
```

## Skills

### Flutter

| Skill | Description |
|---|---|
| **figma-to-flutter** | Converts Figma designs to pixel-perfect Flutter code using figma-console-mcp. Extracts design metadata, exports assets, implements UI, and iteratively validates. Uses live Desktop Bridge tools when REST-backed Figma calls hit `403 Token expired`. |
| **flutter-cleanup-assessor** | Assesses and refactors Flutter/Dart codebases into idiomatic, maintainable Flutter. Covers bloc/cubit, clean architecture, rebuilds, layering, testing, accessibility, localization, and package hygiene. |

### Go

| Skill | Description |
|---|---|
| **go-code-smells** | Identifies and refactors Go code smells in libraries, services, CLIs, and modules. Covers package/API design, interfaces, errors, context, goroutines, channels, testing, and performance. |

### Frontend

| Skill | Description |
|---|---|
| **frontend-typescript-code-smells** | Identifies and refactors frontend TypeScript code smells in React, Angular, Vue, or vanilla TS. Covers re-renders, effect bugs, unsafe `any`, state/data flow, component boundaries, and type strengthening. |

### Java

| Skill | Description |
|---|---|
| **java-refactoring** | Review Java code for maintainability issues, code smells, and SOLID violations. Creates behavior-preserving refactoring plans. |
| **java-21-refactor-assessor** | Assesses and refactors Java 21 codebases into idiomatic, maintainable Java. Removes Pythonic anti-patterns, improves architecture, concurrency, testing, and error handling. |

### Kotlin / JVM

| Skill | Description |
|---|---|
| **quarkus-kotlin-cleanup-assessor** | Assesses and refactors Kotlin server-side Quarkus codebases into idiomatic, maintainable Quarkus and Kotlin. Covers CDI, REST, config, Panache, coroutines, virtual threads, testing, security, observability, native-readiness, and Spring-to-Quarkus migration. |

### Multi-Agent Orchestration

| Skill | Description |
|---|---|
| **gastown-guru** | Expert guide for Gas Town (gt) multi-agent orchestration — setup, rig management, formula workflows (shiny, shiny-enterprise, TDD), convoy orchestration, quality pipelines, and troubleshooting. Covers the full spec-to-code pipeline with parallel agent dispatch. |

### General

| Skill | Description |
|---|---|
| **reflect** | Analyze work-session learnings and route evidence-backed guidance to the right durable surface: memory, instructions, specs, hooks, skills, docs, prompts, templates, or automation. |
| **feature-demo-recorder** | Records, trims, and publishes a short reviewer-facing demo of a completed feature. Produces GIF/MP4 assets, uploads them to GitHub, updates the PR `## Demo` section, and cleans local scratch artifacts. |
| **fix-bug** | Fixes, debugs, or specifies defects in OpenSpec-style repositories. Captures current, expected, and unchanged behavior, identifies root cause, adds regression coverage, and maps complex bugfixes into OpenSpec proposal/design/tasks/spec artifacts. |

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
│ # Go
├── go-code-smells/
│   ├── SKILL.md
│   ├── references/    (16 reference files)
│   ├── scripts/       (quality gates, profiling)
│   └── assets/        (code review + refactor report templates)
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
│ # Kotlin / JVM
├── quarkus-kotlin-cleanup-assessor/
│   ├── SKILL.md
│   ├── references/    (18 reference files)
│   └── assets/        (assessment template, detekt config, editorconfig samples)
│
│ # Multi-Agent Orchestration
├── gastown-guru/
│   ├── SKILL.md
│   └── references/
│       ├── agent-configuration.md
│       ├── community-insights.md
│       ├── concepts-glossary.md
│       ├── convoy-orchestration.md
│       ├── formula-hierarchy.md
│       ├── infrastructure.md
│       ├── setup-pitfalls.md
│       └── spec-to-code-pipeline.md
│
│ # General
├── reflect/
│   ├── SKILL.md
│   ├── evals/        (7 reflection routing scenarios)
│   └── references/
│       ├── confidence-scoring.md
│       ├── reflection-categories.md
│       └── update-targets.md
├── feature-demo-recorder/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   └── feature_demo_playbook.md
    └── scripts/
        ├── make_demo_assets.sh
        └── publish_pr_demo.py
└── fix-bug/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── evals/        (6 OpenSpec bugfix scenarios)
    └── references/
        ├── bugfix-spec-workflow.md
        └── investigation-quality-gates.md
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
- **Go** — "find code smells in this Go package" · "refactor this Go service" · "fix context misuse or goroutine leaks"
- **Frontend** — "review this TypeScript for code smells"
- **Java** — "refactor this Java code" · "modernize this Java 21 codebase"
- **Kotlin / JVM** — "clean up this Quarkus Kotlin service" · "assess this Quarkus codebase for Spring-shaped anti-patterns"
- **Multi-Agent** — "set up a Gas Town rig" · "launch a convoy with shiny-enterprise" · "fix gt doctor issues" · "what formula should I use?"
- **General** — `/reflect` · "record a short feature demo and attach it to the PR" · "fix this bug with an OpenSpec-compatible spec"

## License

MIT
