# Quarkus CDI and Typed Configuration

## Constructor injection for required dependencies

```java
@ApplicationScoped
class PaymentGateway {
    private final PaymentsConfig config;
    private final Clock clock;

    PaymentGateway(PaymentsConfig config, Clock clock) {
        this.config = config;
        this.clock = clock;
    }
}
```

A single package-private constructor can be injected by Quarkus without field injection boilerplate in supported generations. Compile through augmentation; do not assume this rule for another CDI runtime.

## Type-safe variants

```java
@Qualifier
@Retention(RUNTIME)
@Target({ TYPE, FIELD, PARAMETER, METHOD })
@interface PrimaryGateway {}

@ApplicationScoped
@PrimaryGateway
class AcquirerGateway implements Gateway {}

@ApplicationScoped
class Checkout {
    private final Gateway gateway;

    Checkout(@PrimaryGateway Gateway gateway) {
        this.gateway = gateway;
    }
}
```

Prefer a type-safe qualifier to routine `@Named("primary")` use. A string identifier may still be appropriate for external lookup/template integration.

## Config mapping

```java
@ConfigMapping(prefix = "payments")
interface PaymentsConfig {
    URI baseUrl();
    Duration connectTimeout();
    Duration requestTimeout();
    Optional<String> audience();
}
```

Example configuration:

```properties
payments.base-url=https://payments.example
payments.connect-timeout=2s
payments.request-timeout=5s
```

Decisions to test:

- missing required property fails startup
- default values are safe and intentional
- exact environment variable mapping works in packaged mode
- secret fields are not logged
- property phase permits the desired runtime override

## Shared state trap

```java
@ApplicationScoped
class RequestCache {
    final HashMap<String, Object> values = new HashMap<>();
}
```

Changing this to `ConcurrentHashMap` alone does not define tenant scope, bounds, expiry, compound atomicity, cluster behavior, or invalidation. First decide whether application-scoped in-memory state is correct at all.
