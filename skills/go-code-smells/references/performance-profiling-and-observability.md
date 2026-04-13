# Performance, Profiling, and Observability Smells

## Contents
- Measure first
- Hot-path smells
- Profiling workflow
- Trace and blocking analysis
- PGO and modernization opportunities
- Observability smells

## Measure first

Performance refactors should be evidence-led.
Review order:
1. reproduce the complaint
2. benchmark or capture profiles
3. identify a dominant cost
4. choose the smallest fix
5. re-measure

Without evidence, many performance changes are just maintainability regressions in disguise.

## Hot-path smells

### `fmt` in tight loops without evidence it is acceptable
May be a smell in hot paths. Consider more direct conversions only after measurement.

### Repeated string-to-byte or byte-to-string conversions
Frequent in encoding and protocol code. Avoid repeated conversions when profiles show them as a cost.

### Missing preallocation on known sizes
When length is known or strongly bounded, preallocation can materially reduce allocations.

### Pooling without evidence
`sync.Pool` can help some workloads, but it complicates design.
Only introduce it when profiles show allocation pressure and object lifetimes fit the model.

### Micro-optimizing cold code
A smell because it adds complexity without measurable benefit.

## Profiling workflow

Prefer these tools:
- benchmarks with `-benchmem`
- CPU profiles
- memory profiles
- block and mutex profiles when contention is suspected
- traces for scheduler and lifecycle behavior

Suggested flow:
1. benchmark the candidate path
2. capture CPU and memory profiles
3. inspect hottest stacks and biggest allocators
4. patch the dominant cost
5. re-run the same benchmark/profile

## Trace and blocking analysis

Use tracing when the complaint is about:
- latency spikes
- scheduler behavior
- blocked goroutines
- work that does not stop promptly on cancellation

Tracing often reveals lifecycle and synchronization problems that plain CPU profiles miss.

## PGO and modernization opportunities

For binaries with stable production-like workloads, profile-guided optimization may help after basic algorithm and allocation issues are addressed.
Treat it as a later-stage improvement, not a substitute for code review.

Also review version-gated modernization opportunities when the toolchain supports them.
Newer library or tooling features can remove old workarounds and simplify code.

## Observability smells

### Logging instead of structured telemetry boundaries
Smell when logs are the only way to understand critical flows.
Add structure where it clarifies causality and operations.

### Missing context propagation in logs and traces
If request IDs, trace IDs, or deadlines disappear across boundaries, debugging concurrent systems becomes harder.

### High-cardinality log spam
A smell because it increases noise and cost without improving diagnosis.

### No metrics around queues, retries, or errors
If the system has concurrency or backpressure, it should expose enough signals to validate assumptions.
