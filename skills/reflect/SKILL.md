---
name: reflect
description: Analyze conversation for learnings and update project instructions (CLAUDE.md) and persistent memory with confidence-scored, evidence-backed patterns. Use when user says "reflect", "what did we learn", "update instructions", "capture learnings", or at the end of significant work sessions.
metadata:
  author: ByAxe
  version: 2.0.0
  category: workflow
  tags: [reflection, learning, instructions, memory, continuous-improvement, confidence-scoring]
---

# Reflect

Evidence-based conversation analysis that extracts learnings, scores their confidence, and persists them where they matter. Inspired by claude-flow's uncertainty ledger and evolution pipeline.

## Important

- Quality over quantity: 2-3 sharp, evidence-backed insights beat 10 vague ones
- Every learning must cite its evidence from the conversation
- Score confidence honestly — uncertain findings are valuable when labeled as such
- Never overwrite established high-confidence rules without explicit user approval
- Never duplicate: always check existing CLAUDE.md and memory before proposing

## Instructions

### Step 1: Trace the Conversation

Review the conversation as a sequence of trace events, not just outcomes. For each significant event, note:

**Event type**: correction, discovery, success, failure, backtrack, user-feedback
**Evidence**: the specific quote, error message, file path, or command output
**Impact**: did it change approach, reveal a constraint, or confirm a pattern?

Categorize into three buckets:

**Effective Patterns** — approaches that worked well
- What tool/technique was used?
- Why did it succeed? (reproducible insight, not luck)
- How many times did this pattern succeed in the session? (frequency = confidence)

**Corrections** — where the user corrected you or you had to backtrack
- What was the original mistake?
- What was the fix?
- Is this a recurring pattern? (check claude-mem for similar past corrections)

**Discoveries** — new information about the project, tools, or environment
- Technical constraints or behaviors not documented anywhere
- Workarounds that resolved blockers
- Integration details between components

### Step 2: Score Confidence

For each finding, assign a confidence level using evidence weight:

| Level | Label | Criteria | Persistence Target |
|-------|-------|----------|-------------------|
| 0.8-1.0 | **Confirmed** | Repeated in session + user validated, or reproduced with evidence | CLAUDE.md (direct add) |
| 0.5-0.79 | **Probable** | Single strong signal, logical inference from evidence | CLAUDE.md (propose) or Memory |
| 0.2-0.49 | **Uncertain** | Edge case, might not generalize, limited evidence | Memory file only (with caveat) |
| 0.0-0.19 | **Speculative** | Hunch, no hard evidence | Mention to user, do not persist |

**Evidence weight factors:**
- User explicitly stated it (+0.3)
- Error message / stack trace confirms it (+0.2)
- Reproduced multiple times in session (+0.2)
- Contradicts no existing guidance (+0.1)
- Aligns with existing patterns (+0.1)
- Single occurrence, no corroboration (+0.0)

Consult `references/confidence-scoring.md` for detailed scoring examples.

### Step 3: Check Existing Knowledge (Anti-Forgetting)

Before proposing updates, scan for conflicts with established guidance:

1. Read the current `CLAUDE.md` in the project root
2. Search memory files:
   ```
   Grep pattern="relevant term" path="~/.claude/projects/<current-project>/memory/" glob="*.md"
   ```
3. If claude-mem is available:
   ```
   search(query="relevant term", limit=10, project="<current-project>")
   ```

**Anti-forgetting rules** (adapted from EWC++ consolidation):
- Entries marked CRITICAL in CLAUDE.md are protected — never weaken or remove
- If a new learning conflicts with an existing rule, mark it as CONTESTED and present both to the user with evidence for each side
- High-frequency patterns (referenced in multiple CLAUDE.md sections) have higher importance — require stronger evidence to modify
- When updating an entry, preserve the original intent while refining the details

Mark each finding: NEW | UPDATE | CONTESTED | SKIP

### Step 4: Propose Changes as Evolution Proposals

For each NEW, UPDATE, or CONTESTED item, format as a structured proposal:

```
## Proposal: [Short title]

Target: CLAUDE.md > [Section Name]  |  Memory > [filename]
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

Existing rule: [current CLAUDE.md text]
Evidence for existing: [why it was added]
New finding: [what this session suggests]
Evidence for new: [conversation evidence]
Recommendation: [keep existing | replace | merge | ask user]
```

Consult `references/update-targets.md` for the decision matrix on persistence targets.
Consult `references/reflection-categories.md` for category definitions.

### Step 5: Apply Approved Changes

After user approval:

1. **CLAUDE.md edits** — place in correct section, match existing style
2. **Memory files** — write to the project's memory directory (`~/.claude/projects/<current-project>/memory/`) with frontmatter (name, description, type). Include confidence level in the content.
3. **MEMORY.md index** — update if new memory files were created
4. **claude-mem** — save confirmed/probable discoveries:
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
- [N] confirmed learnings persisted to CLAUDE.md
- [N] probable learnings saved to memory
- [N] uncertain findings noted (not persisted)
- [N] contested items resolved
- [N] existing entries updated/superseded
```

## Performance Notes

- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip confidence scoring — it prevents low-quality guidance from polluting CLAUDE.md
- When confidence is below 0.5, ask the user before persisting
- Prefer updating existing entries over adding new ones to prevent guidance bloat
