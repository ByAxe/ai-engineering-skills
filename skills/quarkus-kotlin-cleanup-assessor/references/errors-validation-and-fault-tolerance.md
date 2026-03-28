# Errors, Validation, and Fault Tolerance

Use this guide to make failures explicit, readable, and operationally sane.

## Validate Early

Boundary validation should happen close to the transport layer.

Use:

- Bean Validation for request shapes
- explicit parsing and conversion for domain-specific input
- preconditions for internal invariants

Distinguish:

- client input errors
- domain conflicts
- missing resources
- transient remote failures
- internal bugs

## Model Expected Business Outcomes Explicitly

Prefer sealed results or domain-specific exceptions for expected outcomes.

Example:

```kotlin
sealed interface CheckoutResult {
    data class Success(val orderId: OrderId) : CheckoutResult
    data object OutOfStock : CheckoutResult
    data object PaymentDeclined : CheckoutResult
}
```

This is clearer than:

- `Boolean`
- `null`
- generic strings
- giant `ErrorResponse` objects leaking through the whole service layer

## Centralize HTTP Translation

Business code should not know too much about HTTP.

Prefer:

- services returning domain result or throwing domain-specific exception
- resource or exception mapper translating that to HTTP

## Preserve Causes

When wrapping exceptions, keep the cause.

Good:

```kotlin
throw CatalogSyncException("Failed to sync catalog", e)
```

Avoid:

```kotlin
throw RuntimeException("sync failed")
```

## Do Not Swallow Exceptions

Bad:

```kotlin
try {
    repository.persist(entity)
} catch (e: Exception) {
    log.warn("ignored", e)
}
```

Either:

- handle fully and compensate
- or propagate with context

## Coroutines: Never Break Cancellation

If coroutine code catches `CancellationException`, rethrow it.

Do not wrap cancellation into generic domain failures.

## Fault Tolerance

Use retries, timeouts, circuit breakers, fallbacks, or rate limits when a remote dependency justifies them.

Good use:

- flaky remote dependency
- bounded timeout budget
- clear fallback semantics

Bad use:

- masking correctness bugs
- retrying non-idempotent operations blindly
- stacking retries in several layers

Keep resilience policy close to the remote boundary.

## Logging Failures

Rules:

- log with enough context
- avoid duplicate logging in every layer
- avoid logging and then throwing repeatedly unless each layer adds distinct operational value

A good pattern is:

- service adds context when wrapping
- boundary logs once with correlation details

## Review Questions

- Are expected outcomes explicit?
- Are input errors separated from domain conflicts?
- Are exceptions preserved with causes?
- Is cancellation safe in coroutine code?
- Are retries and timeouts intentional and localized?
