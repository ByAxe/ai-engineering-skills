# Bugfix Spec Workflow

Use this workflow to adapt bugfix-spec practice to an OpenSpec repository. It does not require Kiro and should not create Kiro-only files by default.

## Source Principles

- Keep the three-phase shape: bug analysis or requirements, design, then tasks.
- Use review gates when requirements, design, or regression risk are unclear; a one-pass draft is only acceptable for well-understood low-risk defects.
- Analyze the bugfix contract before design when ambiguity is costly: conflicting constraints, undefined terms, missing failure modes, and edge cases.
- Write requirements and scenarios so they are testable and traceable into tasks.
- Make tasks dependency-aware. Independent tasks can proceed in parallel only after prerequisites are satisfied.
- Prefer property-style tests for universal contracts, but choose the local test form that best expresses the behavior.

## Intake

First establish whether the work needs an OpenSpec change.

Use an OpenSpec bugfix change when any of these are true:

- The user asks for OpenSpec, a spec, a proposal, or a documented bugfix.
- The bug is user-visible, security-sensitive, payment/auth-related, data-contract related, or production-facing.
- The fix crosses modules, changes a durable contract, or has non-obvious regression risk.
- Previous fixes or tests failed to protect the behavior.
- The root cause is unclear and the investigation itself needs to be reviewable.

For a tiny local typo or isolated test expectation with no durable contract change, it is acceptable to fix directly, but still capture the current/expected/unchanged behavior in the work notes or final response.

## Bugfix Contract

Before editing code, write or hold these three statements:

```markdown
Current behavior (defect):
- WHEN [condition or reproduction step]
- THEN the system [incorrect behavior]

Expected behavior (correct):
- WHEN [same condition]
- THEN the system SHALL [correct behavior]

Unchanged behavior (regression protection):
- WHEN [related condition]
- THEN the system SHALL CONTINUE TO [existing behavior]
```

Use these statements to choose tests and scope. The third statement is the guard against broad fixes that silently break neighboring behavior.

## OpenSpec Mapping

Create or update local OpenSpec files under the repository's change directory, usually:

```text
openspec/changes/<change-id>/
├── proposal.md
├── design.md
├── tasks.md
└── specs/<capability>/spec.md
```

Use short, bug-focused change ids, such as `fix-payment-result-advisory`, `dedupe-signed-out-access-copy`, or `harden-auth-logout-fallback`.

Kiro's `bugfix.md` analysis maps locally to the combination of `proposal.md` plus the `Context`, `Root Cause`, and `Regression Strategy` sections in `design.md`. Do not add a separate `bugfix.md` unless the repository standardizes on one.

### proposal.md

Use the proposal to explain the observed defect, intended correction, and impact:

```markdown
## Why

[Observed defect with route, command, file, screenshot, issue, or test evidence.]

## What Changes

- Fix [specific behavior].
- Preserve [unchanged behavior].
- Add regression coverage for [defect/correct/unchanged matrix].
- No [explicit non-goal or adjacent behavior] changes.

## Capabilities

### New Capabilities

- None. [Usually true for bugfixes.]

### Modified Capabilities

- `<capability>`: [contract tightened or corrected].

## Impact

- Affected code: [...]
- Affected tests: [...]
- Affected specs: [...]
- No [API/database/provider/config/etc.] changes.
```

### design.md

Use the design for root cause and scope control:

```markdown
## Context

[How the current implementation reaches the defect.]

## Goals / Non-Goals

**Goals:**
- [Correct behavior.]
- [Regression preservation.]

**Non-Goals:**
- [Adjacent refactor or product change excluded.]

## Root Cause

[Specific cause with file/function/test evidence. Explain why existing tests missed it.]

## Decisions

1. [Smallest fix choice.]
   - Rationale: [...]
   - Alternative rejected: [...]

## Regression Strategy

- Defect proof: [...]
- Correctness proof: [...]
- Unchanged behavior proof: [...]

## Spec Sanity Pass

- Ambiguities resolved: [...]
- Conflicting constraints checked: [...]
- Missing edge cases added or intentionally excluded: [...]
- Undefined terms avoided or defined: [...]

## Risks / Trade-offs

- [Risk] -> [Mitigation]
```

Use a longer design only when the bug spans multiple surfaces or the fix choice is debatable. For copy/layout-only bugs, a compact design is enough.

### specs/<capability>/spec.md

The delta spec describes desired durable behavior, not the broken implementation.

Use `MODIFIED Requirements` when tightening an existing capability:

```markdown
## MODIFIED Requirements

### Requirement: [Existing requirement name]

[Updated normative behavior. Include the corrected behavior and the protected unchanged behavior.]

#### Scenario: [Defect no longer occurs]

- **WHEN** [condition]
- **THEN** [correct outcome]
- **AND** [old incorrect behavior is absent]

#### Scenario: [Neighboring behavior continues]

- **WHEN** [related existing condition]
- **THEN** the system SHALL CONTINUE TO [existing outcome]
```

Use `ADDED Requirements` only when the fix creates a new durable capability or guardrail.

### tasks.md

Task order should force evidence before implementation and make dependencies explicit:

```markdown
## 1. Reproduction And Root Cause

- [ ] 1.1 Reproduce the defect with [command/route/test].
  Depends: none. Blocks: regression coverage and fix. Verify: [exact command/evidence].
- [ ] 1.2 Identify the root cause with file/function evidence.
  Depends: 1.1. Blocks: design decision. Verify: [file/function/test evidence recorded].

## 2. Regression Coverage

- [ ] 2.1 Add a test or fixture that fails on the current defect.
  Depends: 1.1. Blocks: implementation. Verify: fails on the pre-fix behavior or is documented from captured evidence.
- [ ] 2.2 Add or update coverage for the corrected behavior.
  Depends: 1.2. Blocks: completion. Verify: targeted test command.
- [ ] 2.3 Add or update coverage for unchanged neighboring behavior.
  Depends: 1.2. Blocks: completion. Verify: targeted test command.

## 3. Fix

- [ ] 3.1 Implement the smallest scoped fix.
  Depends: 2.1. Blocks: final verification. Verify: defect regression passes.
- [ ] 3.2 Avoid unrelated refactors unless the root cause is duplicated logic and the design explicitly accepts that scope.
  Depends: 3.1. Blocks: final verification. Verify: diff review.

## 4. Verification

- [ ] 4.1 Run OpenSpec validation.
- [ ] 4.2 Run targeted tests.
- [ ] 4.3 Run repository verification commands for changed paths.
```

Use `Depends`, `Blocks`, and `Verify` lines when the task graph is non-trivial. This keeps the change readable for human review and future multi-agent execution.

## Regression Test Matrix

Every non-trivial bugfix needs this matrix, even when the tests are not property-based:

| Proof | Purpose | Common forms |
| --- | --- | --- |
| Defect proof | Demonstrate the old behavior is real | Failing browser case, function test, golden fixture diff, screenshot/route evidence |
| Correctness proof | Demonstrate the fixed behavior | Targeted assertion, status/copy check, API contract test, locale pair |
| Unchanged proof | Prevent collateral damage | Existing state variant, neighboring route, safe fallback, old invariant, responsive viewport |

Property-based tests are useful when the domain is a pure function, parser, validator, or state machine. Do not force property tests onto browser flows where route tests, fixtures, or golden vectors express the property better.

## Property Candidates

Consider property-style checks when the bug concerns:

- URL/path validators, parsers, serializers, mappers, or reducers.
- Idempotency, ordering, concurrency, or bounded retry behavior.
- Sanitization contracts where many hostile inputs should share the same safe outcome.
- Locale or route generation where a finite matrix can be generated from a source table.

Use generated or table-driven tests when that gives stronger coverage than one example, but keep the failing example that reproduced the original bug.

## Bugfix Patterns To Preserve

- Copy bugfixes should assert the replacement copy and the absence of the old copy.
- Payment result fixes must keep server truth as the source of positive paid state; URL advisory state must not unlock access.
- Auth and provider fixes must preserve safe local fallback behavior and sanitized metadata when provider proof is unavailable.
- Frontend script hardening should fix verified bugs in place unless the design proves a refactor is the smallest safe root-cause fix.
- Browser-visible bugs need browser or viewport evidence across the relevant route and viewport. Use the repository's browser QA workflow when available.
- Security, auth, and payment specs should explicitly say what secrets, provider ids, internal order ids, debug states, or raw payloads must not appear.
- If mocks caused the bug to survive, add at least one assertion against the real contract value or a golden vector shared with the real implementation.

## Gotchas

- Do not write the broken current behavior as a target OpenSpec requirement. Put the defect in `proposal.md` or `design.md`; put the corrected contract in `spec.md`.
- Do not let a bugfix become a broad cleanup. If structural debt is real but not required for the fix, name it as a non-goal or follow-up.
- Do not use a one-pass spec draft for critical, unfamiliar, compliance-sensitive, auth, payment, or security defects; explicitly review the contract and design first.
- Do not skip reproduction because the fix seems obvious. If reproduction is impossible, report the attempts and block or narrow the claim.
- Do not rely only on snapshots for semantic bugs. Assert the contract directly.
- Do not change API, database, provider, deployment, or environment behavior unless the root cause requires it and the OpenSpec impact section says so.
- Do not declare success until repository verification commands and the targeted regression have run, or until any skipped command is explicitly justified.

## Completion And Spec History

For a completed OpenSpec bugfix, prefer the repository's archive/history-preserving flow over syncing specs only.

Main specs should contain the durable corrected behavior and any protected unchanged behavior that remains part of the capability contract. The archived change should preserve the bugfix history: observed broken behavior, root cause, goals and non-goals, design decisions, regression strategy, task proof, and verification evidence.

Use sync-only as an interim operation when a change must remain active but main specs need the delta early. Do not treat sync-only as the final history-preserving step for a completed bugfix.

## Final Report Shape

When finishing a bugfix, report:

- The root cause in one sentence.
- The scoped fix.
- The regression tests or evidence that cover defect, correctness, and unchanged behavior.
- The verification commands run.
- Any residual risk or unverified environment.
