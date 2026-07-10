# Quarkus Configuration, Security, and Observability

Configuration, authorization, and telemetry are operational contracts. Avoid fixes that work only in dev mode, expose secrets, or record misleading success.

## 1. Configuration inventory

For each touched setting, identify:

- canonical property name and owning extension/application component
- source: properties, YAML, environment, system property, secret store, test profile
- type and validation
- required/default/optional semantics
- build-time versus runtime phase
- profile-specific value
- secret classification
- whether reload/rebuild is required
- how the setting is tested in packaged mode

Do not invent a config key from naming conventions. Verify it against the exact project version and effective config.

## 2. Prefer grouped typed configuration

SmallRye Config Mapping can provide a typed, validated view of related settings.

```java
@ConfigMapping(prefix = "payments")
interface PaymentsConfig {
    URI baseUrl();
    Duration timeout();
    Optional<String> audience();
}
```

Use it when settings form a coherent component. Avoid creating one mapping interface per scalar property or a global mega-interface for the entire application.

Check:

- naming strategy and exact property keys
- defaults and optionality
- collection/map semantics and ordering
- Bean Validation support in the project
- interface method names after refactor
- test profile overrides
- static-initialization safety where an extension consumes the mapping

Do not proxy/mock config mappings casually; supply configuration values or a focused test implementation when supported.

## 3. Defaults are behavior

A fallback can hide a deployment error. Categorize defaults:

- safe product default
- development-only convenience
- backward-compatibility default
- unsafe missing-secret/endpoint fallback

Credentials, issuer URLs, encryption keys, tenant identifiers, and production endpoints should generally fail clearly when absent rather than silently use a placeholder.

## 4. Profiles and environment variables

Environment variable conversion can be ambiguous for quoted segments and dynamic map keys. Do not assume every dotted property maps cleanly to a guessed uppercase name.

Test the actual environment variable in packaged mode. Keep profile selection separate from build-tool profiles and build-time bean conditions.

## 5. Secrets

Never:

- commit real credentials or private keys
- log secrets, bearer tokens, cookies, auth headers, database URLs with credentials, or full signed URLs
- place secrets into build-time constants/native images unintentionally
- include secrets in exception messages, metrics labels, or trace attributes
- use a production secret as a test fixture

Use the deployment platform’s supported secret source and redact at log boundaries. Rotate exposed secrets rather than only deleting them from the latest commit.

## 6. Authentication versus authorization

Keep distinct:

- **authentication:** who/what is calling
- **authorization:** whether that identity may perform this operation on this resource
- **validation:** whether input is structurally acceptable

A valid JWT and a valid resource ID do not prove the caller owns the resource.

For endpoint changes, test:

- unauthenticated request
- authenticated but unauthorized request
- correct role/permission with wrong tenant/resource ownership
- permitted request
- expired/invalid token behavior
- challenge/status/error body contract

## 7. Quarkus security annotations and policies

Use the project’s established model: role annotations, permission checks, HTTP authorization policies, OIDC, or custom identity augmentation. Do not mix mechanisms without understanding precedence.

High-risk agent errors:

- moving security annotations to a method that is not intercepted
- protecting a UI route but not the underlying API
- relying on client-supplied tenant/user IDs
- changing path patterns so a deny/permit rule no longer matches
- adding an unprotected health/admin/debug endpoint
- swallowing auth exceptions into 200/404 inconsistently

Verify route matching and method-level checks with integration tests.

## 8. OIDC and token handling

Do not implement token validation manually when the Quarkus security stack already provides it. Confirm:

- issuer/audience/client configuration
- bearer versus authorization-code flow
- clock skew and expiration behavior
- tenant resolution
- token propagation policy
- refresh and logout semantics where applicable
- sensitive claim logging

Never authorize solely from an unverified decoded token or from client-controlled headers.

## 9. Outbound calls and token propagation

Propagate credentials only to intended origins. Review:

- REST client base URL and redirects
- per-client token propagation
- service versus end-user identity
- least privilege scopes/audience
- proxy/DNS behavior
- retries and idempotency
- header logging/redaction

Do not copy the inbound `Authorization` header to arbitrary URLs.

## 10. Logging

Logs should answer what happened without leaking data.

Prefer:

- stable event names
- request/job/message correlation ID
- tenant/resource identifiers only when privacy policy permits
- duration and outcome
- exception object at the owning layer
- structured fields supported by the configured backend

Avoid:

- string concatenation that eagerly renders expensive/sensitive values
- duplicate stack traces at every layer
- logging success before commit or asynchronous completion
- high-cardinality arbitrary labels/fields
- `System.out`, `printStackTrace`, or swallowed failures

## 11. Health

Liveness and readiness have different purposes:

- liveness asks whether the process should be restarted
- readiness asks whether it should receive traffic
- startup health can model slow initialization where supported

Do not make liveness depend on every downstream service; that can create restart storms. Readiness checks must be bounded and should not overload dependencies. Document whether a degraded dependency makes the service unready or merely limits a feature.

## 12. Metrics

Metrics need stable, low-cardinality dimensions.

Reject labels such as:

- user ID
- raw URL/query
- exception message
- order ID
- unbounded tenant ID unless the monitoring architecture explicitly supports it

Measure outcomes and latency at meaningful boundaries. Ensure retries do not count one logical operation as several successes.

## 13. OpenTelemetry and tracing

Check:

- automatic versus manual instrumentation
- span ownership and nesting
- async context propagation
- redaction of headers/body/SQL parameters
- sampler and exporter configuration
- errors recorded on the correct span
- transaction/message completion before success status

Do not create a span for every tiny method. Instrument external boundaries and important business transitions.

## 14. Configuration and native images

Build-time initialization can freeze values unexpectedly. Avoid static fields that capture:

- current time
- random IDs
- environment/config secrets
- default locale/time zone
- host/network state
- temporary paths

Verify whether initialization occurs at image build or runtime. Prefer explicit runtime initialization and injected configuration/clock where behavior must vary per deployment.

## High-signal smells

| Signal | Risk | Verification |
|---|---|---|
| scattered string `@ConfigProperty` keys | drift/weak grouping | property inventory and typed mapping candidate |
| default secret/URL | unsafe deployment | missing-config startup test |
| config override works only in dev | phase mismatch | packaged artifact run |
| user/tenant ID in metric tag | cardinality/privacy | telemetry backend sample |
| success log before reactive completion | false observability | failure-after-return test |
| auth only at resource path | method/alternate route bypass | route matrix |
| role check without ownership | horizontal privilege escalation | cross-user/tenant test |
| inbound auth forwarded to arbitrary host | credential leak | redirect/base URL tests |
| full exception text in response | information disclosure | error contract test |
| liveness calls database/remote API | restart cascade | outage behavior test |

## Completion checklist

- [ ] Every setting has a verified name, phase, type, and source.
- [ ] Missing/invalid production configuration fails appropriately.
- [ ] Secrets are absent from source, output, logs, metrics, and traces.
- [ ] Authentication and authorization are tested separately.
- [ ] Route/policy precedence is proven.
- [ ] Logs and telemetry reflect actual completion/rollback.
- [ ] Metric labels are bounded.
- [ ] Health semantics match orchestration behavior.
- [ ] Packaged/native initialization was considered.
