# Async, Reactive, Coroutines, and Virtual Threads

This is one of the most important cleanup guides in Quarkus code. Many maintainability and production bugs come from execution-model confusion.

## First Rule: Choose Intentionally

For each entry point, decide between:

- blocking on worker thread
- blocking on virtual thread
- coroutine `suspend`
- reactive `Uni` or `Multi`

Do not mix them by accident.

## Decision Table

### Blocking on Worker Thread

Good when:

- the code is simple and mostly blocking
- concurrency needs are moderate
- the team wants plain imperative code
- JDBC or other blocking APIs dominate

Avoid if:

- many concurrent I/O waits are expected and worker saturation becomes a concern

### Blocking on Virtual Thread

Good when:

- the path is mostly I/O-bound
- you want simple synchronous code
- dependencies are virtual-thread friendly
- you understand pinning risks

Use:

```kotlin
@GET
@Path("/catalog/{id}")
@RunOnVirtualThread
fun getCatalogItem(id: String): CatalogItemResponse =
    service.get(id)
```

Watch for:

- `synchronized` on Java 21–23
- native-code pinning scenarios
- compute-heavy work monopolizing carriers

Virtual threads are for I/O-bound work, not CPU-heavy parallel computation.

### Coroutines with `suspend`

Good when:

- the Quarkus extensions in use support `suspend`
- the team is comfortable with structured concurrency
- you want imperative-looking async code without callback chains

Example:

```kotlin
@Path("/products")
class ProductResource(
    private val service: ProductService,
) {
    @GET
    @Path("/{id}")
    suspend fun get(id: String): ProductResponse =
        service.get(id)
}
```

Rules:

- do not use `GlobalScope`
- do not use `runBlocking` in request handling
- keep cancellation propagation intact
- prefer structured concurrency

If you catch `CancellationException`, rethrow it.

### Reactive `Uni` or `Multi`

Good when:

- the path is genuinely reactive end-to-end
- you need stream or back-pressure semantics
- messaging or reactive clients already drive the design

Example:

```kotlin
@GET
fun list(): Uni<List<ProductResponse>> =
    service.list()
```

Avoid reactive code only for aesthetics. It is more complex and should buy concurrency or streaming value.

## Event Loop Safety

The event loop must not be blocked.

Smells:

- JDBC call inside a non-blocking endpoint
- `Thread.sleep`
- blocking REST client call on event loop
- file I/O in a non-blocking handler

Tools:

- `@Blocking`
- `@NonBlocking`
- `@RunOnVirtualThread`

Use them to make the execution contract explicit.

## Coroutines + Quarkus

Quarkus supports `suspend` across several extensions, including REST, REST client, messaging, scheduler, fault tolerance, Vert.x, and WebSockets Next.

Use this only where the whole path remains understandable.

### Cancellation

In coroutine code:

- do not swallow `CancellationException`
- do not translate every exception to a generic business error
- use structured scopes, not orphaned jobs

Bad:

```kotlin
suspend fun syncCatalog() {
    runCatching {
        client.fetchAll()
    }.onFailure {
        log.error("sync failed", it)
    }
}
```

Better:

```kotlin
suspend fun syncCatalog() {
    try {
        client.fetchAll()
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        log.error("sync failed", e)
        throw e
    }
}
```

## Context Propagation

With Mutiny plus the Quarkus context propagation extension, CDI, REST, and transaction context can propagate automatically in the common cases.

With `CompletionStage`, manual propagation support is often needed through `ManagedExecutor` or `ThreadContext`.

Cleanup smell:

- security, transaction, or MDC context mysteriously disappears in async code

## `runBlocking`

Valid mostly in:

- tests
- bridges at application startup or CLI edges where no better boundary exists

Invalid in:

- HTTP request handling
- messaging consumers
- normal application services

## Mixed-Model Smells

High-risk examples:

- resource returns `Uni`, service uses blocking ORM, helper wraps in `runBlocking`
- coroutine endpoint calls a blocking client on the event loop
- virtual-thread endpoint does heavy CPU work
- service uses both `Deferred` and `Uni` with ad-hoc conversions

Prefer one idiom per slice.

## Review Questions

- Is the model obvious for each entry point?
- Could this block the event loop?
- Is `runBlocking` used in request code?
- Are virtual threads used only for I/O-bound paths?
- Are coroutine cancellations preserved?
- Is context propagation intentional?
