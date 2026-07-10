# Reference Router

Load only the smallest set that addresses the task. The table is intentionally trigger-based: do not read every file before acting.

| Evidence or task trigger | Primary reference | Add when needed |
|---|---|---|
| large, polished, or suspicious agent patch | `agent-failure-modes.md` | `evidence-first-workflow.md`, `review-checklists.md` |
| uncertain root cause or risky change | `evidence-first-workflow.md` | domain-specific reference |
| Java release, records, sealed types, pattern matching | `modern-java-language-and-modeling.md` | `version-policy.md`, `compatibility-public-apis-and-migrations.md` |
| public method or type design, null, generics | `api-design-nullness-and-generics.md` | `compatibility-public-apis-and-migrations.md` |
| lists, maps, sets, streams, collectors | `collections-streams-and-mutability.md` | `equality-ordering-numerics-and-time.md` |
| equality, hashes, sorting, money, clock, locale | `equality-ordering-numerics-and-time.md` | persistence reference for entities |
| exceptions, files, HTTP, JSON, resources | `exceptions-resources-io-and-serialization.md` | security reference for untrusted input |
| threads, futures, locks, reactive, virtual threads | `concurrency-virtual-threads-and-async.md` | relevant Quarkus execution reference |
| package or module restructuring | `architecture-packages-modules-and-dependencies.md` | compatibility and build references |
| POM, Gradle, toolchain, dependencies, generated code | `build-maven-gradle-and-generated-code.md` | `version-policy.md` |
| test design, mocking, flaky behavior, debugging | `testing-debugging-and-test-doubles.md` | Quarkus test reference when applicable |
| authorization, injection, path/URL input, secrets | `security-input-boundaries-and-secrets.md` | Quarkus security reference |
| JPA/Hibernate/database/migration | `persistence-jpa-and-transactions.md` | Quarkus persistence reference |
| latency, throughput, memory, allocation, startup | `performance-profiling-and-allocation.md` | concurrency/native references |
| public API, wire format, schema, upgrade | `compatibility-public-apis-and-migrations.md` | language/build/persistence reference |
| Quarkus project detected | `quarkus-project-model-and-build-time.md` | choose the exact Quarkus area below |
| CDI, injection, scopes, interceptors | `quarkus-cdi-and-lifecycle.md` | project/build-time reference |
| REST endpoint/client or event-loop behavior | `quarkus-rest-clients-and-execution-model.md` | concurrency/security references |
| Quarkus ORM, Panache, reactive persistence | `quarkus-persistence-and-transactions.md` | general persistence reference |
| Quarkus config, OIDC, metrics, tracing, health | `quarkus-config-security-observability.md` | security reference |
| messaging, scheduler, retry, circuit breaker | `quarkus-messaging-scheduling-and-fault-tolerance.md` | concurrency/persistence references |
| Quarkus tests, Dev Services, native executable | `quarkus-testing-dev-services-and-native.md` | build/performance references |
| Spring annotations or mental model in Quarkus | `spring-to-quarkus-migration.md` | relevant Quarkus area |
| broad smell inventory or staged cleanup | `smell-and-refactoring-catalog.md` | `review-checklists.md` |
| final review | `review-checklists.md` | output asset in `assets/` |
| updating this skill | `source-index.md` | `version-policy.md`, evals |

## Minimal load sets

### Small Java fix

1. `evidence-first-workflow.md`
2. one domain reference
3. `testing-debugging-and-test-doubles.md`

### Java 21 modernization

1. `version-policy.md`
2. `modern-java-language-and-modeling.md`
3. `compatibility-public-apis-and-migrations.md`
4. domain reference for the changed behavior

### Quarkus refactor

1. `quarkus-project-model-and-build-time.md`
2. one or two area-specific Quarkus references
3. `testing-debugging-and-test-doubles.md`
4. `review-checklists.md`

### Broad assessment

1. profile the project with `scripts/profile_java_project.py`
2. `agent-failure-modes.md`
3. `smell-and-refactoring-catalog.md`
4. domain references only for evidence found
5. `review-checklists.md`

## Evidence rule

A reference gives hypotheses and decision rules. It does not prove a repository has a defect. Tie every conclusion to project code, build configuration, tests, runtime evidence, or an explicit contract.
