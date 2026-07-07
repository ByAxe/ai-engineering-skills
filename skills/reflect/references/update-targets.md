# Update Targets Decision Matrix

Where each type of learning should be persisted. Use this file when memory is not obviously the right target.

## Decision Tree

```
Can the lesson be enforced mechanically?
  YES -> hook, CI/local gate, test, lint, or lifecycle check
  NO  -> Is it a product/code behavior contract?
    YES -> spec/OpenSpec, tests, docs if needed
    NO  -> Is it agent behavior or workflow reuse?
      YES -> skill, prompt/template, instruction file, or eval
      NO  -> Is it project-specific guidance?
        YES -> project instruction file, docs/runbook, or memory
        NO  -> user/global memory or semantic memory
```

Always explain why the chosen target is better than nearby alternatives.

## Environment Gate

Before choosing a target, identify which surfaces are present and writable.

| Environment Signal | Prefer | Avoid |
|---|---|---|
| Local repo with writable agent memory | Memory plus repo artifacts when appropriate | Saving only to memory when a repo contract/gate should change |
| Cloud/hosted workspace with repo write access | Repo-tracked specs/docs/skills/workflows, PR description/comment, issue | Local-only memory paths, workstation hook claims, secret-dependent proofs |
| Read-only/cloud proposal mode | Research report with exact target paths and patches | Claiming persistence happened |
| OpenSpec present (`openspec/config.yaml`, `openspec/specs`, active changes) | Active OpenSpec change/spec for product, architecture, agent-harness, hook, context-pack, deployment-gate, or memory-promotion contracts | Plain docs or memory as the only durable contract |
| Non-OpenSpec methodology present | Existing methodology artifacts: ADR/RFC, specs.md, Kiro, GitHub Spec Kit, BMAD, issue acceptance criteria, runbooks, or equivalent | Introducing OpenSpec or a new methodology unless requested |
| Hooks not installed or not verifiable | Propose hook/lifecycle gate and validation command; use CI/test if available | Claiming hook enforcement exists |
| CI/workflow available | CI/local gate, workflow check, or test for repeated mechanical misses | Manual checklist as the only guard |
| No repo write access but PR/issue comments available | PR/issue comment with proposal and evidence | Silent local notes |

If the ideal target is missing, propose creating it and state the smallest proof that would make it enforceable.

## Target Catalog

| Target | Use For | Do Not Use For | Validation |
|---|---|---|---|
| Project instruction files (`AGENTS.md`, `CLAUDE.md`, equivalents) | Durable rules agents must see before work | Detailed procedures, one-off facts, low-confidence notes | Re-read governing file; run context/instruction validator if present |
| Nested instruction files | Area-specific constraints | Project-wide rules | Same as project instructions, plus nearest-file routing |
| Memory files | User preferences, project/tool quirks, caveated observations | Enforceable policy, product contracts, facts already in git/logs | Search for duplicates; update index if new file |
| Semantic memory MCP | Searchable important discoveries across sessions | Only copy of a required rule | Search before saving; save concise evidence-backed memory |
| Docs/runbooks | Explanations, operational procedures, architecture narratives | Short rules that must always be seen | Docs tests/link checks if present |
| Specs/OpenSpec | Durable product/capability behavior, requirements, scenarios | Process tips or agent preferences | Spec validation, affected tests |
| ADR/RFC/specs.md/methodology docs | Durable design decisions and requirements in non-OpenSpec projects | Projects that already have a more specific contract layer | Existing methodology review/checks |
| Skills | Reusable agent workflow or judgment pattern across projects | Project-specific one-off quirks | Skill validator, lint/review, evals when behavior matters |
| Prompts/templates | Repeated task framing, PR descriptions, subagent prompts, issue templates | Rules that should be enforced automatically | Template smoke/manual use check |
| Hooks/git hooks/Codex lifecycle hooks | Repeated missed checks, cheap enforceable guardrails | Judgment-heavy guidance or flaky/expensive checks | Hook tests or dry-run commands |
| CI/local gates/tests | Behavioral regressions, contracts, generated-artifact drift | Pure preferences | Targeted test plus full relevant gate |
| Backlog/issues/ADRs | Larger work, contested decisions, future design choices | Immediate tiny edits | Link evidence and acceptance criteria |
| Changelog/release notes | User-visible shipped changes | Internal process facts | Date/localization/content consistency checks |
| Cloud run artifacts | Hosted-agent handoff, PR description/comment, launch result, issue comment | Long-term contract if repo files can be changed | Link back to repo-tracked follow-up or commit |

## Project Instruction Files

**Best for:** Technical constraints, architectural decisions, workflow rules, known limitations, common mistakes, CI patterns, testing requirements.

Use the instruction file the current project actually loads (`CLAUDE.md`, `AGENTS.md`, or equivalent). Read the root file and any more specific nested file before editing.

**Section Map:**

| Learning Type | Target Section |
|---|---|
| New command/make target | Common Commands |
| Architecture insight | Architecture Overview |
| Environment variable | Environment Variables |
| Tool limitation | Known Limitations |
| Workflow rule | Development Practices / Key Patterns |
| Testing insight | Pre-Commit Validation or Testing |
| CI/deployment issue | CI Failure Cascade |
| Git workflow | Git Operations |
| Code style rule | Coding Style |
| Spike finding | Working with Research Spikes |
| Completion criteria | MANDATORY COMPLETION CHECKLIST |
| Anti-pattern | Common Mistakes |

**Style rules:**
- Match existing formatting (bullets, code blocks, bold labels)
- Use the existing pattern: "Anti-pattern X: description | Correct Y: description"
- Keep entries concise: 1-2 lines per bullet
- Include evidence: file paths, error messages, command examples

## Target: Memory Files

**Best for:** Cross-project learnings, user preferences, tool knowledge, external references.

**File location:** Use the current agent's project memory directory. Common defaults include `~/.claude/projects/<current-project>/memory/` and `~/.codex/projects/<current-project>/memory/`.

**Format:**
```markdown
---
name: descriptive-name
description: one-line description for relevance matching
type: feedback | user | project | reference
---

Content with Why and How to apply lines for feedback/project types.
```

**After creating:** Add entry to MEMORY.md index.

## Target: Semantic Memory MCP

**Best for:** Significant discoveries, debugging breakthroughs, architectural decisions that future sessions should know about.

**When to use:** In addition to (not instead of) instruction files or memory files. A semantic memory MCP provides searchable cross-session context.

**Format:**
```
save_memory(
  text="<detailed description with context>",
  title="<short title>",
  project="<current-project>"
)
```

## Target: Project Documentation (docs/)

**Best for:** Findings that change understanding of architecture, concepts, or implementation paths.

**When to use:** Only if the learning is substantial enough to warrant a doc update. Use a documentation-focused subagent for this if available.

**NOT a target for:** Quick tips, workarounds, or configuration details (those go in project instruction files).

## Target: Specs and OpenSpec

**Best for:** Product behavior contracts, acceptance scenarios, capability requirements, and requirements changed by a session.

Use the project's existing contract layer when the learning should change what the system must do, not merely how agents should work.

If OpenSpec is present, treat it as the durable contract layer for:
- product behavior and acceptance scenarios
- architecture invariants
- agent workflow and harness rules
- hook, context-pack, deployment-gate, and memory-promotion contracts

Use an active `openspec/changes/<change-id>` when the requirement is still being proposed or implemented. Sync/archive only after verification. If the OpenSpec CLI or write access is unavailable in the current environment, produce a proposal with exact capability/spec paths and the validation command to run later.

If OpenSpec is absent, do not invent it. Route to the project's current methodology instead: ADR/RFC, `specs.md`, Kiro artifacts, GitHub Spec Kit files, BMAD artifacts, issue acceptance criteria, runbooks, or whichever contract layer the repo already uses. If no contract layer exists, propose the smallest durable repo artifact before falling back to memory.

## Target: Hooks, Gates, and Tests

**Best for:** Repeated misses that can be checked cheaply and deterministically.

Examples:
- Required verification commands repeatedly missed -> lifecycle hook or pre-completion check.
- Generated artifacts left dirty -> targeted smoke or post-command cleanliness check.
- Changelog date drift -> content consistency test.

Avoid hooks for subjective judgment, expensive broad checks, or flaky checks. Put those in skills/runbooks with explicit verification guidance.

In cloud runs, do not assume workstation git hooks or Codex lifecycle hooks are installed. Prefer CI/workflow checks when the guard must work in cloud, or propose the hook plus a separate local verification step.

## Target: Skills, Prompts, Templates, and Evals

**Best for:** Reusable agent behavior, subagent prompts, workflow sequences, and reflection itself.

Use a skill when the lesson is a repeatable judgment workflow. Use a prompt/template when the issue is task framing. Use evals when the skill must reliably produce or avoid a behavior.

For cloud skill launches, include cloud-specific limits in the proposal: available repo, branch/PR target, writable files, missing local memory, and validations that must run in CI or a later local session.

## Changelog and Content Hygiene

When reflecting on public content changes:
- Highlight only significant new changes; filter facts already true before the session.
- Keep localized changelog wording aligned when the product has multiple languages.
- Update visible "updated on" dates together with the changelog date when that is the project convention.
- Consider a content-sync skill note, test, or hook if this drift has repeated.
