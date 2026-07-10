# Concurrency, Virtual Threads, and Async Boundaries

Choose an execution model deliberately. Concurrency is a behavior and resource-management decision, not a syntax upgrade.

## Begin with the workload

Classify each path:

- CPU-bound
- blocking I/O-bound
- non-blocking/reactive I/O
- mixed
- latency-sensitive versus throughput-sensitive
- bounded versus bursty/untrusted concurrency

Name the concurrency limit and scarce resource: CPU cores, database connections, downstream quota, memory, file descriptors, or event-loop time.

## Java Memory Model essentials

- `volatile` provides visibility/order for a variable, not atomicity of compound actions
- `count++` is not atomic
- safe publication matters for mutable objects
- final fields help initialization safety but do not freeze referenced objects
- concurrent collections make their own operations safe, not arbitrary multi-step invariants
- double-checked locking requires a volatile reference

Prefer immutable messages and confined mutable state. Use locks/atomics only around a clearly stated invariant.

## Locks

Keep critical sections small and free of blocking network/database calls. Document lock ordering when multiple locks exist. Choose `ReentrantLock` only for capabilities such as timed/interruptible acquisition, conditions, or version-specific virtual-thread pinning needs—not as a reflexive replacement for every `synchronized`.

## Executor ownership

Every executor requires:

- owner and lifetime
- thread/task naming or observability
- queue/bound policy
- rejection behavior
- shutdown and drain behavior
- uncaught failure handling
- context propagation policy

In an application server, prefer framework-managed execution unless a dedicated resource is justified. Avoid creating executors per request.

## `CompletableFuture`

Review:

- implicit common-pool use in `supplyAsync`/`runAsync`
- sync versus async continuation methods and executing thread
- exception wrapping (`CompletionException`/`ExecutionException`)
- cancellation propagation
- timeouts and fallback semantics
- blocking `join/get` on event-loop or constrained threads
- shared mutable capture

A chain is not non-blocking merely because it returns a future.

## Virtual threads (Java 21)

Virtual threads improve scalability for high-concurrency workloads that spend much of their time blocked on I/O. They do not make CPU-bound code faster or reduce the cost of downstream resources.

Rules:

- use thread-per-task; do not pool virtual threads
- use a semaphore/rate limiter/connection pool to bound scarce resources
- avoid thread-local caches/pools that allocate expensive state per virtual thread
- preserve interruption and cancellation
- ensure libraries/blocking calls cooperate with the JDK implementation
- measure memory and downstream saturation, not only thread count

### Pinning is JDK-version-sensitive

On JDK 21–23, blocking while holding a monitor (`synchronized`) or in certain native code can pin a carrier and reduce scalability. JFR pinning events and `-Djdk.tracePinnedThreads` help diagnose this on those versions. JEP 491 changes synchronized-related pinning in JDK 24; native interactions can still matter. Do not apply a JDK 21 pinning workaround blindly to a later runtime.

Do not replace short in-memory `synchronized` sections merely because virtual threads exist. Focus on frequent, long blocking while pinned.

## Structured concurrency and scoped values

Both are preview APIs in Java 21 and evolved in later releases. Do not introduce them unless preview usage is already accepted and the exact JDK API is verified. Their conceptual benefits—task lifetime nesting, cancellation, and bounded context—can still inform design.

## Thread locals and context

Thread locals can leak state in pooled platform threads and consume excessive memory with many virtual threads. Clear owned thread locals reliably. Prefer explicit context or framework-supported propagation. Do not assume security/transaction/trace context crosses arbitrary executors.

## Parallel streams

They use shared execution infrastructure by default and offer limited lifecycle/context control. Avoid in request handling or blocking work without evidence. Associativity, splittability, ordering, and workload size determine value.

## Reactive code

Reactive types do not make blocking calls non-blocking. A reactive path requires:

- non-blocking dependencies or explicit offload
- backpressure/overflow policy
- cancellation propagation
- timeout and retry semantics
- context propagation
- clear transaction/session lifetime

Avoid converting a method to `Uni`, `Multi`, `Publisher`, or future solely to change its signature while retaining blocking internals.

## Timeouts, retries, and idempotency

A timeout stops waiting; it does not prove work stopped. Cancellation may be cooperative. A retry can duplicate side effects. Define idempotency keys, deduplication, transaction boundaries, and retryable failure classes before retrying writes.

Use jittered backoff and global budgets where retries are valid. Avoid retry amplification across stacked clients/services.

## Concurrency tests

- avoid `Thread.sleep` as synchronization
- use latches/barriers/futures and bounded deadlines
- repeat/race tests where useful, but do not mistake probabilistic absence for proof
- test cancellation, interruption, timeout, and saturation
- use JFR/thread dumps/profilers for runtime evidence

## Quarkus

Quarkus event-loop, worker, virtual-thread, Mutiny, transaction, and messaging rules are framework-specific. Read `quarkus-rest-clients-and-execution-model.md` or `quarkus-messaging-scheduling-and-fault-tolerance.md` before changing execution annotations.

## Primary sources

- OpenJDK JEP 444 — Virtual Threads
- OpenJDK JEP 491 — Synchronize Virtual Threads without Pinning
- Java 21 `java.util.concurrent` API
- Quarkus virtual threads and REST execution model guides
