# Failure Modes of Coding Agents in Java

Java agents often produce code that looks conventional and compiles locally while violating repository-specific semantics. This taxonomy is designed for review and prevention, not for blaming a particular model.

## Confidence vocabulary

Use these labels in assessments:

- **Confirmed defect:** a failing test, compiler error, reproducible behavior, violated specification, or direct contradiction proves it.
- **High-confidence risk:** the code and execution model make the failure likely, but the triggering runtime condition was not reproduced.
- **Candidate:** a heuristic or smell worth inspection; do not recommend a change without context.
- **Preference:** a maintainability choice with legitimate alternatives; state the trade-off.

Never promote a scanner match directly to a confirmed defect.

## 1. Version and API confabulation

### Typical output

- imports or annotations from a different Java/Quarkus generation
- `javax.*` mixed with `jakarta.*`
- a Maven coordinate, Gradle DSL block, Quarkus property, or extension that does not exist in the project version
- finalized syntax used while the project only supports a preview, or preview syntax used without flags
- documentation from “latest” applied to an older BOM

### Why it survives review

The names are plausible, autocomplete-like, and often resemble a real API from another version.

### Countermeasure

1. Read the configured release/toolchain and Quarkus BOM.
2. Search the local dependency graph or source before importing.
3. Compile the smallest touched module immediately.
4. Never repair an invented API by adding a random dependency before verifying the intended capability.

## 2. Compile-success illusion

### Typical output

- only the edited class was mentally checked
- tests compile but annotation processing, generated code, integration tests, or native build do not
- a test is added but never discovered by the configured engine
- a module builds in isolation while the reactor or dependent module breaks

### Countermeasure

Run gates in widening circles. Confirm test discovery, not merely process exit. For multi-module changes, compile affected dependents or the relevant reactor slice.

## 3. Semantic drift hidden as cleanup

High-risk contracts agents routinely change accidentally:

- `equals`/`hashCode` behavior after class-to-record conversion
- list mutability after switching to `Stream.toList()` or `List.copyOf`
- encounter order after replacing `LinkedHashMap`/`List` with `HashMap`/`Set`
- `BigDecimal` scale-sensitive equality
- default charset, locale, or zone
- exception type, cause, message, or HTTP mapping
- transaction start/end, flush timing, and lazy-loading window
- JSON property names, omission rules, constructor visibility, and unknown-field handling
- blocking versus event-loop execution in Quarkus

### Countermeasure

Write a contract matrix before editing and add a regression check for every changed dimension that matters.

## 4. Cargo-cult modernization

### Typical output

- nested streams replacing a clear loop
- `Optional` in fields, DTOs, setters, and every method
- records used for entities or mutable aggregates
- sealed types introduced without a genuinely closed domain
- pattern switches with a broad `default` that defeats exhaustiveness
- virtual threads added to CPU-bound work
- reactive wrappers around blocking persistence

### Countermeasure

Require a concrete advantage: stronger invariant, smaller error surface, clearer exhaustive model, measured throughput need, or reduced boilerplate without contract loss. “Modern Java” is not itself a requirement.

## 5. Abstraction inflation

### Typical output

- one interface per implementation
- generic base repository/service/controller
- factory and builder for a two-field immutable object
- mapper layers that copy identical shapes
- “clean architecture” packages with pass-through use cases
- strategy pattern for a variation that never varies

### Why agents do it

Pattern names are easy to generate and make a patch look architecturally deliberate.

### Countermeasure

Ask: Which independent axis of change, test boundary, or external dependency does this abstraction isolate? If there is no answer, keep the concrete code. Extract after repetition or volatility is demonstrated, not before.

## 6. Scope explosion and repository damage

### Typical output

- formatter churn across untouched files
- build plugin or dependency upgrades during a feature fix
- generated files edited directly
- package moves mixed with behavior changes
- deleted “unused” code referenced by CDI, reflection, service loading, serialization, or configuration
- changed lockfiles without the corresponding tool command

### Countermeasure

Use `scripts/check_diff_scope.py`. Separate mechanical moves from semantic edits. Inspect reflective and generated references before deletion. Keep build upgrades in a dedicated change.

## 7. Test theater

### Typical output

- mocking the class under test
- asserting that mocks were called instead of checking outcome or state
- reproducing the implementation inside the expected value
- broad `assertDoesNotThrow` with no contract assertion
- integration behavior “tested” with all real boundaries mocked
- `Thread.sleep` used as synchronization
- a Quarkus test used for pure logic, making feedback slow
- happy-path-only tests that miss null, duplicate, order, time-zone, retry, rollback, or authorization behavior

### Countermeasure

Each test should prove a named contract. Include defect proof, corrected behavior, and protected unchanged behavior for fixes. Prefer plain unit tests for pure logic and framework tests only for framework integration.

## 8. Concurrency and lifecycle hallucination

### Typical output

- a new executor with no owner or shutdown path
- `CompletableFuture.supplyAsync` using the common pool in server code
- `parallelStream()` inside request handling
- virtual-thread pools instead of thread-per-task
- unbounded task submission
- ignored cancellation or interrupted status
- mutable state in application-scoped beans
- thread-local caches migrated unchanged to millions of virtual threads

### Countermeasure

Name the owner, lifetime, concurrency limit, queue policy, cancellation path, context propagation, and observability for every async resource. Prefer framework-managed execution where appropriate.

## 9. Persistence and transaction simplification

### Typical output

- transaction annotation moved to a private/self-created object where interception is ineffective
- entity returned from REST and serialized after the persistence context closes
- cascade or orphan removal added to “fix” a test without lifecycle analysis
- `EAGER` applied globally to hide `LazyInitializationException`
- retries around non-idempotent writes
- count-then-insert race instead of a database constraint
- migration altered after deployment rather than superseded

### Countermeasure

Trace one complete request or message path: transaction, queries, flush, locks, events, serialization, and failure mapping. Use database constraints for invariants and test at the real boundary.

## 10. Quarkus mental-model errors

### Typical output

- treating ArC exactly like Spring or CDI Full
- assuming an unindexed dependency bean is discoverable
- using `@Named` as a qualifier and creating ambiguity
- ignoring build-time-fixed configuration
- blocking an event loop or using reactive APIs over blocking ORM
- assuming JVM success proves native success
- broad reflection registration instead of precise registration
- relying on Dev Services behavior in production

### Countermeasure

Profile the Quarkus version and extensions first. Read the relevant Quarkus reference and validate the execution model, augmentation, transaction, and native implications explicitly.

## 11. Security boundary omission

### Typical output

- input validation without authorization
- path normalization without containment check
- URL allowlist checked before redirects or DNS resolution
- SQL parameters fixed but dynamic identifiers still concatenated
- error responses exposing internals
- secrets in logs or config committed to source
- retries duplicating payments or messages
- parser limits omitted for XML/JSON/archive inputs

### Countermeasure

Identify trust boundaries and assets. Verify authentication, authorization, validation/canonicalization, resource limits, and failure behavior separately. Use `references/security-input-boundaries-and-secrets.md`.

## 12. “Helpful” behavior invention

Agents may add fallback values, swallow errors, auto-create missing data, retry, sort, normalize, or coerce because it seems user-friendly. Each can be a breaking semantic change.

Require an explicit contract before adding resilience. A failure made invisible is not necessarily a failure handled.

## Patch review red flags

Pause and inspect when a patch:

- is much larger than the requirement
- adds several new abstractions or dependencies
- changes build files and production code together
- has no test for the changed contract
- replaces domain types with maps or strings
- changes concurrency, transaction, serialization, or public API shape without mentioning it
- claims performance improvement without a measurement
- claims “idiomatic Quarkus” without naming the project version and execution model

## Research context

Recent empirical work on LLM-generated Java reports more code-smell and security findings than human reference solutions, and studies of agent skills show that broad or version-mismatched guidance can add little value or reduce performance. Treat those results as motivation for deterministic checks, specialized context, and paired evals—not as proof that any individual patch is defective. See `source-index.md` for the primary papers.
