# Concurrency, Context, and Lifecycle Smells

## Contents
- Review model for concurrent Go code
- Context smells
- Goroutine lifecycle smells
- Channel ownership smells
- Synchronization smells
- Shutdown and cancellation patterns
- Review checklist

## Review model for concurrent Go code

Read concurrent Go code by asking three questions:
1. **Who owns this goroutine or resource?**
2. **How does it stop?**
3. **What prevents indefinite blocking under partial failure?**

If the code does not answer those questions clearly, there is already a smell.

## Context smells

### Context stored in a struct
Usually a smell.
`context.Context` should be passed explicitly to each call that needs it.

### Context not first parameter
Use `ctx context.Context` as the first parameter for functions and methods that use it.

### Using context values as optional parameters
Smell when context becomes a generic bag of configuration.
Use context values only for request-scoped data that must cross API/process boundaries.

### Cancellation ignored in loops or blocking operations
Smell when workers or streams block forever on send/receive or I/O with no cancellation path.
Add `select` on `ctx.Done()` or use context-aware APIs.

## Goroutine lifecycle smells

### Fire-and-forget goroutine
Smell when a goroutine is launched with no owner, no shutdown path, and no error reporting strategy.

Refactor toward:
- synchronous call if background work is unnecessary
- owned worker object with `Run`/`Stop`
- `errgroup` or explicit wait/close protocol

### Leaking goroutine on channel send or receive
Common signs:
- goroutine blocks on send after consumer exits
- goroutine waits forever on receive after producer is gone

Refactor toward:
- buffered channel only when it models real capacity
- explicit cancellation
- ownership-documented close direction
- bounded worker pools

### Unbounded fan-out
Smell when loops launch goroutines per item with no concurrency bound.
Use a semaphore, worker pool, or `errgroup` limit pattern.

## Channel ownership smells

### Receiver closes the channel it did not create
Usually a smell.
The sending/owning side should close the channel.

### Channel used as both queue and lifetime signal with no documentation
Separate data channels from shutdown signals unless the protocol is very clear.

### Channel sizes chosen by guesswork
A large buffer can hide backpressure bugs.
Capacity should model a real queueing need.

## Synchronization smells

### Exposed mutex in public API
Smell when embedding or exporting a mutex leaks implementation detail and lets callers couple to internals.

### Copying structs that contain mutexes
Dangerous. Use pointer receivers and avoid copying after first use.

### Cargo-cult `RWMutex`
`RWMutex` is not automatically better than `Mutex`.
Use it only with measured read-heavy contention.

### Mixing atomic and non-atomic access
A correctness smell unless carefully designed. All accesses to a synchronized value should follow the same synchronization model.

## Shutdown and cancellation patterns

Preferred patterns:
- owner creates worker and owns its shutdown
- `ctx` communicates cancellation
- goroutines signal completion explicitly
- `defer` handles cleanup at the narrowest safe scope
- long-lived loops document exit conditions

For services, review shutdown order explicitly:
1. stop accepting new work
2. cancel outstanding work
3. wait for workers to finish
4. release resources

## Review checklist

Use this list for concurrent code:
- Does every goroutine have a named owner?
- Is there a clear stop condition?
- Can sends or receives block forever?
- Is channel close responsibility obvious?
- Does cancellation flow from request or process shutdown?
- Are cleanup and `Wait` semantics explicit?
- Has the code been exercised with `go test -race`?
