# Spring-Shaped Java to Quarkus-Native Java

Quarkus can support selected Spring APIs through compatibility extensions, but a safe migration is semantic, not an annotation search-and-replace. Preserve contracts while moving one vertical slice at a time.

## 1. Decide the target

Clarify whether the goal is:

- run existing Spring-style code on Quarkus through compatibility extensions
- gradually adopt Quarkus-native APIs
- complete framework migration
- only clean up new Quarkus code that copied Spring habits

Compatibility is a valid transitional strategy. Do not remove it solely for aesthetic purity when the cost/risk exceeds the benefit.

## 2. Inventory before editing

Map:

- Spring Boot version and starters/auto-configuration
- Quarkus version/platform/extensions
- `org.springframework.*` annotations and APIs
- servlet versus reactive web stack
- bean scopes, conditions, profiles, factories, events, lifecycle
- transactions, async, scheduling, retry/circuit breaker
- Spring Data repositories and query derivation
- configuration properties and environment access
- security filter chain/method security
- Actuator health/metrics
- test slices, context caching, mock facilities
- reflection/classpath scanning/native assumptions

Generate a per-feature migration matrix rather than a global annotation count.

## 3. Dependency injection

Typical mapping direction:

| Spring concept | Quarkus-native consideration |
|---|---|
| `@Component`, `@Service`, `@Repository` | CDI scope such as `@ApplicationScoped`; use scope intentionally |
| constructor injection | supported; often single constructor without `@Inject` |
| `@Autowired` | CDI `@Inject` or simplified constructor injection |
| `@Qualifier("name")` | type-safe CDI qualifier; string identifier only when justified |
| `@Bean` in `@Configuration` | CDI producer for external/conditional construction |
| `@Primary` | CDI alternatives/default bean/priority depending on use case |
| `@Lazy` | understand ArC normal-scope laziness/startup behavior |
| conditional bean | Quarkus build profile/property conditions or runtime strategy, depending phase |

Do not replace every Spring stereotype with `@Singleton`. Scope and proxy semantics differ.

## 4. Component scanning versus indexing

Spring’s runtime scanning/auto-configuration mental model does not transfer directly. Quarkus discovers indexed beans during augmentation.

For library beans:

- provide an index where appropriate
- use explicit dependency indexing
- expose a producer/adapter
- use a Quarkus extension for deep integration

Do not add broad classpath scanning to recreate Spring Boot; it undermines build-time optimization and native compatibility.

## 5. Configuration

Spring `@ConfigurationProperties`, `Environment`, relaxed binding, and profile semantics differ from SmallRye Config/Quarkus.

Migrate by contract:

1. enumerate canonical keys and aliases
2. classify defaults and required secrets
3. map profile/environment behavior
4. choose `@ConfigMapping` or focused injection
5. validate build-time/runtime phase
6. test actual environment variable names
7. preserve deprecation aliases during rollout if external deployments use them

Do not assume identical kebab/camel/underscore conversion or dynamic refresh semantics.

## 6. Web layer

Spring MVC/WebFlux controllers and Quarkus REST resources differ in:

- annotations and parameter binding
- exception handling
- validation
- content negotiation
- filters/interceptors
- thread dispatch
- reactive types and context
- security integration

Preserve endpoint paths, status codes, headers, media types, payloads, and error envelopes with contract tests before replacing annotations.

A WebFlux `Mono` is not mechanically equivalent to Mutiny `Uni`; cancellation, context, operator semantics, and integration libraries differ. Prefer a clear boundary adapter during staged migration.

## 7. Transactions

Do not translate transaction annotations without tracing interception and execution model.

Check:

- rollback rules for checked/runtime exceptions
- propagation/isolation actually used
- self-invocation assumptions
- private/final method behavior
- reactive versus blocking transaction model
- transaction synchronization/event publication
- test transaction behavior

If code depends on a Spring-specific propagation mode or synchronization callback, design an explicit Quarkus/Jakarta equivalent and test it.

## 8. Persistence and Spring Data

Spring Data repository interfaces and derived queries may be replaced with:

- Panache active record
- Panache repository
- plain Hibernate ORM/JPA
- Hibernate Reactive/Panache Reactive

Do not generate a generic base repository hierarchy to mimic Spring Data. Migrate queries one feature at a time, preserving pagination, sorting, locking, projections, auditing, and exception translation.

Database constraints and migration history remain framework-independent contracts.

## 9. Security

Spring Security filter chains, request matchers, method security, CSRF/session behavior, OAuth2 resource server/client, and Quarkus security/OIDC are not annotation equivalents.

Build a route/permission matrix:

- unauthenticated
- authenticated wrong role
- right role wrong tenant/resource
- allowed
- browser/session-specific behavior
- preflight/static/admin/health routes

Migrate denial/challenge status and error behavior deliberately. Do not claim parity from a successful login test alone.

## 10. Events and lifecycle

Spring events, `ApplicationRunner`, `CommandLineRunner`, `@PostConstruct`, context refresh listeners, and Quarkus startup/observer semantics differ.

For each callback, classify:

- once per artifact startup versus dev-mode restart
- synchronous versus async
- request context availability
- transaction timing
- failure policy/readiness effect
- shutdown cleanup

Avoid moving all startup behavior into one giant observer.

## 11. Async and scheduling

`@Async`, task executors, schedulers, Reactor, and Quarkus worker/reactive/virtual-thread models need explicit migration.

Name:

- executor owner and bounds
- context propagation
- ordering
- cancellation
- cluster-singleton requirement
- retry/idempotency
- graceful shutdown

Do not preserve a Spring executor bean automatically when Quarkus/framework-managed execution is more appropriate. Do not replace it without proving workload behavior.

## 12. Fault tolerance

Spring Retry/Resilience4j and MicroProfile/SmallRye Fault Tolerance differ in annotation semantics, configuration keys, exception selection, fallback signatures, and metrics.

Protect total deadline, attempts, idempotency, fallback outcome, and circuit/bulkhead behavior with failure tests.

## 13. Actuator, health, metrics, tracing

Map capabilities, not endpoint names:

- liveness/readiness/startup
- metrics names/tags
- tracing and baggage
- info/build metadata
- config/env exposure
- log-level control

Avoid recreating sensitive Actuator endpoints without equivalent authorization. Expect metric names/dimensions to change; provide dashboard/alert migration where necessary.

## 14. Testing migration

Map each Spring test to the contract:

| Spring test | Quarkus target |
|---|---|
| plain JUnit/Mockito | keep plain where framework is irrelevant |
| `@WebMvcTest`/WebFlux slice | HTTP/component test appropriate to Quarkus version |
| `@DataJpaTest` | focused DB-backed Quarkus test/component strategy |
| `@SpringBootTest` | `@QuarkusTest` for in-process integration |
| packaged/container test | `@QuarkusIntegrationTest` or deployment test |
| `@MockBean` | supported Quarkus mock injection/fake at boundary |

Do not convert every unit test into `@QuarkusTest`; preserve fast pure tests.

## 15. Native-readiness delta

Spring-era patterns that need scrutiny:

- classpath scanning
- dynamic proxies and reflection
- runtime-generated serializers
- SpEL or expression-driven class lookup
- Java serialization
- dynamic resource discovery
- build-time static initialization

Use Quarkus extension support and precise registration. Validate native separately.

## Staged migration sequence

1. **Baseline:** contract tests, build/profile inventory, dependency graph.
2. **Choose one vertical slice:** endpoint/message to persistence/client.
3. **Stabilize boundary DTOs and errors.**
4. **Move DI/config/lifecycle semantics.**
5. **Move persistence/transaction/execution model.**
6. **Move security and operations.**
7. **Remove now-unused compatibility extension only after usage search and build proof.**
8. **Run packaged/native gates required by production.**
9. **Repeat; keep old and new paths clearly separated during transition.**

## Migration traps

- mass replacing imports with no behavior tests
- using compatibility extension and Quarkus-native stack inconsistently in one path
- copying Spring package-by-layer plus generic base services unchanged
- assuming runtime component scan or conditions
- translating Reactor types operator-for-operator to Mutiny
- losing transaction rollback/propagation semantics
- changing security challenge/denial behavior
- removing compatibility dependencies before generated/reflected usage search
- making all tests full Quarkus tests
- declaring migration complete after JVM tests while native is the deployment target

## Completion checklist

- [ ] The intended compatibility versus native target is explicit.
- [ ] One vertical slice has contract coverage.
- [ ] DI discovery/scope/qualifier semantics are preserved.
- [ ] Config keys, phases, profiles, and defaults are mapped.
- [ ] HTTP/security/transaction behavior is tested.
- [ ] Blocking/reactive/virtual-thread choices are deliberate.
- [ ] Operations and dashboards have a migration plan.
- [ ] Compatibility extensions are removed only when truly unused.
- [ ] Packaged/native deployment mode is verified.
