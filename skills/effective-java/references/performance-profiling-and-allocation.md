# Performance, Profiling, and Allocation

Optimize measured bottlenecks under a representative workload. Preserve correctness, observability, and operability.

## Define the target

Name the metric and budget:

- p50/p95/p99 latency
- throughput
- CPU
- allocation rate/heap/GC pause
- startup time/RSS
- database query count/time
- downstream calls
- native image size/build time

A faster micro-method may not improve the service bottleneck.

## Measurement hierarchy

- production telemetry/traces/metrics for real symptoms
- Java Flight Recorder for CPU, allocation, locks, I/O, GC, virtual-thread events
- profiler for hotspots/allocation
- database query plan and statement metrics
- JMH for isolated JVM microbenchmarks
- load test for end-to-end behavior

Do not write a timing loop in a unit test and call it a benchmark. JVM warmup, dead-code elimination, constant folding, GC, and environment noise make naive measurements misleading.

## Common real bottlenecks

- N+1 queries or missing indexes
- remote call fan-out/retries/timeouts
- serialization of large graphs
- excessive allocation/copying
- lock contention
- unbounded queues/backlogs
- poor cache behavior
- blocking on event loop
- connection pool saturation

Prefer fixing I/O/query shape before low-level syntax changes.

## Allocation and collections

Avoid speculative object reuse that harms correctness or virtual-thread memory. Profile before replacing streams, records, optionals, or immutable copies. Escape analysis and JIT can remove allocations; conversely, a concise pipeline can allocate heavily in a hot path.

Use primitive streams/arrays only when profiling shows boxing matters and clarity remains acceptable.

## Caching

Every cache needs:

- key correctness and tenant/security scope
- maximum size/eviction
- TTL/staleness policy
- invalidation
- loading/concurrency behavior
- failure behavior
- metrics
- memory estimate

Do not cache mutable entities/session-bound objects or secrets without explicit design. Beware high-cardinality user input keys.

## Pools and limits

Size pools around the scarce resource and workload, not an arbitrary CPU multiplier. More threads cannot overcome a small database pool. Virtual threads should not be pooled; limit downstream concurrency separately.

## Logging and observability cost

Guard expensive log argument construction when the logging API does not defer it. Avoid high-cardinality metric labels and huge trace attributes. Do not remove necessary observability for a small benchmark gain without an operational alternative.

## Startup and native

Quarkus/native optimizes startup and footprint but introduces build-time initialization, closed-world, reflection/resource, and build-cost constraints. Measure the deployment objective; native is not automatically faster for every steady-state workload.

## JMH discipline

When a microbenchmark is warranted:

- use JMH, appropriate modes, warmup, forks, and profilers
- consume results with `Blackhole` when needed
- parameterize representative sizes/distributions
- isolate setup from measured operation
- compare confidence/error, not one number
- inspect generated assembly only for genuinely low-level work

## Optimization report

Record:

- baseline environment/workload
- before distribution, not only average
- bottleneck evidence
- change
- after distribution
- correctness gates
- trade-offs and rollback

Do not claim “O(1)” or reduced allocation without considering the whole operation and data structure semantics.
