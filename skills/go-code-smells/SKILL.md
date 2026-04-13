---
name: go-code-smells
description: Identifies and refactors Go code smells in libraries, services, CLIs, and modules. Use when the user asks to review Go code, clean up packages or APIs, fix context, error, goroutine, channel, or test issues, remove interface or abstraction overdesign, or improve performance without changing behavior.
license: MIT
metadata:
  compatibility: Go module repositories. Works best with repository access and ability to run gofmt, go test, go vet, and optional analyzers such as staticcheck or golangci-lint.
  author: ByAxe Datamola
  version: 1.0.0
  category: software-development
  tags:
    - go
    - golang
    - refactoring
    - code-smells
    - concurrency
    - api-design
    - testing
    - performance
---

# Go Code Smells

Use this skill to **diagnose**, **explain**, and **refactor** Go code smells in a way that matches how strong Go teams actually review code.

This skill is optimized for:
- Go libraries, services, CLIs, workers, and internal packages
- Refactors that must preserve behavior and keep diffs reviewable
- Go-native design questions: packages, exported APIs, interfaces, errors, context, goroutines, channels, testing, and performance

## Core idea

Analyze Go code **package-first, API-first, and lifecycle-first**.

In Go, many of the highest-leverage smells are not classic OO smells. They show up as:
- unclear package boundaries
- exported APIs that lock callers into bad abstractions
- interface pollution
- context misuse
- goroutine and resource leaks
- muddled error semantics
- hidden ownership of slices, maps, channels, and cleanup

## Operating rules

Follow these rules unless the user explicitly asks for a different trade-off:

1. **Preserve behavior first.** Prefer minimal, reviewable changes over rewrites.
2. **Prefer deletion and simplification.** In Go, fewer layers often means better design.
3. **Review package boundaries before local cleverness.** A bad exported API causes more damage than an ugly private helper.
4. **Prefer concrete types by default.** Introduce interfaces only when they model a real consumer need, boundary, or protocol.
5. **Keep goroutine lifetime obvious.** Every goroutine should have a clear owner, exit path, and cancellation story.
6. **Treat context as a parameter, not ambient state.** Pass `ctx` explicitly; do not hide it in structs or global state.
7. **Handle errors deliberately.** Return errors for normal failure, wrap with meaning, and avoid string-based error checks.
8. **Measure before optimizing.** Use benchmarks, profiles, and traces before recommending performance changes.
9. **Keep public APIs stable unless the user asks for a breaking change.** Narrow exports when possible, but do not break callers casually.
10. **Always include verification.** Formatting, tests, race detection, vet, and static analysis are part of the refactor.

## Workflow checklist

Copy and follow this checklist for each request:

```text
Go refactor checklist
- [ ] Identify code kind: library, service, CLI, worker, or internal package
- [ ] Determine stability constraints: private code, internal package, or public API
- [ ] Note any version-gated features only if they materially affect the advice
- [ ] Inventory smells by category: package/API, interfaces/types, errors, concurrency, I/O, tests, performance, security
- [ ] Pick the smallest refactor that removes the highest-risk smell first
- [ ] Apply the change file-by-file with explicit ownership and cleanup semantics
- [ ] Add or update tests only where regressions are plausible
- [ ] Verify: gofmt, go test, go test -race, go vet, static analysis; benchmark/profile when relevant
- [ ] Summarize preserved behavior, remaining risks, and deferred work
```

## What to ask from the user

If context is missing, ask for the smallest missing piece and proceed with grounded assumptions.

Prefer these questions, in order:
1. What is the scope: one file, one package, or a wider module?
2. Is this a library, service, or CLI, and is the public API allowed to change?
3. Are there Go version constraints or CI/tooling constraints that matter?

If the user gives only a snippet, assume:
- the code belongs to a normal Go module
- behavior and public API should stay stable
- modern stable Go idioms are preferred
- version-gated features should be suggested only when clearly beneficial

## Output contract

When providing a refactor, produce these sections in this order:

1. **Smells found**
   - name, evidence, risk, root cause
2. **Refactor plan**
   - 3–7 steps, smallest valuable step first
3. **Patch**
   - updated code or diff, with file paths
4. **Verification**
   - exact commands and what success looks like
5. **Risk notes**
   - compatibility, concurrency, or rollout risks
6. **Follow-ups**
   - optional improvements intentionally deferred

## Smell navigation

Use progressive disclosure. Keep the response focused and pull deeper material only when needed.

- Full smell catalog: `references/smell-catalog.md`
- Classical smells translated into Go, including SOLID-through-Go: `references/classical-smells-through-go.md`
- Review workflow and decision tree: `references/refactoring-workflow.md`
- Package, module, and exported API design: `references/package-and-api-design.md`
- Interfaces, generics, receivers, data ownership: `references/interfaces-generics-and-type-design.md`
- Errors, panics, wrapping, and control flow: `references/errors-and-control-flow.md`
- Context, goroutines, channels, synchronization: `references/concurrency-context-and-lifecycles.md`
- HTTP, database, filesystem, JSON, and resource cleanup: `references/http-database-and-io-smells.md`
- Testing, race detection, fuzzing, benchmarks: `references/testing-benchmarks-and-fuzzing.md`
- Performance, pprof, trace, observability: `references/performance-profiling-and-observability.md`
- Security and hardening smells: `references/security-and-hardening.md`
- Toolchain, analyzers, and quality gates: `references/toolchain-and-quality-gates.md`
- Version-gated modernization opportunities: `references/version-gated-modernization.md`
- Quick smell-to-refactor map: `references/smell-to-refactor-map.md`
- Review checklists: `references/checklists.md`
- Sources and further reading: `references/sources.md`

## Refactoring heuristics

### Prioritize by risk

Sort findings by:
1. **Correctness and data integrity** — wrong behavior, silent corruption, broken transactions, invalid ownership
2. **Concurrency and lifecycle** — goroutine leaks, blocked channels, missing cancellation, races
3. **Public API design** — bad exports, interface pollution, package coupling, compatibility traps
4. **Security and trust boundaries** — SQL injection, path traversal, unsafe randomness, permissive decoding
5. **Maintainability** — giant packages, duplicated flows, config sprawl, hidden global state
6. **Performance** — only after measurement or obvious hot-path evidence

### Choose the smallest effective refactor

Prefer these moves, in order:
- rename for clarity and remove dead code
- extract a private helper or small private type
- narrow the exported surface
- move an interface to the consumer and return a concrete type
- make ownership explicit for `ctx`, closers, channels, slices, and maps
- replace global state with constructor injection or explicit parameters
- split a package only when import direction or mental model demands it
- split a module only when release boundaries are genuinely independent

### Avoid these by default

Do **not** recommend these unless the user explicitly asks or the evidence is overwhelming:
- creating an interface for every concrete type
- introducing generics before proven duplication exists
- enterprise-style layer multiplication with no boundary benefit
- turning closed `switch` statements into open polymorphism just on principle
- broad folder or module rewrites that bury the real fix

## Common verification commands

If a repository exists, prefer:
- `gofmt -l .` or the helper script in `scripts/run_quality_gates.sh`
- `go test ./...`
- `go test -race ./...`
- `go vet ./...`
- `staticcheck ./...` if available
- `golangci-lint run` if configured

If performance is involved:
- `go test -run '^$' -bench . -benchmem ./...`
- capture CPU and memory profiles with `scripts/profile_hot_path.sh`
- inspect with `go tool pprof` and `go tool trace`

## Troubleshooting patterns

### User says: "There are too many interfaces"
- First ask whether those interfaces exist on the producer side.
- Prefer deleting implementor-owned interfaces, returning concrete types, and defining a narrow interface only in the consuming package.
- Consult: `references/interfaces-generics-and-type-design.md`

### User says: "We leak goroutines" or "this hangs under load"
- Treat as a lifecycle bug, not just a style issue.
- Audit channel ownership, blocking sends/receives, cancellation, shutdown order, and tests under `-race`.
- Consult: `references/concurrency-context-and-lifecycles.md`

### User says: "Error handling is messy"
- Check for panic in normal flow, log-and-return duplication, string matching on errors, lost wrapping, and undocumented semantics.
- Consult: `references/errors-and-control-flow.md`

### User says: "This package is impossible to test"
- Look for globals, `init()` side effects, hidden singletons, producer-owned interfaces for mocking, and API boundaries that do not expose real seams.
- Consult: `references/package-and-api-design.md` and `references/testing-benchmarks-and-fuzzing.md`

### User says: "This is slow"
- Do not redesign blindly.
- Ask for the hot path, benchmark it, profile it, then choose the smallest measurable improvement.
- Consult: `references/performance-profiling-and-observability.md`

## Examples

### Example 1: API cleanup
User: "Review this Go package and reduce abstraction overhead."
Action: inventory exported symbols, delete unnecessary interfaces, return concrete types, keep public behavior stable, and verify with tests plus static analysis.

### Example 2: Concurrency bug
User: "Our worker pool sometimes deadlocks on shutdown."
Action: trace goroutine ownership, channel close direction, cancellation propagation, and blocking paths; patch shutdown sequencing and verify with race tests.

### Example 3: Error design
User: "Make this library's errors more idiomatic."
Action: replace panic/strings with wrapped errors, typed or sentinel errors only where callers need branching, and update tests to use `errors.Is`/`errors.As`.

### Example 4: Performance review
User: "Find performance smells in this Go service."
Action: focus on measured hotspots, allocation patterns, repeated conversions, preallocation, and profile-backed fixes rather than speculative micro-optimizations.

## Trigger test suite

These should trigger:
- "Find code smells in this Go package"
- "Refactor this Go service without changing behavior"
- "Why do we have so many interfaces in this repo"
- "Fix context misuse or goroutine leaks"
- "Review our error handling and public API design"
- "Make this Go code more idiomatic and maintainable"

These should not trigger:
- "Write a SQL query"
- "Help me with React hooks"
- "Summarize this article"
- "Generate a vacation itinerary"
