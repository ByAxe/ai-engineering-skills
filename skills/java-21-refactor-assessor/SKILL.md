---
name: java-21-refactor-assessor
description: Assesses and refactors Java 21 codebases into idiomatic, maintainable Java. Use when the user asks to review or modernize a Java 21 repository, refactor a Python-to-Java port, remove Pythonic anti-patterns, or improve architecture, concurrency, testing, performance, logging, and error handling. Do not use for pure Python-only repositories or projects not written in Java.
---

# Java 21 Refactor Assessor

Turn a Java 21 codebase that was ported from Python into clean, idiomatic Java with strong typing, clear boundaries, safe concurrency, and verifiable behavior.

## Operating principles

- Preserve behavior first. Favor refactors that keep external behavior identical, backed by tests.
- Prefer clarity over cleverness. Avoid overusing streams, reflection, metaprogramming patterns, or “framework magic” when a simple, explicit approach is clearer.
- Make illegal states unrepresentable. Use types, immutability, and sealed hierarchies to prevent bugs.
- Keep changes incremental. Refactor in small batches; compile and run tests after each batch.
- Optimize last. Make performance changes only after correctness and clarity are established, and back them with measurements.

## Workflow

### 1) Establish a baseline

- Identify the build tool and entry points:
  - Maven: pom.xml
  - Gradle: build.gradle or build.gradle.kts
- Run a clean build and the full test suite.
- Capture current behavior:
  - Record API contracts, CLI output, and key workflows.
  - Note runtime flags (especially for any preview features).

### 2) Inventory architecture and dependencies

- Map modules and packages:
  - Identify “core domain” code vs frameworks/adapters (web, DB, messaging).
  - Detect cycles between packages/modules.
- Identify external dependencies and versions:
  - Highlight Python-era libraries or patterns that no longer fit (dynamic maps, “duck-typing” wrappers, runtime type switching).

### 3) Detect Python-to-Java port smells

Look for these high-signal patterns:

- Dynamic data everywhere:
  - Map<String, Object>, Map<String, Any>, raw Object fields, JSON-as-Map without schemas.
  - “payload” blobs passed through many layers.
- Overloaded “utility” modules/classes:
  - Large static helper classes replacing cohesive services.
  - God classes that centralize unrelated responsibilities.
- Pythonic control flow:
  - Deep if/elif chains for type dispatch instead of polymorphism or sealed + switch.
  - Sentinel values and None-like patterns instead of explicit types or Optional.
- Weak error modeling:
  - Catch-all Exception, silent failures, logging without propagation, “return null” on failure.
- Concurrency translated literally:
  - Shared mutable state, ad-hoc thread creation, executor misuse, or “async-style” code without need.

### 4) Propose a refactor plan

- Prioritize by risk and leverage:
  1. Correctness and data integrity
  2. API and domain modeling
  3. Boundaries and layering
  4. Concurrency and scalability
  5. Performance and allocation hot spots
- Define phases with acceptance criteria:
  - Build still passes
  - Tests still pass (or are improved)
  - Public interfaces unchanged unless explicitly approved

### 5) Execute refactors (idiomatic Java 21)

Apply the guidance below. Prefer changes that reduce complexity and increase static guarantees.

### 6) Validate and harden

- Run formatters and static analysis.
- Add or strengthen tests around previously implicit behavior.
- Re-run the suite and key workflows.
- Provide a concise change log: what changed, why, and how to validate.

## Java 21 best practices to enforce

### Data modeling and immutability

- Prefer records for immutable “data carrier” types:
  - DTOs, events, messages, value objects.
  - Avoid records for persistence entities that require proxies/mutation (common in ORMs).
- Prefer sealed interfaces/classes for closed hierarchies (algebraic data types):
  - Model “one of these variants” with sealed types instead of stringly-typed enums plus payload maps.
- Prefer java.time types for time, duration, and instants:
  - Avoid java.util.Date and Calendar.
- Prefer explicit types over Map-based “schemas”:
  - Replace Map payloads with records/classes and validated parsing.

Example: sealed hierarchy + records + exhaustive switch

```java
sealed interface Result permits Result.Ok, Result.NotFound, Result.Error {
  record Ok(String value) implements Result {}
  record NotFound(String key) implements Result {}
  record Error(String message, Throwable cause) implements Result {}
}

static String render(Result r) {
  return switch (r) {
    case Result.Ok(var value) -> value;
    case Result.NotFound(var key) -> "missing: " + key;
    case Result.Error(var msg, var cause) -> msg + " (" + cause.getClass().getSimpleName() + ")";
  };
}
```

### Pattern matching and readability

- Use pattern matching for switch to replace type-dispatch if/else chains.
- Use record patterns to simplify deconstruction of nested records.
- Prefer switch expressions (->) when producing values; keep side effects explicit.

### Collections and APIs

- Prefer interfaces in APIs (List, Set, Map) and immutable factory methods where appropriate:
  - List.of, Set.of, Map.of, List.copyOf.
- Use sequenced collections APIs when order matters and you need first/last or reverse traversal:
  - Prefer explicit first/last intent rather than manual index arithmetic.

### Null and Optional

- Avoid returning null from public APIs.
- Use Optional primarily for return values (not for fields) and avoid Optional parameters in most cases.
- Enforce nullness at boundaries:
  - Validate inputs early, fail fast with clear exceptions or typed error results.

### Exceptions and error modeling

- Treat exceptions as exceptional, not control flow.
- Prefer domain-specific exceptions or typed results for expected failure modes.
- Never swallow exceptions. Either:
  - Handle fully with compensation, or
  - Propagate with context.
- Preserve causes when wrapping: new XException(message, cause).

### Concurrency and Java 21 features

#### Virtual threads

- Use virtual threads for high-throughput, I/O-bound concurrency (request-per-task style).
- Avoid virtual threads for compute-bound parallelism; use platform threads or structured parallel algorithms.
- Avoid pinning:
  - Avoid synchronized blocks/methods in code that runs on virtual threads.
  - Prefer java.util.concurrent locks or other non-blocking coordination where appropriate.

Example: virtual thread per task executor

```java
try (var executor = java.util.concurrent.Executors.newVirtualThreadPerTaskExecutor()) {
  var futures = java.util.stream.IntStream.range(0, 1000)
      .mapToObj(i -> executor.submit(() -> callRemoteService(i)))
      .toList();

  for (var f : futures) {
    process(f.get());
  }
}
```

#### Structured concurrency and scoped values (preview in Java 21)

- Prefer structured concurrency when you need “fork subtasks, join once, handle failures centrally”.
- Use try-with-resources to bound lifetimes, ensure cancellation, and keep observability.
- Use preview features only when the project explicitly opts in:
  - Compile and run with --enable-preview, and document this choice in the build.

Example: structured concurrency with fail-fast policy

```java
try (var scope = new java.util.concurrent.StructuredTaskScope.ShutdownOnFailure()) {
  var user = scope.fork(this::fetchUser);
  var offers = scope.fork(this::fetchOffers);

  scope.join().throwIfFailed();

  return combine(user.get(), offers.get());
}
```

### I/O, resources, and lifecycle

- Use try-with-resources for anything that must close (streams, channels, DB handles, HTTP responses).
- Prefer java.net.http.HttpClient (or a well-supported library) for HTTP, with explicit timeouts.
- Prefer NIO (Path, Files) over legacy File where it improves correctness and testability.

### Logging and observability

- Use structured logging (key-value fields) where possible.
- Avoid System.out/System.err for production code.
- Ensure logs include:
  - Correlation identifiers (request id, job id)
  - Failure causes (exception stack traces where appropriate)
  - Clear event boundaries (start, success, failure)

### Testing strategy

- Add tests before large refactors:
  - Characterize existing behavior (golden tests) for tricky ported logic.
- Prefer:
  - JUnit 5 for unit tests
  - Parameterized tests for edge cases
  - Contract tests at boundaries (HTTP/DB/message)
- Keep tests deterministic; avoid timing-based assertions unless necessary.

### Build and quality gates

- Set compiler level explicitly to Java 21.
- Enable warnings and treat important ones as errors in CI.
- Use formatters and static analysis (examples):
  - Code style: Spotless or Checkstyle
  - Bug finding: SpotBugs, Error Prone
  - Architecture tests: ArchUnit
- Keep dependency versions consistent and avoid “version drift” across modules.

## Refactoring playbook by symptom

### Symptom: “Everything is a Map”

- Introduce typed records/classes for payloads.
- Centralize parsing/validation at the boundary (JSON in, typed object out).
- Replace Map lookups with field access.
- Add validation and tests for parsing.

### Symptom: “Huge if/else chains for types or states”

- Model states with sealed types or enums + dedicated data.
- Replace chains with pattern switch and exhaustive handling.
- Enforce no default branch unless explicitly needed.

### Symptom: “God classes and static helpers”

- Split by responsibility:
  - Extract cohesive services and inject dependencies.
  - Move pure functions to small utility classes only when genuinely cross-cutting.
- Reduce static state; prefer instance composition.

### Symptom: “Concurrency feels unsafe or inconsistent”

- Identify shared mutable state and race risks.
- Prefer confinement:
  - Make state immutable, or
  - Confine mutation to a single thread/component.
- For I/O-heavy parallelism, prefer virtual threads + bounded lifetimes.
- For multi-step parallel workflows, prefer structured concurrency.

### Symptom: “Errors are swallowed or unclear”

- Replace catch-all with specific handling.
- Add context to errors and propagate causes.
- Introduce typed results for expected failures.

## Output format for an assessment

When asked to assess a codebase, produce:

1. Findings summary:
   - Top 5 risks and their impact
2. Refactor plan:
   - Phases, expected effort, and safety checks
3. Concrete changes:
   - Specific files/classes to touch and why
4. Verification steps:
   - Exact commands to build/test/run key workflows

When asked to refactor code, implement changes in small batches and include:

- What changed
- Why it is more idiomatic Java 21
- How to verify (build + tests)
