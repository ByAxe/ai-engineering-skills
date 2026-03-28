# CDI and Dependency Injection in Quarkus

Use this guide to clean up bean wiring, scopes, and composition.

## Prefer Constructor Injection

Default style:

```kotlin
@ApplicationScoped
class CreateOrderService(
    private val repository: OrderRepository,
    private val paymentClient: PaymentClient,
) {
    fun create(command: CreateOrderCommand): Order = TODO()
}
```

Why:

- dependencies are explicit
- invariants are easier to maintain
- tests are simpler
- Kotlin works more naturally with constructor injection than field injection

Avoid field injection as the default style.

## One Constructor Usually Means No `@Inject`

In Quarkus, when a bean has a single constructor, that constructor can usually be used directly without annotating it with `@Inject`. Favor that style for Kotlin classes.

## Prefer `@ApplicationScoped` by Default

`@ApplicationScoped` is a good default for stateless services.

Use `@Singleton` only when you truly want singleton semantics and understand the lifecycle trade-offs.

Be careful with mutable state in either scope.

## Qualifiers Over Magic Selection

If multiple beans implement the same contract, use qualifiers explicitly.

Example:

```kotlin
@Qualifier
@Retention(AnnotationRetention.RUNTIME)
@Target(
    AnnotationTarget.FIELD,
    AnnotationTarget.FUNCTION,
    AnnotationTarget.VALUE_PARAMETER,
    AnnotationTarget.CLASS,
)
annotation class PrimaryCatalog
```

Then:

```kotlin
@ApplicationScoped
@PrimaryCatalog
class HttpCatalogClient : CatalogClient
```

Avoid ad-hoc bean lookups, string switches, or “service locator” helpers.

## Producer Methods Are for Special Cases

Use producers when:

- integrating a third-party object you do not control
- configuration of the object is non-trivial
- lifecycle must be adapted

Do not wrap normal application classes in producer methods just to be clever.

## Keep Lifecycle Callbacks Boring

`@PostConstruct` and `@PreDestroy` are allowed, but keep them small.

Good:

- local initialization
- cache warm-up when explicitly justified
- resource cleanup

Bad:

- cross-service orchestration
- business calls with side effects
- hidden startup behavior that changes correctness

## Avoid Field Access on Normal-Scoped Beans

Quarkus uses client proxies for normal-scoped beans such as `@ApplicationScoped`. Treat injected beans as services to call, not as state bags to read and mutate.

Smell:

```kotlin
@Inject
lateinit var service: MyService

fun doWork() {
    service.counter++
}
```

Prefer encapsulated behavior on the bean itself.

## Optional and Multiple Beans

Reach for `Instance<T>` only when optional or multiple bean resolution is genuinely part of the design.

Smell:

- using `Instance<T>` everywhere because the graph is unclear
- runtime lookup instead of build-time safe resolution

## CDI Cleanup Checklist

- Constructor injection by default?
- Scopes appropriate and explicit?
- Qualifiers used instead of conditionals?
- No giant mutable singletons?
- No producer-method abuse?
- Lifecycle callbacks small and unsurprising?
