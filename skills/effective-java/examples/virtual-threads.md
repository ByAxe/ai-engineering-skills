# Virtual Threads with Explicit Resource Bounds

Virtual threads improve the scalability of thread-per-task blocking I/O. They do not increase CPU capacity or downstream connection limits.

## Appropriate shape

```java
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;

final class CustomerImporter {
    private final CustomerClient client;
    private final Semaphore remoteConcurrency = new Semaphore(32);

    CustomerImporter(CustomerClient client) {
        this.client = client;
    }

    void importAll(java.util.List<CustomerId> ids) throws Exception {
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            var futures = ids.stream()
                .map(id -> executor.submit(() -> fetchBounded(id)))
                .toList();

            for (var future : futures) {
                persist(future.get());
            }
        }
    }

    private Customer fetchBounded(CustomerId id) throws Exception {
        remoteConcurrency.acquire();
        try {
            return client.fetch(id);
        } finally {
            remoteConcurrency.release();
        }
    }
}
```

The semaphore represents a downstream capacity decision. In production, cancellation, timeout, partial failure, persistence ordering, and metrics also need explicit handling.

## Reject

```java
Executors.newFixedThreadPool(100, Thread.ofVirtual().factory());
```

Virtual threads are disposable and should not be pooled merely to copy a platform-thread design.

Also reject moving a CPU-heavy transformation to thousands of virtual threads. Measure and use bounded CPU parallelism if it is genuinely beneficial.

## JDK-specific pinning

On JDK 21–23, blocking while holding a monitor can pin a carrier. JDK 24’s JEP 491 changes `synchronized`-related pinning, while native-code cases remain. Diagnose the actual runtime before replacing synchronization repository-wide.

## Proof

- workload is blocking I/O
- client/database pools remain bounded
- timeouts and cancellation reach the operation
- thread-local allocation/context is understood
- load test reflects downstream limits
- JFR/runtime diagnostics support the claim
