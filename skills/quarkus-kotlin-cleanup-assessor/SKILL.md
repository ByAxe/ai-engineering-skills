---
name: quarkus-kotlin-cleanup-assessor
description: Assesses and refactors Kotlin server-side Quarkus codebases into idiomatic, maintainable Quarkus and Kotlin. Use when the user asks to clean up or modernize a Quarkus service, remove Spring-shaped or Java-shaped anti-patterns, review CDI, REST, configuration, persistence, testing, concurrency, observability, security, or native-readiness without changing behavior. Do not use for Android, Flutter, Ktor, Spring Boot, or generic non-Quarkus JVM codebases.
license: MIT
metadata:
  author: ByAxe
  version: 1.0.0
  category: software-development
  environment: Kotlin JVM server projects built on Quarkus. Works best with repository access and ability to run Maven or Gradle, plus format, lint, test, dev-mode, and build commands.
  tags:
    - kotlin
    - quarkus
    - cdi
    - rest
    - panache
    - coroutines
    - refactoring
    - code-smells
    - native
    - testing
---

# Quarkus Kotlin Cleanup Assessor

Assess a Kotlin server-side Quarkus codebase **after feature work is complete**, then refactor it toward idiomatic Kotlin, Quarkus-native architecture, predictable execution, safe transactions, strong tests, clean observability, and long-term evolvability.

This skill is for **cleanup, reassessment, and structural hardening**. It is **not** a feature-generation skill.

## Important

- Preserve behavior first. Favor incremental refactors that keep HTTP contracts, persistence behavior, messaging contracts, and operational behavior stable unless the user explicitly wants behavior changes.
- Prefer **Quarkus-native APIs and conventions** over Spring compatibility layers. Use Jakarta REST, CDI, Quarkus REST Client, Config Mappings, Panache, Quarkus Scheduler, and Quarkus testing patterns unless the task is specifically about migration compatibility.
- Prefer the **smallest architecture that fits**. Use clear boundaries and package-by-feature. Add extra domain/use-case layers only when they reduce complexity or isolate important business rules.
- Keep transport, orchestration, and persistence responsibilities distinct:
  - resources handle HTTP and transport concerns
  - application services orchestrate workflows and transaction boundaries
  - repositories and adapters hide persistence or remote-system details
- Choose **one execution model per path** on purpose:
  - blocking on worker thread
  - blocking on virtual thread
  - coroutines with `suspend`
  - reactive `Uni` or `Multi`
  Do not mix them casually in the same request flow.
- Keep Kotlin idiomatic:
  - use nullability intentionally
  - avoid `!!`
  - avoid giant `Util` files and generic base classes
  - prefer explicit types, small functions, sealed outcomes, value objects, and focused extensions
- Make refactors measurable. Always include exact verification commands and the expected green path.
- When generated files, migrations, or schema contracts exist, edit the **source of truth**, not the generated artifact.

## Workflow

### Step 1: Establish a Baseline

- Identify:
  - Maven vs Gradle
  - Quarkus version
  - Kotlin version
  - JDK target
  - JVM-only vs JVM + native target
  - major extensions in use: REST, REST Client, ORM, Panache, messaging, scheduler, OIDC, OpenTelemetry, etc.
- Run the narrowest useful baseline:
  - `./mvnw -q test` or `./gradlew test`
  - formatter or lint task if already configured
  - `./mvnw quarkus:dev` or `./gradlew --console=plain quarkusDev` only when a live behavior check is useful
  - native build only when the touched surface or the user request requires it
- Record high-risk flows:
  - authentication and authorization
  - create or update flows
  - transaction-heavy workflows
  - remote client integrations
  - scheduled jobs
  - messaging consumers or producers
  - startup health and readiness behavior

### Step 2: Inventory Architecture, Boundaries, and Execution Model

- Map each vertical slice end-to-end:
  - HTTP or messaging boundary
  - resource or consumer
  - service
  - repository or external client
  - database or remote dependency
- Identify the actual package organization:
  - feature-first
  - layer-first
  - hybrid
  - “clean architecture” with varying real value
- For each important path, note:
  - blocking vs non-blocking
  - `suspend` vs `Uni` vs plain return type
  - where transactions begin and end
  - where exceptions are translated to HTTP or messaging outcomes
- Flag Spring-shaped code in Quarkus:
  - Spring annotations
  - compatibility extensions used as default style
  - controller or service shapes copied from Spring Boot instead of Quarkus idioms

### Step 3: Detect Smells

Classify findings using the reference pack:

- Architecture and package design: `references/quarkus-architecture-principles.md`
- General maintainability: `references/maintainability-principles.md`
- Kotlin language and API design: `references/kotlin-language-and-api-design.md`
- CDI and dependency injection: `references/cdi-and-dependency-injection.md`
- Spring-shaped code and compatibility cleanup: `references/spring-shaped-to-quarkus-native.md`
- REST and HTTP boundaries: `references/rest-and-http-boundaries.md`
- Configuration and secrets: `references/configuration-and-secrets.md`
- Persistence, transactions, and migrations: `references/persistence-transactions-and-migrations.md`
- Panache-specific guidance: `references/panache-kotlin-guidelines.md`
- Async, reactive, coroutines, and virtual threads: `references/async-reactive-coroutines-and-virtual-threads.md`
- Errors, validation, and fault tolerance: `references/errors-validation-and-fault-tolerance.md`
- Testing: `references/testing-strategy.md`
- Security and authorization: `references/security-and-authz.md`
- Logging, health, and telemetry: `references/observability-logging-and-health.md`
- Performance and native readiness: `references/performance-native-and-resource-usage.md`
- Tooling and quality gates: `references/build-tooling-lints-and-quality-gates.md`
- Symptom-to-fix guidance: `references/refactoring-playbook.md`
- Final review pass: `references/assessment-checklists.md`
- Concrete before-and-after examples: `references/idiomatic-examples.md`

### Step 4: Choose a Target Shape

Prefer one of these target shapes:

- **Small service**
  - thin resources
  - one focused service per feature
  - repositories or REST clients as adapters
  - minimal abstractions
- **Medium business service**
  - package by feature
  - explicit application services
  - repositories or adapters per external dependency
  - clear DTO/domain boundaries
  - explicit error translation
- **Integration-heavy or high-concurrency service**
  - clear execution-model choices per entry point
  - careful blocking vs non-blocking boundaries
  - explicit timeouts, retries, and circuit breakers
  - stronger observability and back-pressure awareness

Do **not** add pass-through use cases, generic repositories, or identical model layers just to imitate a pattern catalog.

### Step 5: Refactor in Small Safe Batches

In each batch:

1. pick one smell cluster
2. refactor the smallest useful slice
3. run the smallest relevant verification set
4. record what changed and why

Prefer this order:

1. correctness and transaction safety
2. boundary clarity and API contracts
3. Kotlin type quality and null-safety
4. dependency injection and composition
5. execution model consistency
6. persistence cleanup
7. observability, security, and operational hardening
8. performance and native-readiness

### Step 6: Validate and Harden

- Re-run build, tests, and the key flows touched by the refactor.
- Run static analysis and formatter tasks if present.
- Re-check:
  - exception mapping
  - transaction boundaries
  - event-loop safety
  - native image implications
  - security annotations and config
  - health and telemetry behavior
- Produce a concise change log:
  - what changed
  - why it is more idiomatic Quarkus and Kotlin
  - how to verify
  - what was intentionally deferred

## High-Signal Quarkus + Kotlin Smells

Treat these as priority signals:

### Architecture and Layering

- `resource -> repository` directly for non-trivial workflows
- layer-first mega-packages that hide feature boundaries
- “clean architecture” with five copies of the same data shape and no real boundary value
- generic base services, generic base repositories, or inheritance-heavy frameworks inside app code
- Spring stereotypes or Spring Data patterns used as the default style in a Quarkus app

### Kotlin Smells

- frequent `!!`
- broad nullable types used to avoid thinking about invariants
- `lateinit` used outside framework-managed or persistence-managed cases
- `Util.kt`, `Extensions.kt`, or `Common.kt` becoming dumping grounds
- deeply nested `let`, `run`, `also`, `apply`, `with`
- public APIs returning `Any`, `Map<String, Any?>`, or untyped blobs

### Quarkus and CDI Smells

- field injection everywhere when constructor injection would be simpler
- widespread `@Singleton` with mutable state
- unqualified ambiguous beans
- side-effect-heavy `@PostConstruct`
- abusing producer methods instead of normal beans

### REST Smells

- resource methods doing orchestration, validation, retries, and persistence all at once
- returning raw `Response` everywhere when a typed response would be clearer
- entity classes exposed directly over HTTP
- blocking calls on non-blocking endpoints
- inconsistent exception mapping

### Configuration Smells

- scattered string keys via `@ConfigProperty`
- secrets logged or embedded in code
- no profile strategy
- dev-service assumptions leaking into production setup

### Persistence Smells

- entities used as request or response DTOs
- active-record style spread across a medium or large app
- hidden transactions or transaction boundaries inside resource methods
- schema generation relied on in production instead of migrations
- ORM code accidentally used from event-loop execution

### Async and Concurrency Smells

- `runBlocking` in request paths
- `GlobalScope`
- blocking I/O on the event loop
- mixing `suspend`, `Uni`, blocking JDBC, and virtual threads with no policy
- swallowing `CancellationException`
- compute-heavy work placed on virtual threads

### Testing and Ops Smells

- no pure unit tests for business logic
- everything tested only via `@QuarkusTest`
- transaction-heavy tests that leak data
- missing readiness or liveness checks
- logs without correlation context
- no native verification even though production ships native

## Refactoring Rules by Area

### Architecture

- Prefer package-by-feature over giant package-by-layer structures.
- Keep resources thin and application services focused.
- Keep repositories or adapters specific to one persistence model or remote dependency.
- Delete dead abstractions freely. Removing a useless layer is a valid refactor.

### Kotlin

- Prefer `data class` for DTOs and immutable transport objects.
- Prefer `@JvmInline value class` for type-safe identifiers and constrained primitives when it improves clarity.
- Prefer sealed interfaces or sealed classes for closed outcome sets.
- Prefer default parameters over overload explosions.
- Prefer `require`, `check`, and explicit null handling over `!!`.
- Avoid exposing mutable collections from public APIs.

### CDI

- Prefer constructor injection.
- Default to `@ApplicationScoped` unless `@Singleton` is truly justified.
- Use qualifiers to model multiple implementations.
- Keep lifecycle callbacks small and side-effect-light.

### REST

- Prefer `quarkus-rest` and Quarkus REST Client for new Quarkus code.
- Keep resources transport-focused.
- Validate at the boundary.
- Use central exception translation.
- Return domain-safe response models, not JPA entities.

### Configuration

- Prefer grouped Config Mappings over scattered one-off properties.
- Centralize remote client configuration, timeouts, and feature flags.
- Keep production secrets outside source control and out of logs.

### Persistence

- Use the repository pattern by default for medium and large applications, even if Panache active record is available.
- Keep transaction boundaries explicit.
- Use Flyway or Liquibase when schema history matters in real environments.
- Keep ORM entity modeling separate from public transport contracts.

### Concurrency and Execution Model

- Use blocking worker-thread execution for simple blocking flows when concurrency needs are modest.
- Use `@RunOnVirtualThread` for I/O-bound blocking code when the codebase benefits from synchronous style and the pinning risks are understood.
- Use `suspend` when the involved Quarkus extensions support it and the team wants coroutine-native code.
- Use `Uni` or `Multi` when the path is truly reactive end-to-end or the integration requires reactive semantics.
- Never perform blocking work on the event loop.

### Testing

- Put as much logic as possible under plain Kotlin unit tests.
- Use `@QuarkusComponentTest` for CDI slices.
- Use `@QuarkusTest` for app-level behavior and HTTP integration.
- Use `@TestTransaction` for rollback-friendly persistence tests.
- Use `@InjectMock` or `QuarkusMock` instead of overbuilding test infrastructure.

### Security, Observability, Native

- Use Quarkus security and OIDC features intentionally; do not improvise auth.
- Prefer structured, centralized logging and standard health endpoints.
- Treat native-readiness as a design constraint when native is a real target:
  - serialization choices
  - reflection-heavy libraries
  - resource loading
  - provider selection
  - config at build time vs runtime

## How to Use the Reference Pack

Start narrow:

- unclear package shape or over-abstraction -> `references/quarkus-architecture-principles.md`
- Quarkus app still shaped like Spring Boot -> `references/spring-shaped-to-quarkus-native.md`
- Kotlin smells or API design problems -> `references/kotlin-language-and-api-design.md`
- bean wiring or injection issues -> `references/cdi-and-dependency-injection.md`
- HTTP or REST client issues -> `references/rest-and-http-boundaries.md`
- execution-model confusion -> `references/async-reactive-coroutines-and-virtual-threads.md`
- database or transaction problems -> `references/persistence-transactions-and-migrations.md`
- Panache-specific concerns -> `references/panache-kotlin-guidelines.md`
- test coverage or test type confusion -> `references/testing-strategy.md`
- ready-to-apply examples -> `references/idiomatic-examples.md`
- final pass -> `references/assessment-checklists.md`

Use `assets/quarkus-kotlin-cleanup-assessment-template.md` to structure your assessment output.

## Output Contract

When asked to **assess** a codebase, produce:

1. findings summary
   - top 5 to 10 risks
   - impact
   - confidence
2. target-shape recommendation
   - minimal architecture change vs moderate restructuring vs deeper cleanup
3. staged refactor plan
   - batches
   - safety checks
   - verification commands
4. file-level change map
   - which files or packages to touch first
   - why
5. deferred items
   - things worth fixing later but not in the first cleanup pass

When asked to **refactor** code, implement changes in small batches and include:

- what changed
- why it is more idiomatic Kotlin and Quarkus
- what risk it removes
- how to verify
- what remains intentionally unchanged
