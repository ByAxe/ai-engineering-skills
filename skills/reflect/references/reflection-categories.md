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

**Where they go:** Project instruction file > Known Limitations, Common Mistakes, or relevant component section

## Enforcement Patterns

Learnings about checks that should become automatic.

**Examples:**
- "Agents repeatedly missed required verification commands; the lifecycle hook should surface and block completion."
- "Generated artifacts became dirty after a smoke command; add a post-command cleanliness check."

**Signals in conversation:**
- Same omission recurs after user or hook correction
- A command failure reveals a cheap deterministic guard
- Manual checklist items are repeatedly forgotten

**Where they go:** Hooks, git hooks, CI/local gates, tests, or lifecycle checks. Use memory only for quirks that cannot be enforced safely.

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

**Where they go:** Project instruction file > Development Practices, Key Patterns, or Completion Checklist

## Contract Patterns

Learnings about desired product or capability behavior.

**Examples:**
- "Module 1 is now free-access content."
- "The changelog date must match the public updated-on date."
- "Signed-out copy must be distinct in title and body."

**Signals in conversation:**
- User corrects what the product now guarantees
- Requirements, acceptance criteria, or scenarios change
- The learning should be true for users, not only for agents

**Where they go:** Specs/OpenSpec, tests, changelog, content source, or docs. Use instruction files only for the workflow that maintains the contract.

## Agent-Steering Patterns

Learnings about how agents should perform repeatable work.

**Examples:**
- "OpenSpec verification must include an independent reviewer pass."
- "Reflection must audit hooks, specs, prompts, skills, docs, and memory before choosing a target."

**Signals in conversation:**
- User corrects the agent's workflow expectations
- A reusable prompt, skill, or subagent instruction would prevent recurrence
- The pattern applies across repositories

**Where they go:** Skills, prompts/templates, evals, or project/global instruction files.

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

**Where they go:** Project instruction file > relevant architecture/component section, or Known Limitations

## Content and Release Patterns

Learnings about public-facing change communication.

**Examples:**
- "Do not list preface/module 0 as new if they were already open."
- "Include the new GitHub repository link in the education-program changelog."

**Signals in conversation:**
- User filters changelog suggestions as too broad or stale
- Visible updated dates, release notes, or localized content drift
- The same content must be reflected in multiple public surfaces

**Where they go:** Changelog, content-sync skill, content consistency tests/hooks, source content, or docs.

## Trace Event Mapping

When analyzing a conversation, look for these event patterns:

| Conversation Signal | Trace Event Type | Likely Category |
|---|---|---|
| Error message appeared | `tool_invoke` failure | Technical |
| User said "no, do X instead" | `correction` | Process or Communication |
| Retry succeeded with different approach | `backtrack` + `success` | Technical or Process |
| User explained project context | `user-feedback` | Project-Specific |
| Same fix applied twice | `repeated-pattern` | Technical (high confidence) |
| Hook blocked completion | `tool_invoke` failure + `correction` | Enforcement |
| Public behavior changed | `user-feedback` + implementation | Contract or Content |
| Reusable agent workflow changed | `correction` + `process update` | Agent-Steering |
| Approach worked on first try | `success` | Effective Pattern |
| User expressed frustration | `user-feedback` (negative) | Communication |
| Discovered undocumented behavior | `discovery` | Technical or Project-Specific |

## Anti-Pattern: What NOT to Capture

- **Obvious things**: "Python uses indentation" — derivable from reading code
- **Ephemeral state**: "Currently debugging test_api.py" — belongs in tasks, not memory
- **Git-trackable facts**: "Last commit fixed the preview bug" — use `git log`
- **Documented behavior**: If it's in the project docs already, don't duplicate to instruction files
- **One-off fixes**: A typo correction doesn't need documentation
- **Speculative learnings**: Confidence below 0.2 should not be persisted anywhere
- **Session-specific context**: Temporary file paths, debug ports, one-time env vars
