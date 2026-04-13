# Testing, Benchmarks, Fuzzing, and Deterministic Concurrency Tests

## Contents
- Test-design principles
- Common unit-test smells
- Helpful failure output
- Mocking and seam design
- Race detection
- Fuzzing
- Benchmarks and hot-path tests
- Deterministic concurrency testing

## Test-design principles

Good Go tests usually favor:
- ordinary Go code over assertion DSLs
- stable semantic comparisons over brittle string comparisons
- public API testing over architecture-driven mocking
- simple table-driven tests when the same logic repeats

## Common unit-test smells

### Assertion-library dependence
Smell when the test becomes a mini language of chained assertions that hides the actual failure.
Prefer plain Go conditions and clear failure messages.

### Comparing individual fields one by one when full structure comparison is clearer
When the return value is a struct, map, or slice, compare the whole value when possible and use diffs for readability.

### Comparing unstable strings or serialized output
Smell when tests assume exact formatting or JSON serialization details that are not semantically important.
Compare decoded structures or semantic content.

### Error string comparisons
Use `errors.Is`, `errors.As`, or typed data where the test is about semantics rather than wording.

### Index-based subtests with unreadable names
Subtest names should describe the scenario. Do not make humans count table indexes.

### Helpers without `t.Helper()`
When a helper receives `*testing.T`, mark it as a helper so failures point to the call site.

## Helpful failure output

Strong default pattern:
- function name
- relevant input
- got before want
- diff when comparing structures

Prefer keeping tests going with `t.Error` when multiple checks can fail independently.
Reserve `t.Fatal` for setup failure or situations where the current case cannot continue.

## Mocking and seam design

A common Go testing smell is architecture driven by mocks instead of behavior.
Look for:
- producer-owned interfaces created only for tests
- many generated mocks for concrete code that could be tested through the real API
- tests that lock the order of internal calls instead of observable behavior

Prefer:
- small consumer-owned interfaces where a seam is truly needed
- in-memory or real lightweight implementations
- tests through public behavior when possible

## Race detection

Run `go test -race ./...` whenever concurrency matters.
The race detector only finds races on executed paths, so increase coverage or run realistic workloads when needed.

## Fuzzing

Fuzzing is especially valuable for:
- parsers
- decoders
- protocol handling
- boundary validation
- data structure invariants

Add fuzz tests where input space is large and edge cases are easy for humans to miss.

## Benchmarks and hot-path tests

Use benchmarks when making performance claims.
Benchmarks should:
- isolate the operation of interest
- use representative input sizes
- report allocations via `-benchmem`
- avoid extra work inside the benchmark body

For repositories on newer toolchains, consider the newer benchmark loop API where it improves clarity or removes setup-measurement footguns.
Do not churn stable benchmarks just for style.
Benchmark design matters more than benchmark volume.

## Deterministic concurrency testing

For tricky concurrent or time-based code, deterministic concurrency testing can be a big improvement over sleep-based tests.
Use version-gated guidance:
- if the project uses a toolchain with stable support, prefer deterministic facilities for concurrent tests where appropriate
- otherwise, avoid fragile sleep-driven tests and isolate time/cancellation seams carefully

For concrete version guidance on benchmark loops and deterministic concurrency tests, see `references/version-gated-modernization.md`.

## Suggested verification commands

- `go test ./...`
- `go test -race ./...`
- `go test -run '^$' -bench . -benchmem ./...`
- `go test -fuzz=Fuzz -run '^$' ./...` when fuzz targets exist
