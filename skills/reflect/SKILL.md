---
name: reflect
description: Use this skill to reflect on a completed or interrupted work session, extract durable evidence-backed learnings, and update project instruction files (CLAUDE.md, AGENTS.md, or equivalent) plus persistent memory without duplicating existing guidance. Trigger when the user says "reflect", "what did we learn", "update instructions", "capture learnings", or asks to remember process, tool, or project lessons.
metadata:
  author: ByAxe
  version: "2.1.0"
  category: workflow
  tags: "reflection, learning, instructions, memory, continuous-improvement, confidence-scoring"
---

# Reflect

Turn a work session into durable guidance. Capture only lessons that would prevent future mistakes or speed future work.

## Non-Negotiables

- Quality over quantity: 2-3 sharp, evidence-backed insights beat 10 vague ones.
- Every learning must cite its evidence from the conversation.
- Never duplicate: check existing instruction files and memory before writing.
- Persist durable patterns, not task status, timestamps, or one-off facts available in git/logs.
- Prefer updating or superseding an existing entry over adding another entry.
- If the user explicitly asked to reflect or update memory, apply confirmed, non-contested memory changes directly. Ask before broad instruction-file edits, contested changes, or confidence below 0.5.

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
| Confirmed (0.8-1.0) | Instruction file or memory |
| Probable (0.5-0.79) | Memory, or proposed instruction-file edit |
| Uncertain (0.2-0.49) | Memory only, with caveat |
| Speculative (0.0-0.19) | Mention only; do not persist |

Read [confidence-scoring.md](references/confidence-scoring.md) when a score is ambiguous, a learning may edit an instruction file, or existing guidance may be superseded.

### Step 3: Check Existing Knowledge (Anti-Forgetting)

Before proposing updates, scan for conflicts with established guidance:

1. Read the current project's authoritative instruction files (`CLAUDE.md`, `AGENTS.md`, or equivalent), including the nearest nested file that governs the touched area.
2. Search the current agent's memory files:
   ```
   Grep pattern="relevant term" path="<current-agent-memory-dir>" glob="*.md"
   ```
3. If a semantic memory MCP is available:
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

Use [update-targets.md](references/update-targets.md) for the decision matrix. Default target choices:

- Project-wide durable workflow or architecture rule -> current project instruction file.
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

### Step 6: Verify and Report

- Re-read modified files to confirm correct placement
- Check no duplicates were introduced
- Confirm additions match existing style

**Report to user:**
```
Reflection Summary:
- [N] confirmed learnings persisted to instruction files
- [N] probable learnings saved to memory
- [N] uncertain findings noted (not persisted)
- [N] contested items resolved
- [N] existing entries updated/superseded
```
