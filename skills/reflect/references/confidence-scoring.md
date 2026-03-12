# Confidence Scoring Reference

Adapted from claude-flow's UncertaintyLedger and BeliefStatus system.

## Confidence Levels

### Confirmed (0.8 - 1.0)

Multiple evidence sources agree. Pattern reproduced. User validated.

**Examples:**
- User corrected you 3 times about the same thing (confidence: 0.95)
- Error reproduced with identical stack trace on retry (confidence: 0.85)
- User explicitly said "always do X" (confidence: 0.9)
- `make test` failed consistently until specific fix applied (confidence: 0.85)

**Persistence:** Direct addition to CLAUDE.md. These are reliable rules.

### Probable (0.5 - 0.79)

Single strong signal or logical inference from solid evidence.

**Examples:**
- Error occurred once but root cause is clearly understood (confidence: 0.7)
- Workaround solved the problem but wasn't tested in other contexts (confidence: 0.6)
- User implied preference but didn't state it explicitly (confidence: 0.55)
- Documentation gap found — behavior differs from what docs suggest (confidence: 0.65)

**Persistence:** Propose to CLAUDE.md (user reviews) or save to memory file.

### Uncertain (0.2 - 0.49)

Edge case, limited evidence, might not generalize.

**Examples:**
- Fix worked but you're not sure why (confidence: 0.3)
- Pattern observed once, could be coincidence (confidence: 0.25)
- Applies only to a specific file/function, unclear if broader (confidence: 0.4)
- Timing-dependent behavior that might not reproduce (confidence: 0.35)

**Persistence:** Memory file with explicit caveat. NOT CLAUDE.md.

### Speculative (0.0 - 0.19)

Hunch with no hard evidence. Mention to user, do not persist.

**Examples:**
- "I think this might be related to X but I have no evidence"
- Suspicion about a race condition with no reproduction
- Guess about why a previous developer made a choice

**Persistence:** None. Mention verbally if relevant.

## Evidence Types and Weights

Adapted from claude-flow's EvidencePointer system.

| Source Type | Weight | Description |
|---|---|---|
| user-explicit | 0.30 | User directly stated the rule or preference |
| error-output | 0.20 | Error message, stack trace, or failing test output |
| reproduction | 0.20 | Pattern observed multiple times in the session |
| no-contradiction | 0.10 | Does not conflict with existing guidance |
| pattern-alignment | 0.10 | Aligns with related existing patterns |
| single-observation | 0.00 | Observed once, no corroboration (base weight) |
| contradicts-existing | -0.15 | Conflicts with established CLAUDE.md entry |
| context-specific | -0.10 | Only applies in a narrow context |

**Scoring formula:** Sum applicable weights, clamp to [0.0, 1.0].

## Temporal Validity

Adapted from claude-flow's TemporalAssertion system.

Each learning has a validity window:

| Temporal Type | Description | Review Trigger |
|---|---|---|
| **permanent** | Fundamental constraint (e.g., "SQL transactions require explicit COMMIT") | Only if underlying tech changes |
| **until-next-refactor** | True for current architecture, may change with redesign | Major refactoring |
| **version-specific** | Tied to specific library/tool version | Dependency update |
| **session-specific** | Only relevant to this debugging session | Do NOT persist |

When reviewing existing CLAUDE.md entries during reflection:
- Flag entries whose referenced code/files no longer exist
- Note entries tied to specific versions that may have been upgraded
- Suggest retirement of stale guidance with evidence

## Decay Awareness

Adapted from claude-flow's temporal decay and SONA pattern confidence.

Confidence in a learning decreases if:
- It hasn't been relevant in many sessions (unused pattern)
- The codebase has significantly changed since it was captured
- Related entries have been superseded

When encountering a low-confidence existing entry:
1. Check if the referenced code/behavior still exists
2. If outdated, propose SUPERSEDE or RETIRE action
3. If still valid, boost confidence by noting reconfirmation

## Anti-Forgetting Rules

Adapted from claude-flow's EWC++ (Elastic Weight Consolidation).

**Core principle:** Established, high-importance patterns must not be casually overwritten.

**Protection tiers:**

| Tier | Signal | Protection |
|---|---|---|
| **Critical** | Marked CRITICAL in CLAUDE.md, or in completion checklist | Cannot modify without user confirmation + strong evidence |
| **High** | Referenced in multiple sections, or has ## header | Require confidence >= 0.8 to modify |
| **Normal** | Standard bullet point entry | Require confidence >= 0.5 to modify |
| **Low** | In Known Limitations or contextual notes | Can update freely with evidence |

**Conflict resolution:**
- If new learning contradicts a Critical entry: present as CONTESTED, never auto-resolve
- If new learning contradicts a High entry: require user confirmation
- If new learning contradicts a Normal entry: propose update with evidence comparison
- If new learning contradicts a Low entry: propose supersession
