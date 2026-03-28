# Configuration and Secrets in Quarkus

Use this guide to clean up configuration sprawl and production-risky patterns.

## Prefer Config Mappings

Group related configuration in one place.

Prefer:

```kotlin
@ConfigMapping(prefix = "catalog")
interface CatalogConfig {
    fun baseUrl(): URI
    fun connectTimeout(): Duration
    fun readTimeout(): Duration
    fun retries(): Int
}
```

Over:

```kotlin
class CatalogClient {
    @ConfigProperty(name = "catalog.base-url")
    lateinit var baseUrl: String

    @ConfigProperty(name = "catalog.connect-timeout")
    var connectTimeout: Long = 0
}
```

Why:

- less scattered stringly-typed config
- easier review of one namespace
- easier testing and evolution

Use one-off `@ConfigProperty` only for genuinely isolated values.

## Namespace by Capability

Group config by real concern:

- `catalog.*`
- `payments.*`
- `security.*`
- `feature-flags.*`

Avoid random flat naming with no ownership.

## Profiles

Make environment intent obvious:

- dev
- test
- prod

Keep profile-specific behavior visible and documented.

Smells:

- production assumptions hidden in dev defaults
- test-only config accidentally relied on by the app
- logic that branches on environment in code instead of config

## Secrets

Rules:

- do not hardcode secrets
- do not log secrets
- do not expose secrets via debug endpoints or exception messages
- do not spread secret access across unrelated classes

Centralize secret consumption at the integration boundary that actually needs it.

## Dev Services Are Not Production Architecture

Dev Services are excellent for development and tests.

Smell:

- the team never wrote real production datasource or broker config because dev mode “just works”

Cleanup task:

- separate dev/test convenience from production readiness

## Build-Time vs Runtime Thinking

Quarkus distinguishes some build-time choices from runtime-configurable ones.

Be careful when cleanup touches:

- extension enablement
- native behavior
- provider selection
- protocols
- resource inclusion

Do not assume every property is freely changeable at runtime.

## Config Review Questions

- Are related settings grouped?
- Are config names feature-owned and readable?
- Are timeouts, retries, and URLs centralized?
- Are secrets protected?
- Are dev assumptions clearly separated from prod?
