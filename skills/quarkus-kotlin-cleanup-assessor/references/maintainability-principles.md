# Maintainability Principles for Quarkus + Kotlin Cleanup

This guide collects the general cleanup principles that should hold even when specific frameworks differ.

## High Cohesion

A class, file, or package should have one clear reason to change.

Strong signals of low cohesion:

- one service handles persistence, validation, mapping, retries, and HTTP details
- one file contains unrelated extensions or helpers for many features
- one package exists only because “all DTOs go here”

Refactor toward:

- one use case per service when possible
- feature-local DTOs and mappers
- adapters that each speak one external protocol

## Low Coupling

Prefer boundaries that reduce blast radius:

- resources depend on services, not on many repositories
- services depend on small collaborators, not giant helper classes
- callers depend on interfaces or contracts only when that abstraction pays for itself

Avoid fake abstraction. An interface with one implementation and no substitution value is not automatically decoupling.

## KISS

Prefer:

- boring, readable control flow
- small and named transformations
- explicit result mapping
- straightforward transaction boundaries

Avoid:

- nested functional chains that hide business meaning
- meta-frameworks inside application code
- “reusable” generic infrastructure that is harder to read than the problem itself

## DRY

Do not duplicate important business rules.

But do not force unrelated things into one abstraction just to remove a few repeated lines.

Good DRY:

- one validation policy used in multiple flows
- one exception-to-HTTP mapping strategy
- one typed config mapping per namespace
- one repository query shared by several services

Bad DRY:

- giant helper with ten optional parameters
- generic base resource or base service hiding all specifics
- one mapper reused across unrelated boundaries and becoming harder to evolve

## YAGNI

Delete or avoid:

- extension points nobody uses
- asynchronous abstractions without a real concurrency need
- complicated domain layering in simple CRUD services
- pre-emptive interface hierarchies

## SRP and SOLID, Applied Practically

### Single Responsibility

Use one service per coherent workflow, not one 900-line service per bounded context.

### Open/Closed

Extend by adding focused collaborators or sealed variants, not by piling conditionals into god classes.

### Liskov

Avoid inheritance hierarchies that weaken invariants or require “unsupported” overrides.

### Interface Segregation

Prefer small adapters:

- `PaymentAuthorizer`
- `InvoicePublisher`
- `CustomerFinder`

over giant “manager” interfaces.

### Dependency Inversion

Depending on abstractions helps when:

- the dependency is external or unstable
- the boundary deserves contract tests
- you want cleaner test doubles

It does **not** help when the abstraction just wraps a single trivial call.

## Locality of Change

Code is easier to evolve when one feature’s changes stay inside one feature folder.

Ask during review:

- if I change this endpoint, how many packages move?
- if I change persistence shape, do I leak that change into the whole app?
- if I change one remote API, how many unrelated files need edits?

## Naming Over Comments

Prefer:

- `CreateInvoiceService`
- `CustomerId`
- `CancelSubscriptionPolicy`
- `RetryingCatalogClient`

Over:

- `ServiceUtil`
- `Manager`
- `Helper`
- `Processor`
- `CommonExtensions`

Use comments for intent that the code cannot express clearly, not to narrate obvious code.

## Review Heuristic

A cleanup is good when:

- fewer files need to be opened to understand a feature
- more invariants are expressed by types
- the execution model is clearer
- transaction and error boundaries are obvious
- adding the next feature gets simpler, not harder
