# Source Index and Maintenance Policy

Last researched: **2026-07-10**

Use this index when changing the skill, resolving a version-sensitive claim, or reviewing a recommendation that depends on framework behavior. It is a research map, not permission to copy the newest API into an older project.

## Authority order

When sources disagree, use this order:

1. the target repository's build files, wrappers, lockfiles, generated metadata, tests, and runtime evidence
2. documentation and source for the exact JDK, Quarkus platform, extension, build plugin, and library version in that repository
3. current official Java/OpenJDK/Quarkus/Maven/Gradle documentation
4. issue trackers, release notes, and migration guides for the exact version transition
5. empirical studies and practitioner reports as hypotheses about recurring agent mistakes
6. blogs, tutorials, and generated summaries only as discovery aids

Do not use a current guide to assert that an older Quarkus release has the same annotation, configuration phase, default, or dispatch behavior. Do not use a later JDK improvement to erase risks on the configured JDK.

## Agent Skills open standard

| Source | URL | Used for |
|---|---|---|
| Agent Skills specification | https://agentskills.io/specification | Required `SKILL.md`, frontmatter, optional directories, relative references, progressive disclosure, naming and validation constraints |
| Best practices for skill creators | https://agentskills.io/skill-creation/best-practices | Trigger-focused descriptions, moderate detail, procedures, gotchas, templates, checklists, validation loops, and reusable scripts |
| Optimizing descriptions | https://agentskills.io/skill-creation/optimizing-descriptions | Positive and negative activation cases and description refinement |
| Evaluating skill output quality | https://agentskills.io/skill-creation/evaluating-skills | Baseline-versus-skill evals, expected outputs, assertions, and iteration |
| Using scripts in skills | https://agentskills.io/skill-creation/using-scripts | Self-contained executable helpers and safe script ergonomics |
| Reference implementation | https://github.com/agentskills/agentskills | Validator and standard implementation source |

Design decisions derived from these sources:

- `SKILL.md` remains the compact always-loaded control plane.
- Detailed Java and Quarkus guidance lives in focused `references/` files selected through `00-reference-router.md`.
- Deterministic project inspection and validation logic lives in `scripts/`.
- Output structures live in `assets/`; machine-readable contracts live in `schemas/`.
- Eval coverage includes output behavior and activation boundaries.

The open specification permits a `compatibility` frontmatter field. This bundle omits it because the current `ByAxe/ai-engineering-skills` repository validator allows only `name`, `description`, `license`, `allowed-tools`, and `metadata`. The environment baseline is therefore represented as string metadata and in the body.

## Tessl skill packaging and evaluation

| Source | URL | Used for |
|---|---|---|
| Creating skills | https://docs.tessl.io/create/creating-skills | `tile.json`, workspace/name convention, semantic version, skill path, lint/review/publish workflow |
| Review a skill against best practices | https://docs.tessl.io/evaluate/evaluating-skills | Implementation and activation review dimensions; high review threshold |
| Evaluate skill quality using scenarios | https://docs.tessl.io/evaluate/evaluate-skill-quality-using-scenarios | `evals/instructions.json`, `scenario-N/capability.txt`, `task.md`, weighted `criteria.json`, with/without-skill runs |
| Tessl CLI documentation | https://docs.tessl.io/reference/cli-commands | Installed-command syntax, authentication, project/workspace linkage |

`tile.json` uses `byaxe/effective-java` as the expected workspace-qualified tile name. Change only the workspace prefix when publishing under another Tessl workspace. Run the installed CLI's help before automation because command details can evolve.

## Java language and platform — normative sources

### Java 21 language features

| Source | URL | Skill concerns |
|---|---|---|
| JEP 431: Sequenced Collections | https://openjdk.org/jeps/431 | First/last/reversed collection APIs and encounter-order contracts |
| JEP 440: Record Patterns | https://openjdk.org/jeps/440 | Deconstruction and pattern applicability |
| JEP 441: Pattern Matching for `switch` | https://openjdk.org/jeps/441 | Exhaustiveness, dominance, null handling, sealed hierarchies |
| JEP 444: Virtual Threads | https://openjdk.org/jeps/444 | Thread-per-task model, observability, ThreadLocal cost, no pooling |
| JEP 446: Scoped Values (preview in Java 21) | https://openjdk.org/jeps/446 | Preview status and context propagation alternatives |
| JEP 453: Structured Concurrency (preview in Java 21) | https://openjdk.org/jeps/453 | Preview status, bounded task lifetime, failure propagation |
| JEP 491: Synchronize Virtual Threads without Pinning | https://openjdk.org/jeps/491 | Later-JDK change that must not be projected backward onto Java 21–23 |
| Java 21 language guide: records | https://docs.oracle.com/en/java/javase/21/language/records.html | Record constructors, accessors, generated methods, intended data-carrier semantics |
| Java 21 language guide: pattern matching | https://docs.oracle.com/en/java/javase/21/language/pattern-matching.html | Final language behavior and examples |

### Core API semantics with high agent-error value

| Source | URL | Skill concerns |
|---|---|---|
| `Stream` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Stream.html | Non-interference, statelessness, parallelism, `toList()` contract |
| `List` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html | Unmodifiable factories/copies, null behavior, value-based instances |
| `Map` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Map.html | Duplicate-key behavior, immutable factories, key equality |
| `Optional` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Optional.html | Value-based behavior and absence modeling |
| `BigDecimal` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/math/BigDecimal.html | `double` constructors, scale-sensitive equality, ordering, rounding |
| `Arrays` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Arrays.html | Content equality/hashing versus array object identity |
| `Object` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Object.html | `equals`/`hashCode` contracts |
| `Comparator` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Comparator.html | Ordering consistency and comparator composition |
| `java.time` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/package-summary.html | Instant/local/zoned semantics, clocks, duration/period |
| `Charset` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/charset/Charset.html | Explicit encoding at external boundaries |
| `HttpClient` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/HttpClient.html | Client lifecycle, redirects, executors, timeouts |
| Java serialization specification | https://docs.oracle.com/en/java/javase/21/docs/specs/serialization/ | Compatibility and deserialization risk where legacy serialization exists |
| Java Platform Module System guide | https://docs.oracle.com/en/java/javase/21/migrate/migrating-to-java-platform-module-system.html | Module boundaries and migration constraints |

### Concurrency and diagnostics

| Source | URL | Skill concerns |
|---|---|---|
| `java.util.concurrent` Java 21 API | https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html | Executor ownership, interruption, happens-before, queues and locks |
| Java Flight Recorder guide | https://docs.oracle.com/en/java/javase/21/jfapi/ | Runtime evidence for allocation, blocking, locks, and virtual threads |
| `jcmd` troubleshooting guide | https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html | Thread dumps, JFR control, native memory and runtime diagnostics |
| Java monitoring and management guide | https://docs.oracle.com/en/java/javase/21/management/ | JMX and operational inspection |

## Build tools and dependency truth

| Source | URL | Skill concerns |
|---|---|---|
| Maven Wrapper | https://maven.apache.org/wrapper/ | Repository-pinned Maven execution |
| Maven Compiler Plugin | https://maven.apache.org/plugins/maven-compiler-plugin/ | `release`, toolchains, annotation processing, compiler configuration |
| Maven Toolchains Plugin | https://maven.apache.org/plugins/maven-toolchains-plugin/ | Build JDK selection independent of shell JDK |
| Maven Dependency Plugin | https://maven.apache.org/plugins/maven-dependency-plugin/ | Effective dependency graph and duplicate/conflicting artifacts |
| Maven Enforcer Plugin | https://maven.apache.org/enforcer/maven-enforcer-plugin/ | Version convergence, banned dependencies, build invariants |
| Gradle Wrapper | https://docs.gradle.org/current/userguide/gradle_wrapper.html | Repository-pinned Gradle execution |
| Gradle Java Toolchains | https://docs.gradle.org/current/userguide/toolchains.html | Compile/test/runtime JDK selection |
| Gradle dependency management | https://docs.gradle.org/current/userguide/dependency_management.html | Resolution, constraints, locking, verification |
| Gradle incremental build | https://docs.gradle.org/current/userguide/incremental_build.html | Inputs, outputs, generated sources, cache correctness |

For Maven and Gradle, use documentation matching the wrapper/plugin version whenever behavior or DSL availability matters.

## Quarkus — authoritative current guides

Quarkus performs substantial augmentation and validation at build time. Always inspect the platform BOM and extension versions first; current guides can describe behavior unavailable or different in an older project.

### Project model, build time, and CDI

| Source | URL | Skill concerns |
|---|---|---|
| Quarkus Maven tooling | https://quarkus.io/guides/maven-tooling | Platform BOM, plugins, build goals, native/integration lifecycle |
| Quarkus Gradle tooling | https://quarkus.io/guides/gradle-tooling | Plugin tasks, source sets, test/native lifecycle |
| Writing extensions: build-time model | https://quarkus.io/guides/writing-extensions | Augmentation, build items, recording, build/runtime phases |
| CDI reference (ArC) | https://quarkus.io/guides/cdi-reference | Simplified discovery, Jandex, injection, qualifiers, interceptors, bean removal |
| CDI getting started | https://quarkus.io/guides/cdi | Scopes, producers, events, injection basics in Quarkus |
| Lifecycle guide | https://quarkus.io/guides/lifecycle | Startup/shutdown events and lifecycle ownership |

### REST and remote clients

| Source | URL | Skill concerns |
|---|---|---|
| Quarkus REST | https://quarkus.io/guides/rest | Jakarta REST endpoints, dispatch, blocking/non-blocking behavior, filters, serialization |
| REST Client | https://quarkus.io/guides/rest-client | Client interfaces, configuration, reactive/blocking returns, headers and providers |
| REST JSON | https://quarkus.io/guides/rest-json | Jackson/JSON-B integration and native-aware serialization |
| HTTP reference | https://quarkus.io/guides/http-reference | Server limits, access logs, proxy and transport settings |

### Persistence and transactions

| Source | URL | Skill concerns |
|---|---|---|
| Hibernate ORM with Panache | https://quarkus.io/guides/hibernate-orm-panache | Blocking ORM, active record/repository styles, query semantics, entities |
| Hibernate ORM guide | https://quarkus.io/guides/hibernate-orm | Persistence unit configuration, schema handling, fetch/query behavior |
| Hibernate Reactive with Panache | https://quarkus.io/guides/hibernate-reactive-panache | Reactive sessions, non-blocking transactions, Mutiny composition |
| Transaction guide | https://quarkus.io/guides/transaction | JTA/Narayana boundaries, declarative/programmatic transactions, reactive completion |
| Datasource guide | https://quarkus.io/guides/datasource | JDBC/reactive clients, pools, Dev Services, configuration |
| Flyway guide | https://quarkus.io/guides/flyway | Migration lifecycle, locations, startup behavior, native support |
| Liquibase guide | https://quarkus.io/guides/liquibase | Change log lifecycle, configuration, native support |

Use Hibernate ORM's version-matched documentation for JPA provider details such as entity equality, fetching, dirty checking, flush, and query behavior: https://hibernate.org/orm/documentation/

### Configuration, security, and observability

| Source | URL | Skill concerns |
|---|---|---|
| Configuration reference | https://quarkus.io/guides/config-reference | Source precedence, profiles, build-time versus runtime-fixed behavior |
| Config mappings | https://quarkus.io/guides/config-mappings | Typed grouped configuration and validation |
| All configuration options | https://quarkus.io/guides/all-config | Project-version property discovery aid; confirm exact extension/version |
| Security architecture | https://quarkus.io/guides/security-architecture | Authentication mechanisms, identity, authorization architecture |
| Authorization of web endpoints | https://quarkus.io/guides/security-authorize-web-endpoints-reference | Annotation/path policies and endpoint authorization |
| OIDC bearer token authentication | https://quarkus.io/guides/security-oidc-bearer-token-authentication | Token validation and service security behavior |
| Security testing | https://quarkus.io/guides/security-testing | Identity and authorization tests |
| OpenTelemetry tracing | https://quarkus.io/guides/opentelemetry-tracing | Trace propagation, exporters, spans and error recording |
| Micrometer metrics | https://quarkus.io/guides/telemetry-micrometer | Metric types, tags, binders, cardinality considerations |
| SmallRye Health | https://quarkus.io/guides/smallrye-health | Liveness, readiness, startup, and health contracts |
| Logging | https://quarkus.io/guides/logging | Categories, formats, handlers, structured logging and native behavior |

### Messaging, scheduling, and resilience

| Source | URL | Skill concerns |
|---|---|---|
| Messaging guide | https://quarkus.io/guides/messaging | Channels, emitters, acknowledgement, blocking, execution context |
| Kafka guide | https://quarkus.io/guides/kafka | Connector behavior, failure strategies, exactly/at-least-once implications |
| Scheduler reference | https://quarkus.io/guides/scheduler-reference | Concurrent execution, delayed starts, identity, lifecycle |
| Quartz guide | https://quarkus.io/guides/quartz | Clustered/persistent scheduling and transaction implications |
| SmallRye Fault Tolerance | https://quarkus.io/guides/smallrye-fault-tolerance | Retry, timeout, circuit breaker, fallback, bulkhead semantics |

### Concurrency, tests, Dev Services, and native

| Source | URL | Skill concerns |
|---|---|---|
| Virtual threads | https://quarkus.io/guides/virtual-threads | `@RunOnVirtualThread`, workload fit, pinning/version nuance, ThreadLocal and downstream limits |
| Mutiny primer | https://quarkus.io/guides/mutiny-primer | `Uni`/`Multi` semantics, failure/cancellation composition |
| Testing guide | https://quarkus.io/guides/getting-started-testing | `@QuarkusTest`, profiles, mocks, resources, integration tests |
| Component testing | https://quarkus.io/guides/testing-components | Focused ArC component tests and augmentation behavior |
| Dev Services overview | https://quarkus.io/guides/dev-services | Ephemeral dependencies, lifecycle, container prerequisites |
| Native reference | https://quarkus.io/guides/building-native-image | Native toolchain and build modes |
| Native application tips | https://quarkus.io/guides/writing-native-applications-tips | Reflection, resources, proxies, initialization, troubleshooting |
| Native reference guide | https://quarkus.io/guides/native-reference | Native diagnostics, substitutions, build/runtime constraints |

### Spring compatibility and migration

| Source | URL | Skill concerns |
|---|---|---|
| Spring DI compatibility | https://quarkus.io/guides/spring-di | Supported Spring annotations and differences from full Spring |
| Spring Web compatibility | https://quarkus.io/guides/spring-web | Supported controller model and limitations |
| Spring Data JPA compatibility | https://quarkus.io/guides/spring-data-jpa | Repository compatibility subset and Panache alternatives |
| Spring Security compatibility | https://quarkus.io/guides/spring-security | Supported annotations and Quarkus security differences |
| Spring Boot properties compatibility | https://quarkus.io/guides/spring-boot-properties | Configuration mapping and limitations |

Compatibility extensions are not proof that full Spring runtime semantics exist. Verify supported annotation subsets, proxies, transactions, events, configuration, tests, and operational behavior for the installed extension.

## Testing, static analysis, and architecture tools

The skill does not force these tools into a repository. Use them when already configured or when the user explicitly approves adoption.

| Tool | Official source | Typical evidence |
|---|---|---|
| JUnit 5 | https://junit.org/junit5/docs/current/user-guide/ | Unit, parameterized, dynamic, extension, and integration test contracts |
| Mockito | https://javadoc.io/doc/org.mockito/mockito-core/latest/org.mockito/org/mockito/Mockito.html | Test-double behavior and strictness; avoid mocking the subject under test |
| AssertJ | https://assertj.github.io/doc/ | Domain-readable assertions |
| jqwik | https://jqwik.net/docs/current/user-guide.html | Property-based invariants for parsers, models, and stateful logic |
| Testcontainers | https://java.testcontainers.org/ | Real dependency integration tests where containers are available |
| ArchUnit | https://www.archunit.org/userguide/html/000_Index.html | Executable package/module dependency rules |
| Error Prone | https://errorprone.info/docs | Compiler-time bug patterns |
| NullAway | https://github.com/uber/NullAway/wiki | Nullness checking when the project adopts its annotation model |
| SpotBugs | https://spotbugs.readthedocs.io/ | Bytecode-level bug candidates |
| PMD | https://docs.pmd-code.org/latest/ | Source rules and project-specific smells |
| Checkstyle | https://checkstyle.org/ | Style/structure enforcement, not semantic correctness |
| Spotless | https://github.com/diffplug/spotless | Reproducible formatting |
| JaCoCo | https://www.jacoco.org/jacoco/trunk/doc/ | Coverage evidence; coverage percentage alone is not correctness |
| JMH | https://openjdk.org/projects/code-tools/jmh/ | JVM microbenchmark harness; avoid ad hoc stopwatch benchmarks |

## Security sources

| Source | URL | Skill concerns |
|---|---|---|
| OWASP ASVS | https://owasp.org/www-project-application-security-verification-standard/ | Verification-oriented application security requirements |
| OWASP Java Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html | Java-specific secure coding checks |
| OWASP SSRF Prevention | https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html | Outbound URL/address validation and DNS/rebinding concerns |
| OWASP Deserialization | https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html | Unsafe object deserialization and allow-listing |
| CWE | https://cwe.mitre.org/ | Stable weakness taxonomy for findings |

Treat authentication, role checks, object/tenant ownership, and data-policy authorization as separate controls. Treat logs, traces, and metrics as data egress surfaces.

## Empirical research on AI-generated code and skills

These sources motivate adversarial eval cases and evidence gates. They do **not** establish that every generated Java patch has the reported defect or that one language is universally easier for agents.

| Study | URL | How this bundle uses it |
|---|---|---|
| Investigating the Smells of LLM Generated Code (2025) | https://arxiv.org/abs/2510.03029 | Motivates targeted checks for generated-code smells and comparisons against human code, while requiring repository proof |
| SWE-Skills-Bench (2026) | https://arxiv.org/abs/2603.15401 | Motivates version/scope-sensitive skill evaluation and with/without-skill comparisons |
| Assessing the Quality and Security of AI-Generated Code (2025) | https://arxiv.org/abs/2508.14727 | Motivates correctness/security evaluation beyond compilation |
| SafeGenBench (2025) | https://arxiv.org/abs/2506.05692 | Motivates security-focused generation and grading scenarios |

Before citing a study externally, inspect its task construction, model set, language coverage, sample size, metric validity, and publication status. Avoid turning benchmark observations into universal claims about Java, Rust, or all coding agents.

## Repository sources used for replacement coverage

| Source | URL | What was retained or strengthened |
|---|---|---|
| Repository README | https://github.com/ByAxe/ai-engineering-skills/blob/main/README.md | Installation, validation, skill layout, Tessl workflow, and Java catalog integration |
| Legacy Java refactoring skill | https://github.com/ByAxe/ai-engineering-skills/blob/main/skills/java-refactoring/SKILL.md | Behavior-preserving refactoring, smell evidence, staged plans, SOLID as heuristic |
| Legacy Java 21 assessor | https://github.com/ByAxe/ai-engineering-skills/blob/main/skills/java-21-refactor-assessor/SKILL.md | Java 21 language/concurrency modernization and Python-shaped Java checks |
| Legacy smell catalog | https://github.com/ByAxe/ai-engineering-skills/blob/main/skills/java-refactoring/references/code-smells-catalog.md | Classic smell/refactoring vocabulary, expanded with semantic and agent-specific failure modes |
| Quarkus Kotlin assessor | https://github.com/ByAxe/ai-engineering-skills/blob/main/skills/quarkus-kotlin-cleanup-assessor/SKILL.md | Repository-specific depth, reference routing, Quarkus execution/persistence/testing/native topic coverage |
| Repository validator | https://github.com/ByAxe/ai-engineering-skills/blob/main/scripts/validate_skills.py | Frontmatter compatibility and local quick-check behavior |

See `migration/legacy-coverage-map.md` for the file-level replacement map.

## Review cadence

Review the following at least quarterly or before a platform upgrade:

- Agent Skills and Tessl schemas and CLI commands
- Java LTS and preview-feature status
- Quarkus BOM, extension names, dispatch rules, CDI discovery/removal, config phases, test APIs, and native guidance
- Maven/Gradle wrapper and plugin capabilities
- security recommendations and deprecated algorithms/protocols

For every update:

1. record the target versions and date
2. update only claims affected by the source change
3. add or update an eval that would catch the old failure
4. run `scripts/validate_skill.py`, unit tests, and available external skill review tools
5. increment `tile.json`, frontmatter metadata, and `CHANGELOG.md` together
