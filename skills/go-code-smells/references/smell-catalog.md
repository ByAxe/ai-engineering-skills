# Go Code Smell Catalog

## Contents
- Package and module smells
- API and interface smells
- Type and data ownership smells
- Error and control-flow smells
- Concurrency and lifecycle smells
- I/O and resource-management smells
- Testing smells
- Performance and observability smells
- Security smells
- Readability and documentation smells

## Package and module smells

### 1. Grab-bag package
**Symptoms:** package names like `util`, `common`, `misc`, or `helpers`; unrelated exports bundled together.

**Why it hurts:** users cannot infer purpose; dependencies sprawl; packages change for unrelated reasons.

**Preferred refactor:** rename by domain or split by stable responsibility. Use `internal/` for implementation detail.

### 2. Package stutter
**Symptoms:** `cache.CacheClient`, `yamlconfig.ParseYAMLConfig`, `auth.AuthenticatorInterface`.

**Why it hurts:** noisy call sites and weak naming.

**Preferred refactor:** shorten exports so package + identifier reads naturally.

### 3. Giant package with many unrelated exports
**Symptoms:** one package owns domain logic, transport code, persistence, retries, and formatting.

**Why it hurts:** hard to test, reason about, or evolve.

**Preferred refactor:** separate by real boundary, not by arbitrary folder layer.

### 4. Premature multi-module split
**Symptoms:** many `go.mod` files inside one repo with tightly coupled releases.

**Why it hurts:** more release and tooling overhead without a real boundary.

**Preferred refactor:** collapse to one module unless release cadence and versioning truly differ.

### 5. Hidden `init()` behavior
**Symptoms:** registration, I/O, goroutine startup, or global mutation in `init()`.

**Why it hurts:** hidden side effects, test order problems, poor startup control.

**Preferred refactor:** move wiring to constructors or `main`.

## API and interface smells

### 6. Producer-owned interface for mocking
**Symptoms:** `type Client interface {...}` next to `type client struct {...}` with one implementation.

**Why it hurts:** locks callers into abstraction too early; grows shotgun surgery across mocks and wrappers.

**Preferred refactor:** export the concrete type; let consumers define narrow interfaces if needed.

### 7. Fat interface
**Symptoms:** many methods, hard-to-implement mocks, callers use only a subset.

**Why it hurts:** weak abstraction, difficult testing, accidental coupling.

**Preferred refactor:** smaller consumer-shaped interfaces.

### 8. Returning interface unnecessarily
**Symptoms:** `New()` returns `Service` interface even though only one implementation exists.

**Why it hurts:** callers lose methods and API evolution flexibility.

**Preferred refactor:** return concrete type.

### 9. Public embedding leaks internals
**Symptoms:** exported structs embed mutexes, transports, or implementation types.

**Why it hurts:** callers couple to internals; unsafe method surface leaks into API.

**Preferred refactor:** explicit fields or wrapping methods.

### 10. Constructor option soup
**Symptoms:** many booleans, strings, or loosely related args.

**Why it hurts:** unreadable call sites and invalid combinations.

**Preferred refactor:** clear required parameters plus config struct or functional options when justified.

## Type and data ownership smells

### 11. Mixed receiver types
**Symptoms:** same type uses both value and pointer receivers without a strong reason.

**Why it hurts:** confusing method sets and mutation semantics.

**Preferred refactor:** pick one receiver model.

### 12. Passing pointers only to avoid tiny copies
**Symptoms:** `*string`, `*int`, `*io.Reader` without mutation need.

**Why it hurts:** extra indirection and muddled ownership.

**Preferred refactor:** pass values or interfaces by value.

### 13. Shared mutable slices or maps across boundaries
**Symptoms:** constructors store caller slices directly; getters return internal maps directly.

**Why it hurts:** surprising aliasing and integrity bugs.

**Preferred refactor:** copy at boundaries or document transferred ownership clearly.

### 14. `time.Time` compared with `==`
**Symptoms:** equality checks on time values that are really about the same instant.

**Why it hurts:** location and monotonic-clock details can make direct comparison misleading.

**Preferred refactor:** use `Equal` for instant equality.

### 15. Invalid zero value with no guardrail
**Symptoms:** exported struct looks easy to instantiate but must be initialized in a special way.

**Why it hurts:** invalid states leak into callers.

**Preferred refactor:** make fields private or explicitly design for a useful zero value.

## Error and control-flow smells

### 16. Panic for normal errors
**Symptoms:** parsing, I/O, validation, or dependency failures panic.

**Why it hurts:** untestable APIs and poor control flow.

**Preferred refactor:** return errors.

### 17. String matching on errors
**Symptoms:** `strings.Contains(err.Error(), "timeout")`.

**Why it hurts:** brittle semantics tied to wording.

**Preferred refactor:** `errors.Is`, `errors.As`, or typed data.

### 18. Log and return
**Symptoms:** lower layers log an error and return it for higher layers to log again.

**Why it hurts:** duplicate noise and blurred responsibility.

**Preferred refactor:** handle once, at the right level.

### 19. Error wrapping without actionable context
**Symptoms:** raw errors bubble up with no operation name.

**Why it hurts:** poor diagnosis in production.

**Preferred refactor:** wrap with short operation context using `%w`.

### 20. Sentinel explosion
**Symptoms:** many public sentinel errors for low-level details.

**Why it hurts:** public API becomes too implementation-specific.

**Preferred refactor:** keep only stable semantic sentinels; use opaque wrapping elsewhere.

## Concurrency and lifecycle smells

### 21. Fire-and-forget goroutines
**Symptoms:** goroutines launched with no ownership, cancellation, or wait path.

**Why it hurts:** leaks, shutdown bugs, silent failures.

**Preferred refactor:** synchronous call, worker object, or owned group with explicit shutdown.

### 22. Blocked send or receive with no cancellation
**Symptoms:** goroutine can wait forever on channel ops.

**Why it hurts:** goroutine leaks and hanging shutdown.

**Preferred refactor:** select on `ctx.Done()` or redesign ownership/backpressure.

### 23. Unbounded concurrency
**Symptoms:** goroutine per item or request with no limit.

**Why it hurts:** memory blowups, scheduler pressure, overload propagation.

**Preferred refactor:** bound concurrency.

### 24. Context hidden in a struct
**Symptoms:** long-lived type stores `context.Context`.

**Why it hurts:** lifetime confusion and broken propagation discipline.

**Preferred refactor:** pass `ctx` per call.

### 25. Channel close ownership unclear
**Symptoms:** receivers close channels; multiple senders race to close.

**Why it hurts:** panics and protocol confusion.

**Preferred refactor:** owner/producer closes; document protocol.

### 26. Copying synchronized structs or exposing mutexes
**Symptoms:** mutex-containing values copied or embedded publicly.

**Why it hurts:** correctness hazards and API leakage.

**Preferred refactor:** pointer semantics and private synchronization.

## I/O and resource-management smells

### 27. HTTP response body not closed
**Symptoms:** `resp, err := client.Do(...)` without body cleanup.

**Why it hurts:** leaks resources and connection reuse opportunities.

**Preferred refactor:** close body at the narrowest safe scope.

### 28. `Rows`, `Stmt`, file, or cancel function not cleaned up
**Symptoms:** acquired resources leave cleanup implicit.

**Why it hurts:** leaks and hard-to-debug production issues.

**Preferred refactor:** explicit `defer` or structured lifetime management.

### 29. Transaction success path unclear
**Symptoms:** commit/rollback scattered or missing.

**Why it hurts:** inconsistent data and hard-to-review failure paths.

**Preferred refactor:** one explicit commit path plus rollback safety net.

### 30. SQL string formatting
**Symptoms:** `fmt.Sprintf` used to inject values into SQL.

**Why it hurts:** injection risk and correctness bugs.

**Preferred refactor:** parameterized queries.

### 31. No timeout or deadline on external I/O
**Symptoms:** HTTP, DB, RPC, or filesystem operations can block indefinitely.

**Why it hurts:** availability and shutdown problems.

**Preferred refactor:** contexts and explicit timeout policy.

### 32. Trust boundary on file paths is implicit
**Symptoms:** user-controlled path pieces are joined into filesystem operations without a clear boundary strategy.

**Why it hurts:** traversal risk and portability surprises.

**Preferred refactor:** make the boundary explicit and use traversal-resistant techniques appropriate to the environment.

### 33. Permissive decoding at a strict boundary
**Symptoms:** unknown JSON fields or loosely typed payloads accepted deep into the system.

**Why it hurts:** silent contract drift and security risk.

**Preferred refactor:** strict decoding and early typing where appropriate.

## Testing smells

### 34. Mock-first design
**Symptoms:** architecture exists mainly to support mocks.

**Why it hurts:** too many abstractions and brittle tests.

**Preferred refactor:** test real behavior via public APIs or narrow consumer seams.

### 35. Assertion DSL overuse
**Symptoms:** tests become a pseudo-language of assertions.

**Why it hurts:** hard-to-read failures and hidden semantics.

**Preferred refactor:** plain Go checks with clear messages.

### 36. Error strings or JSON blobs compared literally
**Symptoms:** tests assert wording or formatting instead of semantics.

**Why it hurts:** brittle tests with low diagnostic value.

**Preferred refactor:** semantic comparison and diffs.

### 37. No race coverage for concurrent code
**Symptoms:** concurrent code merges without `-race`.

**Why it hurts:** real races survive ordinary unit tests.

**Preferred refactor:** add race verification and targeted coverage.

### 38. Sleep-based concurrency tests
**Symptoms:** tests rely on `time.Sleep` to "let work finish".

**Why it hurts:** flakiness and slow suites.

**Preferred refactor:** deterministic signaling or version-appropriate deterministic concurrency test facilities.

## Performance and observability smells

### 39. Optimize-before-measure
**Symptoms:** speculative micro-optimizations with no benchmark or profile.

**Why it hurts:** complexity without evidence.

**Preferred refactor:** benchmark/profile first.

### 40. Allocation churn in hot path
**Symptoms:** repeated conversions, avoidable allocations, missing preallocation.

**Why it hurts:** latency and throughput regressions under load.

**Preferred refactor:** profile-backed local improvements.

### 41. No useful telemetry around concurrency or retries
**Symptoms:** logs only, no queue depth, retry, or latency insight.

**Why it hurts:** operational blind spots.

**Preferred refactor:** structured logs, metrics, and trace propagation at boundaries.

## Security smells

### 42. `math/rand` for secrets
**Symptoms:** tokens, passwords, keys, nonces, or session identifiers built from `math/rand`.

**Why it hurts:** predictable values.

**Preferred refactor:** cryptographically secure randomness.

### 43. Sensitive values leak into logs or errors
**Symptoms:** secrets interpolated into errors or log lines.

**Why it hurts:** credential exposure.

**Preferred refactor:** contextualize errors without exposing secret material.

## Readability and documentation smells

### 44. Naked returns in non-trivial functions
**Symptoms:** named result parameters plus bare `return` in longer functions.

**Why it hurts:** control flow becomes harder to review and error paths become ambiguous.

**Preferred refactor:** return explicit values unless the function is tiny and the named results add real clarity.

### 45. Named result parameters with no semantic value
**Symptoms:** named results exist only out of habit, not because they clarify the contract.

**Why it hurts:** extra mutable locals and harder-to-read control flow.

**Preferred refactor:** use unnamed results unless names clearly document meaning.

### 46. Dot imports outside tightly justified cases
**Symptoms:** package members appear in scope with no package prefix.

**Why it hurts:** obscures origin, increases collisions, and hurts readability.

**Preferred refactor:** ordinary imports with package names.

### 47. Receiver names that fight readability
**Symptoms:** `this`, `self`, inconsistent abbreviations, or long noisy receiver names.

**Why it hurts:** visual noise across many methods.

**Preferred refactor:** short, consistent receiver names tied to the type.

### 48. Missing or low-value doc comments on exported API
**Symptoms:** exported identifiers lack comments, or comments only restate the name mechanically.

**Why it hurts:** public contracts become guesswork.

**Preferred refactor:** document behavior, invariants, cleanup ownership, concurrency, and edge cases where they matter.

### 49. Getter naming imported from other languages
**Symptoms:** `GetName`, `GetConfig`, `GetStatus` without a strong reason.

**Why it hurts:** noisy API and un-Go-like naming.

**Preferred refactor:** noun-like accessors such as `Name`, `Config`, `Status`.

### 50. Comments explaining confusing code instead of simplifying it
**Symptoms:** long comments justify tangled control flow or hidden side effects.

**Why it hurts:** the comment becomes a maintenance burden and the code stays brittle.

**Preferred refactor:** simplify first; keep comments for contracts, invariants, and non-obvious behavior.
