# Architecture, Packages, Modules, and Dependencies

Architecture should reduce the cost and risk of change. Do not optimize for pattern count.

## Repository-first shape

Before restructuring, map one representative flow end to end:

- entry point (HTTP/message/job/CLI)
- validation and authorization
- orchestration/domain logic
- persistence/remote systems
- transaction and execution model
- errors and observability

Identify real dependency direction, not package names alone.

## Package organization

Package by feature is a strong default for business applications because it keeps change-local code together. Layer packages can work for small/simple systems or strong horizontal platforms. A hybrid is often appropriate.

Do not perform a mass package move without a measurable problem such as cycles, ownership confusion, or repeated cross-feature change. Package changes affect reflection, serialization, JPMS, CDI indexing, test access, and configuration.

## Boundaries

Create a boundary when it isolates:

- an external system or framework
- a volatile business policy
- a test seam that cannot be achieved more simply
- a different lifecycle/transaction/execution model
- an independently deployable or owned module

Do not create a port, adapter, use case, interface, mapper, and DTO for every method by default.

## Interfaces

Prefer an interface when there are multiple meaningful implementations, a public extension contract, or an external boundary that benefits from substitution. A test alone is not always a reason; concrete classes can often be tested directly with injected collaborators.

Avoid “IThing” naming, marker interfaces without semantics, and interfaces that mirror every public method of one implementation forever.

## Inheritance

Use inheritance for substitutability, not merely code reuse. Warning signs:

- subclasses reject base operations
- template methods require many hooks/flags
- protected state couples implementations
- equality becomes ambiguous
- framework proxies/subclasses interact unpredictably

Prefer composition/delegation for variation.

## Utility code

A focused stateless utility class can be appropriate. Avoid `Utils`, `Common`, or `Helper` dumping grounds. Group behavior by domain concept and keep dependencies explicit. Static methods are poor seams when they hide time, I/O, global state, or configuration.

## Modules

Introduce a Maven/Gradle module when it provides a real build/dependency/ownership boundary. Each module adds configuration, publication, test, and versioning cost.

Check for:

- cycles
- duplicated models
- leaking implementation dependencies
- split packages
- annotation processor/generated-source flow
- integration-test placement
- Quarkus application versus library/extension boundaries

## JPMS

Do not add `module-info.java` opportunistically. If JPMS is already used, preserve exported/opened packages, reflection requirements, service providers, and module-path testing. `opens` and `exports` have different semantics; native-image/CDI reflection may add further constraints.

## Dependency direction

Business policy should not require transport or persistence details unless the application intentionally embraces a framework-centric model. Keep dependency inversion proportional: adapters for volatile/external concerns, direct framework use for simple stable concerns when it reduces ceremony.

## Dependency additions

Before adding a library:

- verify the need is not already met by JDK/project stack
- check BOM/version alignment and license/security policy
- evaluate transitive size and native compatibility
- avoid two libraries for the same concern
- confirm maintenance and release compatibility
- add tests around the boundary it introduces

Do not upgrade unrelated dependencies while adding one capability.

## Domain modeling

Use types to prevent meaningful mix-ups and invalid states. Avoid primitive obsession when identifiers, money, units, states, or validated strings have distinct rules. Do not wrap every primitive without value; target high-risk ambiguity.

Anemic data plus giant service is not automatically wrong, but domain rules scattered across controllers, repositories, and mappers make invariants hard to protect.

## Architecture review questions

- Which changes currently require touching many unrelated places?
- Which dependencies are volatile or hard to test?
- Are transaction and execution boundaries visible?
- Are packages/modules aligned with ownership and change?
- Does every abstraction pay for itself?
- Are framework details leaking into public/domain contracts unnecessarily?
- Would deleting a layer make the system clearer without losing a boundary?
