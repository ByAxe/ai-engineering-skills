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

## Skills

| Skill | Description |
|---|---|
| **reflect** | Analyze conversation for learnings and update project instructions with confidence-scored, evidence-backed patterns. Integrates claude-flow concepts: uncertainty ledger, EWC++ anti-forgetting, temporal validity, evolution proposals. |
| **frontend-typescript-code-smells** | Identifies and refactors frontend TypeScript code smells in React, Angular, Vue, or vanilla TS. Covers re-renders, effect bugs, unsafe `any`, state/data flow, component boundaries, and type strengthening. |
| **java-refactoring** | Review Java code for maintainability issues, code smells, and SOLID violations. Creates behavior-preserving refactoring plans. |
| **java-21-refactor-assessor** | Assesses and refactors Java 21 codebases into idiomatic, maintainable Java. Removes Pythonic anti-patterns, improves architecture, concurrency, testing, and error handling. |

## Structure

```
skills/
├── reflect/
│   ├── SKILL.md
│   └── references/
│       ├── confidence-scoring.md
│       ├── reflection-categories.md
│       └── update-targets.md
├── frontend-typescript-code-smells/
│   ├── SKILL.md
│   ├── references/    (14 reference files)
│   ├── scripts/       (quality gates)
│   └── assets/        (report template)
├── java-refactoring/
│   ├── SKILL.md
│   └── reference.md
└── java-21-refactor-assessor/
    └── SKILL.md
```

## Usage

Skills activate automatically based on conversation context. You can also invoke them explicitly:

- `/reflect` - Run reflection analysis on the current conversation
- Ask Claude to "review this TypeScript for code smells"
- Ask Claude to "refactor this Java code"

## License

MIT
