# Refactoring Playbook

Use this guide for symptom-to-fix cleanup.

## Symptom: Spring-Shaped Quarkus Code

Signs:

- Spring Web or Spring DI compatibility annotations all over new code
- Spring Data habits used as the house style
- Quarkus-native options ignored

Cleanup:

- migrate new or touched code toward Jakarta REST, CDI, Quarkus config, and Panache or explicit repositories
- keep compatibility layers only where migration pressure still justifies them
- stop copying Spring Boot patterns into new features

## Symptom: Huge Resource Classes

Signs:

- resource performs validation, transactions, persistence, retries, mapping, and HTTP composition
- resource methods exceed one screen

Cleanup:

- extract one application service per use case
- keep resource focused on HTTP
- centralize exception mapping

## Symptom: `!!` Everywhere

Signs:

- normal code relies on `!!`
- request parsing is nullable chaos
- domain invariants are not encoded

Cleanup:

- tighten types
- validate at boundaries
- use sealed outcomes or preconditions
- replace raw nullable primitives with value objects where useful

## Symptom: Giant `Util.kt` and `Extensions.kt`

Signs:

- unrelated helpers across many features
- hidden business logic in extensions
- impossible ownership

Cleanup:

- move helpers next to the owning feature
- split by domain
- delete helpers used once
- keep only genuinely cross-cutting utilities

## Symptom: Active Record Has Taken Over

Signs:

- entity companion objects are huge
- services call entity helpers directly everywhere
- transaction ownership is unclear

Cleanup:

- introduce repositories
- move queries there
- keep companion helpers only for tiny entity-local query shortcuts

## Symptom: Entity Leaks into API

Signs:

- resources return entities directly
- lazy loading problems show up in HTTP
- API changes blocked by persistence model

Cleanup:

- add response DTOs
- map entities to API-safe models
- keep entity classes persistence-oriented

## Symptom: Execution Model Soup

Signs:

- `Uni`, `suspend`, blocking JPA, and virtual threads mixed per request
- nobody knows which code runs where
- event-loop blocking warnings

Cleanup:

- choose one model per entry point
- annotate boundaries explicitly
- remove `runBlocking` from request paths
- move blocking work off the event loop

## Symptom: Scattered Configuration

Signs:

- dozens of `@ConfigProperty` strings
- URLs and timeouts repeated
- production secrets hard to trace

Cleanup:

- group config with Config Mappings
- centralize integration config
- document profile behavior

## Symptom: No Migration Discipline

Signs:

- schema managed manually
- auto-ddl relied on in shared environments
- no upgrade history

Cleanup:

- pick Flyway or Liquibase
- codify schema evolution
- validate startup and migration behavior

## Symptom: All Tests Are `@QuarkusTest`

Signs:

- slow test suite
- hard-to-debug failures
- simple business rules boot the whole app

Cleanup:

- move pure logic to plain unit tests
- use `@QuarkusComponentTest` for CDI slices
- reserve `@QuarkusTest` for integration behavior

## Symptom: Logs Are Operationally Weak

Signs:

- repeated stack traces in every layer
- no request or trace context
- no health check meaning

Cleanup:

- log once with context at the boundary
- add structured or centralized logging strategy
- verify readiness and liveness semantics
