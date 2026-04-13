# Go Smell to Refactor Map

## Contents
- Package and API smells
- Interface and type smells
- Error smells
- Concurrency smells
- I/O and resource smells
- Testing and performance smells

## Package and API smells

- **Grab-bag package (`util`, `common`)**
  - Refactor: rename by domain, split by stable responsibility, move non-public code into `internal/`

- **Too many exported helpers**
  - Refactor: unexport helpers, keep only user-facing types and functions public

- **Public embedding leaks internals**
  - Refactor: replace embedding with named fields and explicit methods

- **Hidden global registration or `init()` side effects**
  - Refactor: move wiring into constructors or `main`

## Interface and type smells

- **Producer-owned interface for mocking**
  - Refactor: delete interface, return concrete type, define narrow interface in consumer if needed

- **Fat interface**
  - Refactor: split into smaller consumer-shaped interfaces

- **Returning interface needlessly**
  - Refactor: return concrete type

- **Pointer to interface**
  - Refactor: pass interface by value or pointer to concrete type

- **Generic abstraction without real duplication**
  - Refactor: delete type parameters, write concrete code, revisit later if duplication appears

- **Mixed receiver types**
  - Refactor: pick pointer or value receivers consistently

- **Shared mutable slice/map crossing boundaries**
  - Refactor: copy at boundary or document ownership explicitly

## Error smells

- **Panic in normal flow**
  - Refactor: return error

- **String matching on errors**
  - Refactor: `errors.Is`, `errors.As`, typed fields, or sentinel only when needed

- **Log and return**
  - Refactor: handle once at the right layer

- **Errors lack operation context**
  - Refactor: wrap with `%w` and operation name

## Concurrency smells

- **Fire-and-forget goroutine**
  - Refactor: give it an owner, shutdown path, and error channel or `errgroup`

- **Blocked send/receive with no cancellation**
  - Refactor: add `ctx.Done()` path or redesign ownership/backpressure

- **Receiver closes channel it does not own**
  - Refactor: move close responsibility to producer/owner

- **Unbounded fan-out**
  - Refactor: bound concurrency with worker pool or semaphore

- **Context in struct**
  - Refactor: pass `ctx` explicitly per call

## I/O and resource smells

- **HTTP response body not closed**
  - Refactor: `defer resp.Body.Close()` at the narrowest safe scope

- **Rows, statements, files not closed**
  - Refactor: explicit cleanup with `defer`

- **Transaction commit/rollback unclear**
  - Refactor: explicit happy path plus `defer tx.Rollback()` safety net

- **SQL string formatting**
  - Refactor: parameterized query

- **Path traversal assumptions**
  - Refactor: make directory boundary explicit and use traversal-resistant techniques appropriate to the toolchain

## Testing and performance smells

- **Mock-heavy tests distort design**
  - Refactor: test through real public APIs or small consumer seams

- **JSON string comparison in tests**
  - Refactor: decode and compare semantics

- **No race test on concurrent code**
  - Refactor: add `go test -race` to verification

- **Optimization without measurement**
  - Refactor: add benchmark/profile first

- **Repeated conversions or allocation churn in hot path**
  - Refactor: benchmark, preallocate, or simplify only where profiles support it
