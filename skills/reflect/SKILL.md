---
name: reflect
description: Reflects on completed or interrupted sessions, extracts evidence-backed lessons, and routes them to the right persistent surface. Use when the user says "reflect", "what did we learn", "capture learnings", "update memory/instructions", or asks where a lesson belongs across specs, hooks, skills, docs, prompts, or automation.
metadata:
  author: ByAxe
  version: "2.3.0"
  category: workflow
  tags: "reflection, learning, instructions, memory, steering, continuous-improvement, confidence-scoring"
---

# Reflect

Turn a work session into durable steering. Capture only lessons that would prevent future mistakes or speed future work.

## Non-Negotiables

- Quality over quantity: 2-3 sharp, evidence-backed insights beat 10 vague ones.
- Every learning must cite its evidence from the conversation.
- Never duplicate: check existing instruction files and memory before writing.
- Persist durable patterns, not task status, timestamps, or one-off facts available in git/logs.
- Prefer updating or superseding an existing entry over adding another entry.
- Consider every durable persistence surface before defaulting to memory.
- Condition target choice on the actual environment and methodology: local vs cloud, writable vs read-only, OpenSpec vs another contract layer, hooks installed vs merely possible.
- If the user asks for research, exploration, proposals, or "no changes yet", stop after proposals.
- If the user explicitly asked to reflect or update memory, apply confirmed, non-contested memory changes directly. Ask before broad structural edits, contested changes, or confidence below 0.5.
- Run an independent reviewer pass for broad instruction/spec/hook/skill changes when subagents are available. If unavailable, record the warning before reporting completion.

## Instructions

### Step 1: Build the Trace

Review the conversation as trace events, not just outcomes. For each significant event, note:

**Event type**: correction, discovery, success, failure, backtrack, user-feedback
**Evidence**: the specific quote, error message, file path, or command output
**Impact**: did it change approach, reveal a constraint, or confirm a pattern?

Classify candidates as Effective Pattern, Correction, or Discovery. Read [reflection-categories.md](references/reflection-categories.md) when classification or target choice is not obvious.

### Step 2: Score Confidence

For each candidate, assign a confidence band and default target:

| Band | Default target |
|---|---|
| Confirmed (0.8-1.0) | Best durable surface after target audit |
| Probable (0.5-0.79) | Memory, or proposed durable-surface edit |
| Uncertain (0.2-0.49) | Memory only, with caveat |
| Speculative (0.0-0.19) | Mention only; do not persist |

Read [confidence-scoring.md](references/confidence-scoring.md) when a score is ambiguous, a learning may edit an instruction file, or existing guidance may be superseded.

### Step 3: Check Existing Knowledge (Anti-Forgetting)

Before proposing updates, scan for conflicts with established guidance:

1. Read the current project's authoritative instruction files (`CLAUDE.md`, `AGENTS.md`, or equivalent), including the nearest nested file that governs the touched area.
2. Inspect any relevant local steering surfaces: specs, hooks, skills, docs/runbooks, templates, CI gates, or prompt files.
3. Detect environment constraints before picking targets:
   - local or cloud/hosted workspace
   - writable repo, writable agent memory, or proposal-only
   - project methodology or contract layer: OpenSpec, ADR/RFC, specs.md, Kiro, GitHub Spec Kit, BMAD, issue acceptance criteria, runbooks, or none
   - hooks/lifecycle checks installed and verifiable, or only possible as a proposal
   - CI/workflow, PR, issue, or cloud-run artifact surfaces available
4. Search the current agent's memory files when they are readable:
   ```
   Grep pattern="relevant term" path="<current-agent-memory-dir>" glob="*.md"
   ```
   If memory is read-only or unavailable, use it only for duplicate/conflict checks and route persistence elsewhere.
5. If a semantic memory MCP is available:
   ```
   search(query="relevant term", limit=10, project="<current-project>")
   ```

**Anti-forgetting rules** (adapted from EWC++ consolidation):
- Entries marked CRITICAL in instruction files are protected — never weaken or remove
- If a new learning conflicts with an existing rule, mark it as CONTESTED and present both to the user with evidence for each side
- High-frequency patterns (referenced in multiple instruction sections) have higher importance — require stronger evidence to modify
- When updating an entry, preserve the original intent while refining the details

Mark each finding: NEW | UPDATE | CONTESTED | SKIP

### Step 4: Choose Target and Proposal Shape

Use [update-targets.md](references/update-targets.md) for the decision matrix. For each candidate, name why the chosen target is better than nearby alternatives.

- Project-wide durable workflow or architecture rule -> current project instruction file.
- Enforceable repeated miss -> hook, CI/local gate, lifecycle check, or test.
- Capability contract -> the project's existing contract layer.
- OpenSpec project contract or agent-harness rule -> active OpenSpec change/spec before docs or memory.
- Non-OpenSpec methodology -> ADR/RFC/specs.md/issue acceptance criteria/runbook, matching current project practice.
- Cloud/hosted run without writable memory or hook proof -> repo-tracked artifact, PR/issue/comment, or proposal with exact target paths.
- Reusable agent behavior -> skill, prompt, template, or eval.
- Tool, environment, or project quirk -> memory file; also save to semantic memory if important.
- User preference or communication pattern -> memory only.
- One-off task status or facts already in git/logs -> SKIP.

For items that require review, use this proposal format:

```
## Proposal: [Short title]

Target: [instruction file] > [Section Name]  |  Memory > [filename]
Action: ADD | UPDATE | SUPERSEDE
Confidence: [0.0-1.0] ([Confirmed|Probable|Uncertain])
Evidence:
  - [Quote or reference from conversation]
  - [Error message, file path, or command output]
Environment: [local|cloud|readonly|OpenSpec|non-OpenSpec|unknown, plus writable surfaces]
Why this target: [why this surface is better than memory/instructions/specs/hooks/skills/docs]
Fallback if unavailable: [proposal-only target or next-best durable surface]
Supersedes: [existing entry it replaces, if any]
Temporal: [permanent | until-next-refactor | version-specific]
Risk: [low|medium|high] — [what goes wrong if this is incorrect]
---
[Exact text to add/modify]
---
```

For CONTESTED items, present both sides:
```
## Contested: [Title]

Existing rule: [current instruction-file text]
Evidence for existing: [why it was added]
New finding: [what this session suggests]
Evidence for new: [conversation evidence]
Recommendation: [keep existing | replace | merge | ask user]
```

### Step 5: Apply Changes

If the user asked for proposals only, stop after Step 4. Otherwise:

1. **Instruction-file edits** — place in the correct section, match existing style, and keep the addition short.
2. **Memory files** — write to the current agent's project memory directory with frontmatter (name, description, type). Include confidence level in the content.
3. **MEMORY.md index** — update if new memory files were created
4. **Semantic memory** — save confirmed/probable discoveries when the MCP is available:
   ```
   save_memory(text="[learning with evidence]", title="[title]", project="<current-project>")
   ```
5. **Supersession** — if new entry supersedes an old one, update/remove the old entry rather than leaving both
6. **Other surfaces** — for specs, hooks, skills, docs, prompts, templates, or tests, make the smallest scoped edit and run that surface's validator.
7. **Cloud constraints** — if the chosen surface is unavailable in the current hosted run, do not fake persistence. Record the exact patch/proposal, PR/issue/comment target, or validation command needed in an environment that can apply it.

### Step 6: Independent Review

For broad instruction/spec/hook/skill edits, or any reflection that changes multiple persistence surfaces, run an independent reviewer subagent after the main edits and before final reporting.

Reviewer prompt shape:
```
Review this reflection change independently. Check whether each learning is evidence-backed, non-duplicative, routed to the right persistence surface, and not weakening existing protected guidance. Report findings only; do not edit files.
Artifacts: [conversation evidence summary], [changed files], [proposal list]
```

Resolve or explicitly reject reviewer findings with evidence. If subagents are not available in the current client, state that and perform the same checklist yourself; do not silently skip the reviewer gate.

### Step 7: Verify and Report

- Re-read modified files to confirm correct placement
- Check no duplicates were introduced
- Confirm additions match existing style
- Run relevant validators for changed surfaces, such as skill lint/review/evals for skill changes, spec validation for spec changes, hook tests for hook changes, or repository tests for code changes.

**Report to user:**
```
Reflection Summary:
- [N] confirmed learnings persisted
- [N] surfaces updated or proposed
- [N] uncertain findings noted (not persisted)
- [N] contested items resolved
- [N] existing entries updated/superseded
- Independent review: [passed | findings resolved | unavailable with warning]
```
