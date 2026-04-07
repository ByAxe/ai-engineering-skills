# Formula Hierarchy and Quality Tiers

Gas Town formulas are TOML-based workflow definitions that control how polecats work. They compose through three mechanisms:

## Composition Mechanisms

### Extends
A formula inherits all steps from a parent and can override or add steps.
```toml
extends = ["shiny"]
```

### Expand
Replaces a single step with a multi-step expansion.
```toml
[compose]
[[compose.expand]]
target = "implement"
with = "rule-of-five"
```

### Aspect
Cross-cutting concern that wraps steps with pre/post behavior.
```toml
[compose]
[[compose.aspect]]
apply = "security-audit"
```

## Formula Types

### workflow
Sequential steps with dependencies, orchestrated by a single agent. Can spawn sub-convoys for parallel work.
- `shiny`, `shiny-enterprise`, `shiny-secure`
- `mol-idea-to-plan`, `mol-polecat-work`

### convoy
Parallel execution with multiple polecats, each working on a separate leg. Results synthesized.
- `code-review` (10 legs), `design` (6 legs), `mol-prd-review` (6 legs)

### expansion
Replaces a single step in a parent formula with multiple sub-steps.
- `rule-of-five` (5 refinement passes), `tdd-cycle` (red-green-refactor)

### aspect
Cross-cutting behavior applied before/after steps.
- `security-audit` (OWASP, SAST, secrets scanning)

## Quality Tier Details

### mol-polecat-work (Default)
The baseline work formula. Steps:
1. Load context and verify assignment
2. Set up branch
3. Implement the work
4. Run gate commands (test, lint, build, typecheck)
5. Pre-verify (rebase onto target + full gate suite)
6. Submit via `gt done`

Gate commands are configured per-rig in settings.

### shiny — "Engineer in a Box"
Five mandatory steps:
1. **design** — Architecture doc: approach, trade-offs, files to change
2. **implement** — Code following the design, no gold-plating
3. **review** — Self-review: bugs, readability, security
4. **test** — Unit tests, integration tests, full suite, no regressions
5. **submit** — Clean git status, clear commit message

### shiny-enterprise — Rule of Five
Extends shiny, expands implement into 5 passes:
1. **Draft** — Initial attempt, breadth over depth
2. **Refine (correctness)** — Fix errors, bugs, logic issues
3. **Refine (clarity)** — Simplify, make readable for others
4. **Refine (edge-cases)** — What could go wrong? What's missing?
5. **Refine (excellence)** — Final polish, something to be proud of

### shiny-secure — Security Audit
Extends shiny, wraps implement and submit with security checks:
- Pre-implementation: Secrets/credentials review, dependency CVE check
- Post-implementation: SAST scan, OWASP Top 10 review
- Pre-submission: Final vulnerability scan

### mol-polecat-work-monorepo-tdd — TDD Cycle
Extends mol-polecat-work, replaces implement with:
1. **Write failing tests** — Commit tests FIRST (defense against manipulation)
2. **Verify red** — HARD GATE: at least one test must fail
3. **Implement** — Minimal code to pass tests (no modifying test files)
4. **Verify green** — HARD GATE: full suite must pass, zero regressions
5. **Refactor** — Clean up while maintaining green

## Code Review Convoy (10 Parallel Legs)

The `code-review` formula spawns specialized reviewers:

**Analysis legs:**
- correctness — logic errors, race conditions, edge cases
- performance — bottlenecks, O(n^2), N+1 queries
- security — OWASP, injection, hardcoded secrets
- elegance — SOLID, abstraction quality, design clarity
- resilience — error handling, timeouts, circuit breakers
- style — conventions, naming, formatting

**Verification legs:**
- wiring — installed but unused dependencies
- commit-discipline — atomicity, message quality
- test-quality — meaningful tests vs coverage theater
- smells — anti-patterns, DRY violations, deep nesting

**Presets:**
- `gate` — light (wiring, security, smells, test-quality)
- `full` — all 10 legs
- `security-focused` — security, resilience, correctness, wiring
- `refactor` — elegance, smells, style, commit-discipline
