# Reflection Categories

Detailed definitions and examples for each learning category. Each category includes trace event types that signal it during conversation analysis.

## Technical Patterns

Learnings about code, architecture, tools, and infrastructure.

**Examples:**
- "PostgreSQL JSONB indexes require GIN, not B-tree, for containment queries"
- "mypy union type errors require explicit Protocol definitions, not bare Union"
- "WebSocket reconnection needs exponential backoff or the server rate-limits the client"

**Signals in conversation:**
- Error messages that took multiple attempts to resolve
- Workarounds discovered through trial and error
- Configuration details not in official docs
- Tool behavior that surprised you

**Where they go:** CLAUDE.md > Known Limitations, Common Mistakes, or relevant component section

## Process Patterns

Learnings about workflows, methodology, and development practices.

**Examples:**
- "Running `make test` before committing catches integration issues that unit tests miss"
- "Visual validation requires actual browser inspection, API 200 does not mean UI works"
- "Feature work must deploy to staging before marking complete"

**Signals in conversation:**
- User saying "no, do X first" or "you skipped Y"
- Steps that had to be repeated because prerequisites were missed
- Workflow sequences that proved effective

**Where they go:** CLAUDE.md > Development Practices, Key Patterns, or Completion Checklist

## Communication Patterns

Learnings about how the user prefers to interact and receive information.

**Examples:**
- "User prefers concise responses without trailing summaries"
- "User wants evidence before marking anything complete"
- "User expects parallel execution when tasks are independent"

**Signals in conversation:**
- User corrections about tone, format, or level of detail
- Repeated asks for a specific communication style
- Frustration signals about too much/too little information

**Where they go:** Memory files (type: feedback or user) since these transcend the project

## Project-Specific Patterns

Learnings unique to this codebase, its quirks, and its constraints.

**Examples:**
- "The dev server must be running on port 3000 before e2e tests work"
- "File uploads only work in local mode, not in the CI container"
- "The staging API endpoint format differs from production"

**Signals in conversation:**
- Configuration that took debugging to get right
- Integration points between components that aren't obvious
- Environment-specific behaviors

**Where they go:** CLAUDE.md > relevant architecture/component section, or Known Limitations

## Trace Event Mapping

When analyzing a conversation, look for these event patterns:

| Conversation Signal | Trace Event Type | Likely Category |
|---|---|---|
| Error message appeared | `tool_invoke` failure | Technical |
| User said "no, do X instead" | `correction` | Process or Communication |
| Retry succeeded with different approach | `backtrack` + `success` | Technical or Process |
| User explained project context | `user-feedback` | Project-Specific |
| Same fix applied twice | `repeated-pattern` | Technical (high confidence) |
| Approach worked on first try | `success` | Effective Pattern |
| User expressed frustration | `user-feedback` (negative) | Communication |
| Discovered undocumented behavior | `discovery` | Technical or Project-Specific |

## Anti-Pattern: What NOT to Capture

- **Obvious things**: "Python uses indentation" — derivable from reading code
- **Ephemeral state**: "Currently debugging test_api.py" — belongs in tasks, not memory
- **Git-trackable facts**: "Last commit fixed the preview bug" — use `git log`
- **Documented behavior**: If it's in the project docs already, don't duplicate to CLAUDE.md
- **One-off fixes**: A typo correction doesn't need documentation
- **Speculative learnings**: Confidence below 0.2 should not be persisted anywhere
- **Session-specific context**: Temporary file paths, debug ports, one-time env vars
