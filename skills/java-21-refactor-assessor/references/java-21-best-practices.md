# Java 21 Best Practices

Detailed best practices for idiomatic Java 21 development. Referenced from the main skill during Step 5 (Execute Refactors).

## Data modeling and immutability

- Prefer records for immutable "data carrier" types:
  - DTOs, events, messages, value objects.
  - Avoid records for persistence entities that require proxies/mutation (common in ORMs).
- Prefer sealed interfaces/classes for closed hierarchies (algebraic data types):
  - Model "one of these variants" with sealed types instead of stringly-typed enums plus payload maps.
- Prefer java.time types for time, duration, and instants:
  - Avoid java.util.Date and Calendar.
- Prefer explicit types over Map-based "schemas":
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

## Pattern matching and readability

- Use pattern matching for switch to replace type-dispatch if/else chains (finalized in Java 21, JEP 441).
- Use record patterns to simplify deconstruction of nested records (finalized in Java 21, JEP 440).
- Prefer switch expressions (->) when producing values; keep side effects explicit.

## Collections and APIs

- Prefer interfaces in APIs (List, Set, Map) and immutable factory methods where appropriate:
  - List.of, Set.of, Map.of, List.copyOf.
- Use sequenced collections APIs when order matters and you need first/last or reverse traversal (JEP 431):
  - Prefer explicit first/last intent rather than manual index arithmetic.

## Null and Optional

- Avoid returning null from public APIs.
- Use Optional primarily for return values (not for fields) and avoid Optional parameters in most cases.
- Enforce nullness at boundaries:
  - Validate inputs early, fail fast with clear exceptions or typed error results.

## Exceptions and error modeling

- Treat exceptions as exceptional, not control flow.
- Prefer domain-specific exceptions or typed results for expected failure modes.
- Never swallow exceptions. Either:
  - Handle fully with compensation, or
  - Propagate with context.
- Preserve causes when wrapping: new XException(message, cause).

## Concurrency and Java 21 features

### Virtual threads (JEP 444 — finalized)

- Use virtual threads for high-throughput, I/O-bound concurrency (request-per-task style).
- Avoid virtual threads for compute-bound parallelism; use platform threads or structured parallel algorithms.
- Avoid pinning:
  - Avoid synchronized blocks/methods in code that runs on virtual threads.
  - Prefer java.util.concurrent locks (e.g., ReentrantLock) or other non-blocking coordination where appropriate.

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

### Structured concurrency (JEP 453 — preview in Java 21)

- Prefer structured concurrency when you need "fork subtasks, join once, handle failures centrally".
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

**Note:** The StructuredTaskScope API is a preview feature and may change in future Java releases. The `scope.join().throwIfFailed()` chaining pattern shown above reflects the Java 21 preview API (JEP 453). Verify against your specific JDK version.

### Scoped values (JEP 446 — preview in Java 21)

- Scoped values provide a mechanism for sharing immutable data within and across threads in a structured way.
- Prefer scoped values over ThreadLocal for virtual thread workloads where values are set once and read by child tasks.
- Preview feature: requires --enable-preview.

## I/O, resources, and lifecycle

- Use try-with-resources for anything that must close (streams, channels, DB handles, HTTP responses).
- Prefer java.net.http.HttpClient (or a well-supported library) for HTTP, with explicit timeouts.
- Prefer NIO (Path, Files) over legacy File where it improves correctness and testability.

## Logging and observability

- Use structured logging (key-value fields) where possible.
- Avoid System.out/System.err for production code.
- Ensure logs include:
  - Correlation identifiers (request id, job id)
  - Failure causes (exception stack traces where appropriate)
  - Clear event boundaries (start, success, failure)

## Testing strategy

- Add tests before large refactors:
  - Characterize existing behavior (golden tests) for tricky ported logic.
- Prefer:
  - JUnit 5 for unit tests
  - Parameterized tests for edge cases
  - Contract tests at boundaries (HTTP/DB/message)
- Keep tests deterministic; avoid timing-based assertions unless necessary.

## Build and quality gates

- Set compiler level explicitly to Java 21.
- Enable warnings and treat important ones as errors in CI.
- Use formatters and static analysis (examples):
  - Code style: Spotless or Checkstyle
  - Bug finding: SpotBugs, Error Prone
  - Architecture tests: ArchUnit
- Keep dependency versions consistent and avoid "version drift" across modules.
