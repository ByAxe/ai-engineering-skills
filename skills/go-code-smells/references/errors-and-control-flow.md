# Errors and Control Flow Smells

## Contents
- Error model
- Smells in ordinary error handling
- Wrapping and inspection
- Sentinel vs typed vs opaque errors
- Panic boundaries
- Exit paths and `main`
- Refactoring patterns

## Error model

In Go, errors are values.
That means reviews should ask:
- what decision will the caller make with this error?
- does the error preserve enough context?
- is the code handling the error once, at the right level?

## Smells in ordinary error handling

### Panic for expected failure
Smell when libraries or ordinary functions panic for validation, I/O, network, parse, or dependency failures.

Preferred fix:
- return an error
- reserve panic for broken invariants or truly unrecoverable programmer errors inside a package boundary

### Log and return the same error
Smell when lower layers log an error and then return it, causing duplicate logs upstream.

Preferred fix:
- either handle it locally and stop propagation
- or return it with context and let one higher layer log or render it

### String matching on errors
Smell when code uses `err.Error()` text to decide behavior.

Preferred fix:
- `errors.Is`
- `errors.As`
- documented sentinel or typed errors only when callers genuinely need branching

### Lost context
Smell when the returned error hides which operation failed.

Preferred fix:
- wrap with operation context using `%w`
- keep messages short and actionable

## Wrapping and inspection

Use wrapping when the higher layer can add useful context.
Examples:
- `fetch user profile`
- `open cache manifest`
- `commit transaction`

Inspection guidance:
- use `errors.Is` for semantic classes and sentinels
- use `errors.As` for typed data
- use `errors.Join` when multiple failures matter together

Avoid exposing implementation-specific low-level errors directly unless callers truly need them.

## Sentinel vs typed vs opaque errors

### Sentinel errors
Use when callers must branch on one stable condition.
Keep the set small.

### Typed errors
Use when callers need structured fields, not string parsing.
Examples:
- path, offset, kind, temporary/permanent classification

### Opaque wrapped errors
Use when callers mostly need a good message or logging context, not branching.

Smell: sentinel proliferation.
If a package accumulates many sentinels, ask whether the API is leaking implementation detail.

## Panic boundaries

Panic is acceptable for:
- internal invariant violations
- impossible states caused by programmer error
- truly unrecoverable situations within a package boundary

Smell when panic crosses a package API boundary as ordinary behavior.
If panic is used internally, recover at the public boundary and convert to an error only when that is part of the design.

## Exit paths and `main`

Keep `os.Exit` and `log.Fatal` in `main`.
All other code should normally return errors.
This keeps libraries testable and preserves cleanup opportunities.

## Refactoring patterns

### From string matching to semantic handling
Before:
- compare `err.Error()` to text

After:
- introduce sentinel or typed error only if a stable branch is needed
- otherwise wrap and log once higher up

### From panic-driven library to error-returning library
Before:
- `MustParseConfig` used throughout business code

After:
- `ParseConfig` returns error
- `Must...` kept only at process startup or in tests where failure should abort immediately

### From noisy errors to actionable ones
Before:
- `return err`

After:
- `return fmt.Errorf("load tenant policy: %w", err)`

### From duplicate handling to single responsibility
Before:
- lower layer logs and returns
- upper layer logs and returns again

After:
- lower layer wraps and returns
- boundary layer decides logging, status code, retry, or user message
