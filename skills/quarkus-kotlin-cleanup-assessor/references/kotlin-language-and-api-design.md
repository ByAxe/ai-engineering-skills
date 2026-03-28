# Kotlin Language and API Design Guidance

Use this guide to remove Java-shaped and “just make it compile” Kotlin from a Quarkus service.

## Prefer Kotlin, Not Java-in-Kotlin Syntax

Prefer:

- expression bodies when they remain readable
- immutable `val` by default
- default parameters instead of overload explosions
- named data carriers
- strong nullability
- focused extension functions
- value classes and sealed hierarchies when they simplify intent

Avoid:

- overusing mutable state
- pretending nullability does not exist
- helper methods copied from Java utility style
- enormous companion objects or file-level dumping grounds

## Data Classes

Good uses:

- request and response DTOs
- event payloads
- simple immutable state carriers
- mapping targets between layers

Prefer:

```kotlin
data class CustomerResponse(
    val id: CustomerId,
    val email: String,
    val displayName: String,
)
```

Avoid using `data class` for JPA entities. Generated equality, copy, and component functions usually do not fit persistence identity and lifecycle semantics well.

## Nullability Is a Design Tool

Prefer making absence explicit:

- `Customer?` when “missing customer” is a real case
- sealed results when several outcomes are possible
- `requireNotNull` or explicit translation at boundaries

Avoid:

- broad nullable graphs everywhere
- `!!` in normal business code
- returning null when the caller really needs an explicit failure reason

Replace:

```kotlin
val userId = request.userId!!
```

With:

```kotlin
val userId = requireNotNull(request.userId) { "userId is required" }
```

Or a boundary-level validation strategy.

## `lateinit`

Acceptable:

- some framework-managed fields
- JPA entity fields when the persistence model really requires it
- tests with explicit setup

Not acceptable as a general escape hatch for normal application services.

Smell:

- many services with `lateinit` dependencies instead of constructor injection
- domain objects with `lateinit` because invariants are unclear

## Value Classes

Use `@JvmInline value class` when a primitive wrapper adds real meaning:

```kotlin
@JvmInline
value class CustomerId(val value: UUID)

@JvmInline
value class EmailAddress(val value: String)
```

Good uses:

- IDs
- domain-specific strings or numbers
- strongly typed parameters that would otherwise be confused

Avoid them when they would complicate serialization or persistence with no clarity benefit. Use them where the team can support the mapping cleanly.

## Sealed Results and State

Prefer sealed hierarchies for closed outcome sets:

```kotlin
sealed interface CreateCustomerResult {
    data class Success(val id: CustomerId) : CreateCustomerResult
    data object EmailTaken : CreateCustomerResult
    data class InvalidInput(val message: String) : CreateCustomerResult
}
```

This is usually clearer than:

- `Boolean`
- magic strings
- `Map<String, Any?>`
- generic `Result<Any?>`

## Scope Functions

Scope functions are useful, but easy to overuse.

Good:

- a short local transformation
- builder-style setup
- one clear object context

Bad:

- multiple nested `let/apply/also/run`
- a pipeline that hides business meaning
- using `also` for side effects in the middle of core logic

Prefer naming intermediate values when the chain stops being obvious.

## Collections

Prefer read-only collection types in APIs:

- `List<T>`
- `Set<T>`
- `Map<K, V>`

Avoid leaking `MutableList`, `MutableSet`, or `MutableMap` from public APIs unless mutation is the explicit contract.

## Extension Functions

Good uses:

- small, local conversions
- type-specific helpers near the owning feature
- readability improvements with obvious meaning

Bad uses:

- giant `Extensions.kt` shared by the whole codebase
- hidden business logic in surprise extensions
- extensions that make call sites ambiguous

## Top-Level Functions

Good for:

- pure local helpers
- small mapping functions
- feature-local utilities

Keep them near the feature. Do not centralize everything into generic util files.

## Public API Style

Prefer public functions and classes that make contracts obvious:

- explicit return types on public functions
- stable names
- clear nullable vs non-nullable behavior
- typed identifiers rather than raw strings

Example:

```kotlin
fun findCustomer(id: CustomerId): Customer?
```

is clearer than:

```kotlin
fun findCustomer(id: String): Any?
```

## Exceptions and Preconditions

Kotlin exceptions are unchecked. Use them deliberately.

Prefer:

- `require(...)` for caller input
- `check(...)` for internal state
- domain-specific exceptions when they simplify boundary translation
- sealed results for expected business outcomes

Avoid:

- catching broad `Exception` in the middle of business code
- turning every error into `null`
- `runCatching` that swallows important control flow or cancellation

## File and Type Naming

Avoid meaningless names:

- `Util.kt`
- `Common.kt`
- `Extensions.kt`
- `Manager.kt`

Prefer names that describe the content:

- `OrderRequests.kt`
- `PriceCalculation.kt`
- `InvoiceStatusMapper.kt`
- `CustomerLookupService.kt`

## Kotlin Review Questions

- Are types doing real work?
- Can nullability be tightened?
- Is `!!` avoidable?
- Are scope functions improving clarity or hiding it?
- Are data classes used where identity and immutability make sense?
- Are file names descriptive?
