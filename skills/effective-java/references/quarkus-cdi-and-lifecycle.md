# Quarkus CDI, ArC, and Lifecycle

Quarkus ArC implements CDI Lite plus selected features and Quarkus-specific behavior. Treat injection, scopes, proxies, interception, discovery, and bean removal as runtime semantics—not formatting choices.

## 1. Begin with the bean graph

For the relevant path, identify:

- bean-defining annotation and discovery source
- bean types and qualifiers
- normal scope versus pseudo-scope
- proxyability constraints
- constructor/field/producer injection points
- interceptors and decorators
- observers and lifecycle callbacks
- programmatic lookups
- mutable state and concurrent callers
- whether native reflection is involved

Do not replace field injection mechanically across the whole repository. Refactor one graph at a time and compile through augmentation.

## 2. Discovery is indexed and simplified

A class without a bean-defining annotation is generally not a discovered bean, subject to Quarkus extension and producer/observer rules. Dependencies may require an index or explicit inclusion.

When injection fails, investigate in this order:

1. type and generic type match
2. qualifier match
3. bean-defining annotation
4. package/dependency indexing
5. alternatives/default beans/priority
6. bean removal
7. proxyability and constructor rules
8. build profile/property conditions

Do not “fix” discovery by adding `@ApplicationScoped` indiscriminately. A third-party class may be better exposed through a focused producer or adapter.

## 3. Constructor injection

For required dependencies, constructor injection usually makes invariants and plain unit tests clearer. In Quarkus, a bean with one constructor often does not need `@Inject`, and package-private constructor access can avoid native reflection.

```java
@ApplicationScoped
class InvoiceService {
    private final InvoiceRepository repository;
    private final Clock clock;

    InvoiceService(InvoiceRepository repository, Clock clock) {
        this.repository = repository;
        this.clock = clock;
    }
}
```

Keep field injection when framework constraints, generated code, or repository conventions make it the smaller and safer choice. Do not add dummy no-arg constructors from generic CDI folklore without checking ArC rules.

## 4. Scope is a concurrency and lifecycle decision

### `@ApplicationScoped`

- normal scope; injected reference is usually a client proxy
- one contextual instance per application
- methods may be called concurrently
- mutable fields require a deliberate synchronization/confinement model
- initialization is lazy unless explicitly made eager

### `@Singleton`

- pseudo-scope; direct instance rather than normal-scope proxy semantics
- constructed when injected
- still shared and concurrently callable
- not a generic performance replacement for `@ApplicationScoped`

### `@RequestScoped`

- state is tied to an active request context
- asynchronous continuations or messaging paths may not have the context an agent assumes
- do not retain request-scoped instances beyond their valid lifecycle

### `@Dependent`

- lifecycle follows the injection owner/context rules
- repeated injection/programmatic lookup may create multiple instances
- cleanup matters for resources

Select scope by state ownership and lifecycle, not habit.

## 5. Proxyability

Normal-scoped beans require proxyable types under CDI/ArC rules. Risks include final classes/methods, inaccessible constructors, and private members, though Quarkus may transform some classes depending on configuration/version.

Do not rely on a transformation you have not verified. Compile the project and prefer designs naturally compatible with the container. Avoid making everything public merely to appease reflection; package-private access often suffices.

## 6. Qualifiers, `@Named`, and ambiguity

Use type-safe qualifier annotations for semantic variants. String-based naming is fragile.

Quarkus guidance specifically warns that a bean whose only qualifier is `@Named` also receives `@Default`, which can create surprising ambiguity. When a string identifier is genuinely required inside CDI, project/version support may favor `@Identifier`; reserve `@Named` for external name lookup such as template access.

Before introducing a qualifier:

- define the business distinction it represents
- apply it consistently to producer and injection point
- test unsatisfied/ambiguous resolution during augmentation
- avoid using bean names as a service-locator registry

## 7. Producers and disposers

Use a producer when construction is external, conditional, or needs adaptation—not as a dumping ground for ordinary constructors.

Check:

- produced type and qualifiers
- scope of the producer and produced bean
- null production rules
- resource ownership and disposer method
- configuration validation
- native reflection/dynamic loading
- test override strategy

A producer that opens a client, executor, or connection without a disposer or shutdown owner leaks lifecycle responsibility.

## 8. Interceptors and self-invocation

Interception depends on how a method is invoked and the framework’s supported behavior. Quarkus supports some non-standard self-interception behavior, but do not build portability-critical design around an assumption copied from Spring or another CDI implementation.

For `@Transactional`, security, metrics, retry, or custom interceptor bindings:

- verify the method is interceptable
- verify invocation passes through the expected contextual reference
- check private/final/static method limitations
- test the actual call path
- avoid moving an annotation to a helper method without proving interception still occurs

A unit test that calls `new Service()` cannot prove CDI interception.

## 9. Bean removal

Quarkus removes eligible unused beans during build. Programmatic lookups, reflection, external frameworks, or string-based references can be invisible to static analysis.

When a bean disappears:

1. confirm the lookup mechanism
2. prefer a statically visible injection path if possible
3. use precise unremovable configuration or `@Unremovable` only when justified
4. inspect removal diagnostics in dev/build logs
5. avoid disabling removal globally as the first response

Conversely, do not add `@Unremovable` preemptively to every bean; that hides dead code and increases the native/application footprint.

## 10. Startup and shutdown

Normal-scoped beans are lazy by default. Use startup observers or supported startup annotations only when eager work is a real requirement.

Startup work should be:

- bounded and observable
- explicit about failure policy
- independent of request-only context
- free of hidden network calls where readiness semantics would be better
- safe under dev-mode restarts
- paired with resource cleanup on shutdown

Avoid large `@PostConstruct` methods. They are hard to test, obscure readiness, and can turn configuration/network failures into opaque boot failures.

## 11. Mutable application beans

High-risk pattern:

```java
@ApplicationScoped
class TokenCache {
    private final HashMap<String, Token> tokens = new HashMap<>();
}
```

Questions before repair:

- Are reads/writes concurrent?
- Is eviction required?
- Is data tenant/request specific?
- Can the cache be external or bounded?
- What consistency is required?
- Does native or cluster deployment change assumptions?

Do not swap to `ConcurrentHashMap` and declare success. Concurrency safety includes compound operations, memory bounds, expiration, invalidation, and multi-instance behavior.

## 12. Programmatic lookup

`Instance<T>`, `Provider<T>`, or CDI programmatic lookup can be appropriate for optional/selected beans, but it weakens static visibility.

Reject patterns that use it as a global service locator. Check:

- ambiguity and unsatisfied behavior
- destruction of dependent instances
- bean-removal visibility
- startup/runtime selection phase
- native reachability

## 13. Testing CDI behavior

Choose the smallest faithful level:

- plain unit test for constructor-injected pure logic
- `@QuarkusComponentTest` for a focused CDI graph where supported by the project
- `@QuarkusTest` for augmentation, interceptors, configuration, observers, or HTTP integration
- packaged integration/native test for deployment-specific behavior

Test ambiguity, profile alternatives, startup failure, and interception where those are the changed contracts.

## High-signal CDI smells

| Signal | Risk | Preferred investigation |
|---|---|---|
| field injection in every class | hidden mandatory dependencies/test friction | one-bean constructor refactor; compile augmentation |
| `@Singleton` chosen “for speed” | misunderstood proxy/lifecycle/concurrency | scope semantics and state ownership |
| mutable fields in app scope | races/cross-request leakage | concurrency and tenant/request model |
| many `@Named` variants | ambiguity/string coupling | type-safe qualifier or supported identifier |
| giant producer class | service locator/lifecycle leaks | split by external resource or configuration concern |
| heavy `@PostConstruct` | opaque startup and readiness | startup observer/service plus explicit health |
| global bean-removal disable | hidden dead beans/larger artifact | identify exact invisible lookup |
| CDI annotations on private members everywhere | native reflection cost | package-private or constructor access where safe |
| interceptor annotation on private/helper method | interception may not occur | verify actual proxy/invocation path |
| manual `new` of intercepted bean | security/transaction/retry bypass | inject the contextual bean or separate pure logic |

## Completion checklist

- [ ] The bean is discoverable for a documented reason.
- [ ] Scope matches state ownership and concurrency.
- [ ] Required dependencies cannot be omitted silently.
- [ ] Qualifiers resolve unambiguously.
- [ ] Interceptor behavior is tested through CDI.
- [ ] Startup/shutdown resources have owners.
- [ ] Bean removal and programmatic lookup were considered.
- [ ] Native reflection was not expanded without evidence.
