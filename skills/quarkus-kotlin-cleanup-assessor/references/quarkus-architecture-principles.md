# Quarkus Architecture Principles for Kotlin Server Code

This guide defines the preferred architectural end-state for a Kotlin + Quarkus service cleanup.

## Goal

Move the codebase toward:

- explicit boundaries
- package-by-feature organization
- minimal but meaningful layering
- Quarkus-native conventions instead of Spring-shaped defaults
- low coupling, high cohesion, and change-friendly slices

## Prefer Package by Feature

Prefer this:

```text
src/main/kotlin/com/acme/orders/
  api/
    OrderResource.kt
    OrderRequests.kt
    OrderResponses.kt
  application/
    CreateOrderService.kt
    GetOrderService.kt
  domain/
    Order.kt
    OrderId.kt
    OrderPolicy.kt
  infra/
    OrderRepository.kt
    OrderEntity.kt
    OrderEntityMapper.kt
    PaymentGatewayClient.kt
```

Over this:

```text
controller/
service/
repository/
dto/
entity/
util/
```

Package-by-feature makes it easier to:

- understand one vertical slice
- refactor one feature without touching the whole codebase
- keep DTOs, domain types, and persistence details local to a feature
- delete dead code safely

## Use the Smallest Useful Layer Stack

Default target stack:

- **resource** for HTTP transport concerns
- **application service** for orchestration and transaction boundaries
- **repository or adapter** for persistence or remote systems
- **domain types** when business rules deserve stable names and invariants

Add a dedicated domain/use-case layer only when it buys something real:

- the same rules are used by multiple entry points
- workflows are complex and need naming
- invariants matter and deserve strong types
- persistence should be kept clearly out of business policy

Do **not** add layers when every method is pass-through.

## Thin Resources, Focused Services

Resource responsibilities:

- deserialize request
- validate request shape
- call the service
- map result to transport response
- translate errors consistently

Service responsibilities:

- orchestrate one coherent use case
- own transaction boundaries when needed
- coordinate repositories and clients
- enforce business rules that belong to the use case

Repository or adapter responsibilities:

- persistence queries
- mapping entities to domain or transport-safe models
- remote system protocol details
- technical retries only when clearly local to the integration

## Avoid Clean Architecture Theater

Smells:

- `CreateOrderUseCase` that only calls `CreateOrderService`
- `OrderDomainModel`, `OrderDto`, `OrderResponse`, `OrderEntity`, `OrderView`, all with the same fields and no transformation value
- interfaces introduced only because “there should be an interface”
- generic base classes that hide the actual workflow

Keep only the boundaries that protect change.

## Prefer Quarkus-Native Composition

In Quarkus code, prefer:

- Jakarta REST resources instead of Spring MVC controllers
- CDI scopes and qualifiers instead of Spring DI defaults
- Quarkus REST Client instead of Spring OpenFeign-style habits
- Config Mappings instead of Spring configuration classes for new code
- Panache or explicit repositories instead of Spring Data as the default house style
- Quarkus Scheduler instead of pulling in Quartz unless you actually need clustering or persistence

Compatibility layers are useful for migration. They are usually not the clean target style for a Quarkus-native codebase.

## Keep Feature Boundaries Vertical

For each feature ask:

- what are the entry points?
- what data does it own?
- what services or repositories are specific to it?
- what external dependencies does it call?
- can this feature be tested in isolation?

If a feature cannot be reasoned about locally, the package structure is probably too horizontal.

## Make Execution Model a First-Class Boundary

Every entry point should make its model obvious:

- plain blocking
- blocking on virtual threads
- coroutine `suspend`
- reactive `Uni` or `Multi`

Smell:

- resource returns `Uni`
- service uses blocking JPA
- helper wraps blocking work in ad-hoc coroutine code
- nobody knows which thread model is in effect

Pick one model per path and enforce it consistently.

## Typical Target Shapes

### Shape A: Small CRUD Service

Good for:

- low business complexity
- mostly direct persistence with light validation

Pattern:

- resource
- service
- repository
- DTOs
- entity

Keep it simple. Do not invent a domain layer without reason.

### Shape B: Business Workflow Service

Good for:

- meaningful domain rules
- multiple validation or decision points
- several collaborators

Pattern:

- resource
- application services
- domain types or policies
- repositories and clients
- explicit error/result models

### Shape C: Integration-Heavy Service

Good for:

- several remote dependencies
- retries, timeouts, circuit breakers
- multiple asynchronous boundaries

Pattern:

- resource or consumer
- orchestration service
- adapters per dependency
- execution-model policy per path
- strong observability
- explicit error translation

## What to Delete During Cleanup

Safe targets for deletion:

- empty marker interfaces with no real role
- pass-through services
- duplicated mappers with trivial one-to-one copies and no boundary value
- shared “common” packages that only hide ownership
- Spring compatibility abstractions that are not needed anymore

## Architecture Review Questions

Use these questions during assessment:

- Can I explain a feature by opening one folder?
- Is there one obvious place for transactions?
- Are HTTP concerns confined to resources?
- Do repositories know only persistence, not business orchestration?
- Is the execution model obvious for each entry point?
- Are there fewer abstractions after cleanup, not more?
