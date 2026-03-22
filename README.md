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
| **figma-to-flutter** | Converts Figma designs to pixel-perfect Flutter code using figma-console-mcp. Extracts design metadata, exports assets, implements UI, and iteratively validates. Requires figma-console-mcp server. |

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
│   └── references/
│       ├── code-smells-catalog.md
│       └── solid-principles.md
├── java-21-refactor-assessor/
│   ├── SKILL.md
│   └── references/
│       └── java-21-best-practices.md
└── figma-to-flutter/
    ├── SKILL.md
    └── references/
        ├── figma-mcp-tools.md
        ├── flutter-implementation.md
        ├── testing-comparison.md
        └── troubleshooting.md
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

- `/reflect` - Run reflection analysis on the current conversation
- Ask Claude to "review this TypeScript for code smells"
- Ask Claude to "refactor this Java code"
- Ask Claude to "convert this Figma design to Flutter" or "/figma-to-flutter"

## License

MIT
