# Refactoring Workflow for Go Code Smells

## Contents
- Scope the problem first
- Classify the code before changing it
- Build a smell inventory
- Choose the refactor shape
- Apply changes in a safe order
- Verify behavior and non-functional properties
- Produce the final review

## Scope the problem first

Before suggesting any change, answer these questions:
1. Is this private code, an `internal/` package, or a public library API?
2. Is the complaint about correctness, readability, performance, concurrency, operability, or testing?
3. Is the smell local to a function, or does it come from package boundaries and exported contracts?

If the user asks for a "Go idiomatic" review, default to a full pass across:
- package names and export surface
- interface placement
- error semantics
- context propagation
- goroutine lifetime and cleanup
- test quality
- performance evidence

## Classify the code before changing it

Different Go code wants different refactors:

### Library package
Optimize for:
- stable exported API
- small interfaces
- concrete return types
- strong documentation and error semantics
- avoiding hidden package state

### Service package
Optimize for:
- request lifecycle and context propagation
- cancellation and shutdown
- observability boundaries
- resource cleanup
- profile-backed performance improvements

### CLI package
Optimize for:
- clear `main`
- `os.Exit` or `log.Fatal` only in `main`
- thin wiring layer
- testable subcommands and pure helpers

### Worker/background system
Optimize for:
- bounded concurrency
- retry semantics
- shutdown order
- goroutine ownership
- leak resistance under partial failure

## Build a smell inventory

Name smells explicitly. Use categories rather than vague statements like "not idiomatic".

Recommended categories:
- Package and API smells
- Interface and type-system smells
- Error-handling smells
- Concurrency and lifecycle smells
- I/O and resource-management smells
- Testing smells
- Performance smells
- Security and trust-boundary smells

For each smell, capture:
- **Evidence:** exact code shape or behavior
- **Risk:** correctness, leak, compatibility, readability, security, performance
- **Root cause:** why the code got this way
- **Smallest fix:** what removes the smell with the least churn

## Choose the refactor shape

Prefer the least disruptive fix that removes the root cause.

### Shape 1: Local cleanup
Use when the smell is confined to a function or file.
Examples:
- rename variables and receivers
- split a long function
- replace string error matching with `errors.Is`
- add `defer rows.Close()`

### Shape 2: Package-boundary correction
Use when the smell comes from exports or dependency direction.
Examples:
- delete producer-owned interface
- return concrete type instead of interface
- move consumer-owned interface into the consuming package
- hide implementation in `internal/`

### Shape 3: Lifecycle correction
Use when the system fails under cancellation, shutdown, or load.
Examples:
- thread `ctx` through the call graph
- add owner-driven goroutine shutdown
- make channel close responsibility explicit
- bound fan-out or introduce backpressure

### Shape 4: Measurement-backed optimization
Use only when there is measured evidence.
Examples:
- preallocate slices in a hot path
- replace repeated `fmt.Sprintf` in a benchmarked loop
- remove repeated string/byte conversions
- add pooling only after profile evidence

## Apply changes in a safe order

Recommended order:
1. Make naming, ownership, and cleanup explicit.
2. Narrow exported surface and move interfaces if needed.
3. Fix concurrency and resource lifecycle.
4. Improve tests to lock behavior.
5. Apply performance changes only after measurement.

This order reduces the chance that benchmark or readability work hides a deeper lifecycle bug.

## Verify behavior and non-functional properties

### Always run
- formatting
- package tests
- race detector when concurrency is involved
- `go vet`

### Run when available
- Staticcheck
- golangci-lint
- fuzz tests for parsers or boundary decoders
- benchmarks for hot paths
- profiles or traces for latency/allocation regressions

### What success looks like
- behavior unchanged except for the intended bug fix
- no new exports unless justified
- clearer ownership of cleanup and lifetime
- tests fail in a useful, stable way
- performance claims supported by numbers

## Produce the final review

End with:
1. smell list ordered by risk
2. patch or diff
3. verification commands
4. compatibility notes
5. follow-up items intentionally deferred

A strong Go refactor review should answer:
- What did we simplify?
- What ownership became explicit?
- What public commitments did we avoid or improve?
- What evidence says the change is safe?
