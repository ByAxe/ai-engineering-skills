---
name: fix-bug
description: Fix, debug, or specify defects in OpenSpec-style repositories. Use when the user reports a bug, regression, flaky behavior, failing test, security/auth/payment issue, or asks for an OpenSpec-compatible bugfix proposal/spec. The skill reproduces or characterizes the defect, identifies root cause, writes the smallest safe fix, adds regression coverage, and captures current, expected, and unchanged behavior.
license: MIT
metadata:
  author: ByAxe Datamola
  version: 1.0.0
  category: software-development
  tags:
    - debugging
    - bugfix
    - openspec
    - regression-tests
    - specifications
---

# Fix Bug

Use this skill for defect work that must preserve existing behavior while changing the smallest code surface that actually fixes the issue.

## Start Here

1. Read the repository's local instructions first: `AGENTS.md`, `CLAUDE.md`, `README.md`, OpenSpec docs, test guidelines, or nearest area-specific instructions.
2. Read [bugfix-spec-workflow](references/bugfix-spec-workflow.md) before creating or changing OpenSpec bugfix artifacts, designing regression coverage, or deciding a bug is simple enough to fix without a change.
3. Reproduce or characterize the bug before editing. If reproduction is impossible, record the attempted commands/routes and narrow the claim.
4. Capture three contracts before implementation: current broken behavior, expected corrected behavior, and unchanged behavior that must continue to work.
5. Implement the smallest defensible fix, then verify the defect, the correction, and protected unchanged behavior.

Core contract:

```markdown
Current: WHEN [condition] THEN the system [incorrect behavior].
Expected: WHEN [condition] THEN the system SHALL [correct behavior].
Unchanged: WHEN [related condition] THEN the system SHALL CONTINUE TO [existing behavior].
```

## Defaults

- Use OpenSpec artifacts for complex, critical, cross-module, production-facing, security/auth/payment, data-contract, regression-prone, or explicitly requested bugfixes.
- Keep OpenSpec bugfix changes under the repository's normal change directory, usually `openspec/changes/<change-id>/`, with `proposal.md`, `design.md`, `tasks.md`, and `specs/<capability>/spec.md`.
- Do not create Kiro-specific artifacts by default. Adapt bugfix-spec concepts into the local OpenSpec files.
- Prefer `MODIFIED Requirements` for bugs in existing behavior. Use `ADDED Requirements` only when the fix creates a new durable contract.
- Treat tests as the executable bugfix spec: one check proves the defect, one proves the fix, and one protects unchanged behavior.
- Follow repo-specific quality gates exactly. If a repo has context routing, hooks, validation scripts, browser QA, or deployment proof requirements, run those instead of inventing new gates.
- Pair browser-visible reports with browser QA or responsive viewport evidence when the repository has that workflow.
- Keep security, auth, payment, and provider bugfixes explicit about what secrets, provider identifiers, raw payloads, debug state, or internal ids must not appear.

## Completion Check

Before declaring the bug fixed:

1. Run the targeted regression test and the repository's surfaced verification commands.
2. Run OpenSpec validation, usually `openspec validate <change-id> --strict`, when an OpenSpec change exists.
3. Report any reproduction, test, environment, or verification gap explicitly.
4. For completed OpenSpec bugfixes, preserve history using the repository's normal sync/archive flow; do not leave durable bugfix context only in chat.
