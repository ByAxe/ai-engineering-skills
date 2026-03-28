# Performance, Native Readiness, and Resource Usage

Use this guide after correctness and architecture are already under control.

## Performance Starts with Execution Model Choice

The biggest architectural performance choices usually come from:

- blocking vs non-blocking
- worker thread vs virtual thread vs reactive
- ORM vs reactive persistence
- remote call timeout and retry policy
- batching and query shape

Do not start by micro-optimizing Kotlin syntax.

## Measure Before Tuning

Prefer:

- production-like profiling
- latency and throughput measurements on real hot paths
- allocation or query-count visibility
- JFR or tracing for bottleneck analysis

Avoid speculative cleanup that makes code harder to read without proven value.

## Native-Readiness Mindset

If the service ships native, review:

- reflection-heavy libraries
- serialization choice
- provider selection
- dynamic proxies
- resource loading assumptions
- build-time vs runtime config differences

Kotlin-specific watchpoints:

- final classes vs framework proxies
- Jackson plus Kotlin data classes in native mode
- serializer choices
- accidental reliance on reflection-heavy behavior

## Virtual Threads vs Reactive vs Worker Threads

Use virtual threads for:

- simple I/O-bound synchronous code
- easier migration from blocking flows

Use reactive for:

- highly concurrent streaming or async pipelines
- integrations already exposing reactive types

Use worker-thread blocking for:

- simpler services with modest concurrency

## Database Performance

Common cleanup targets:

- N+1 queries
- chatty repository methods
- full-table scans disguised as convenience helpers
- entity graphs too broad for the HTTP contract

## Remote Call Performance

Review:

- timeouts
- retries
- connection reuse
- request batching
- caching opportunities

## Avoid Hot-Path Logging and Allocation Noise

Smells:

- building huge log strings in tight loops
- repeated mapping churn on very hot code paths
- converting between several model layers with no boundary value

## Resource Usage Review Questions

- Is the execution model correct for the load shape?
- Are native constraints respected where relevant?
- Are DB and remote calls measured and intentional?
- Is complexity increasing or decreasing under optimization?
