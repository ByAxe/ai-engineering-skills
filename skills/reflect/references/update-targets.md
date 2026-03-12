# Update Targets Decision Matrix

Where each type of learning should be persisted.

## Decision Tree

```
Is it project-specific?
  YES -> Does CLAUDE.md already have a relevant section?
    YES -> UPDATE that section
    NO  -> Is it important enough for a new section?
      YES -> ADD new subsection under the closest parent
      NO  -> ADD as a bullet under the most relevant existing section
  NO  -> Is it about user preferences or communication style?
    YES -> Memory file (type: feedback or user)
    NO  -> Is it about a tool/MCP that's used across projects?
      YES -> Memory file (type: reference) + relevant project CLAUDE.md
      NO  -> Memory file (type: project or reference)
```

## Target: CLAUDE.md

**Best for:** Technical constraints, architectural decisions, workflow rules, known limitations, common mistakes, CI patterns, testing requirements.

**CLAUDE.md Section Map:**

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

**File location:** `~/.claude/projects/<current-project>/memory/`

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

## Target: claude-mem

**Best for:** Significant discoveries, debugging breakthroughs, architectural decisions that future sessions should know about.

**When to use:** In addition to (not instead of) CLAUDE.md or memory files. claude-mem provides searchable cross-session context.

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

**NOT a target for:** Quick tips, workarounds, or configuration details (those go in CLAUDE.md).
