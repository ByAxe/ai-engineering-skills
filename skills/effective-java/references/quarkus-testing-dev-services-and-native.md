# Quarkus Testing, Dev Services, and Native Readiness

Match the test environment to the contract. Plain JVM unit tests, augmented Quarkus tests, packaged integration tests, and native executable tests prove different things.

## 1. Testing ladder

### Plain unit test

Use for:

- domain calculations and policies
- parsers/mappers without framework behavior
- value objects
- orchestration with explicit ports/fakes
- time/locale/numeric edge cases

Benefits: fast, deterministic, no container startup. It cannot prove CDI, interception, ORM mapping, config resolution, Quarkus REST dispatch, or native reachability.

### Component/CDI slice test

Where the project supports `@QuarkusComponentTest`, use it for:

- focused bean graph
- injection and qualifiers
- interceptors/configuration in a bounded component context
- replacing external dependencies without booting the whole app

Do not assume the annotation exists in older Quarkus versions. Confirm the test extension and API.

### `@QuarkusTest`

Use for:

- augmentation and application boot
- CDI graph and interceptors
- REST endpoints
- security and configuration
- Hibernate/Panache integration
- messaging/scheduler integration where the harness supports it

It runs in the test JVM and does not by itself prove packaged/native behavior.

### `@QuarkusIntegrationTest`

Use for the packaged application boundary:

- packaged JVM runner/container/native executable
- actual HTTP interface
- startup/configuration mode
- classpath/resource packaging

It generally cannot inject application beans like an in-process `@QuarkusTest`; test from external boundaries.

### Native integration test

Use when production ships native or the changed code touches native-sensitive areas:

- reflection/dynamic proxies
- resource inclusion
- serialization
- class initialization
- service loading
- security providers/URL protocols
- JNI/platform behavior

Do not run a native build for every trivial pure-logic edit if CI policy does not require it. Do run it before claiming native compatibility for a relevant change.

## 2. `@TestTransaction`

Use rollback-friendly test transactions where supported and appropriate. Understand that:

- code under test may begin nested/new transactions differently
- external systems/messages are not rolled back automatically
- reactive persistence uses different test transaction helpers
- generated IDs/flush behavior may require explicit flush
- verifying committed behavior requires a separate transaction or packaged path

A rollback test cannot prove post-commit listeners, outbox publication, or data visible to another connection.

## 3. Mocks

Quarkus provides mechanisms such as `@InjectMock` and `QuarkusMock` for normal-scoped beans in supported versions.

Rules:

- mock external boundaries, not the subject under test
- match qualifiers
- confirm bean scope is mockable
- avoid globally leaking a mock between tests
- assert business outcomes, not only interactions
- do not mock persistence in a test intended to prove ORM mapping or transaction behavior
- do not mock security identity in every test while omitting real policy tests

Prefer a small fake for complex stateful behavior when it makes the contract clearer.

## 4. Test profiles and configuration

Use test profiles for coherent alternate configuration/beans, not as a hidden global switchboard.

Check:

- profile selection and restart cost
- build-time versus runtime setting
- tags/grouping
- alternative bean conditions
- config overrides are isolated
- production defaults are still tested somewhere

Do not make tests pass by globally disabling security, validation, migrations, or bean removal unless the test explicitly excludes those contracts.

## 5. Test resources

A test resource that starts a service/container must have:

- deterministic startup and readiness
- bounded ports or collision-safe allocation
- cleanup on failure
- isolated state
- explicit environment variables/config returned to Quarkus
- reasonable logs and timeouts
- parallel-test behavior

Avoid downloading/installing tools implicitly in ordinary unit tests. Respect offline/CI constraints.

## 6. Dev Services

Dev Services can provision databases, brokers, identity providers, and other dependencies in dev/test. They improve fidelity but can hide production assumptions.

Verify:

- service only starts when intended
- production has explicit connection/configuration
- image/version is stable enough for tests
- reused services do not leak state
- CI has container support
- fixed/random ports are handled
- test credentials never become production defaults
- dialect/broker version resembles production when behavior depends on it

A test passing against an embedded/in-memory database may not prove PostgreSQL/MySQL locking, SQL, collation, or migration behavior.

## 7. REST tests

Protect:

- status, headers, and body schema
- authn and authz separately
- validation and malformed input
- error mapping
- content type/charset
- request size and edge cases
- transaction completion before response semantics
- execution model where blocking risk matters

Avoid fragile assertions on full dynamic payloads when only stable fields matter. Use exact golden payloads when the wire format itself is the contract.

## 8. Persistence tests

Test:

- schema/migration startup
- constraints and race-sensitive invariants
- rollback and commit
- lazy access after transaction
- query count/N+1 when performance matters
- optimistic/pessimistic locking
- actual production dialect features
- reactive completion/rollback without blocking waits

Clean state deterministically. Transaction rollback alone may not clean sequences, external resources, or work committed in another transaction.

## 9. Messaging and scheduled tests

Include duplicate delivery, ack/nack, retry, dead letter, ordering, overlap, and shutdown. In-memory connectors are fast but do not prove broker-specific transactions, partitioning, or redelivery; add a container/integration test when those are contractual.

## 10. Native closed-world checklist

### Reflection

Identify the exact framework/library call performing reflective construction or member access. Prefer Quarkus extension integration, generated serializers, or precise registration. Broad package registration increases image size and can mask unsupported dynamic behavior.

### Resources

Classpath resources may need explicit inclusion. Test resource loading from the packaged/native artifact, including case sensitivity and relative paths.

### Static initialization

Inspect static fields/initializers for:

- current time/randomness
- environment variables/config
- hostname/network access
- temp directories/files
- locale/time zone
- security/provider initialization
- native libraries

Values captured while building the image may be wrong or sensitive at runtime.

### Dynamic class loading and proxies

Closed-world compilation cannot discover arbitrary runtime class names. Replace dynamic scanning with known registrations/configuration or prove supported proxy metadata.

### Serialization

Confirm JSON/message serializers can construct types and access members. Records, polymorphic hierarchies, private members, and generic types may need framework-specific metadata.

### Charset, locale, URL protocols, crypto

A native image may include a narrower set than the full JVM. Test only the features the application actually needs and configure providers/protocols precisely.

## 11. Native debugging discipline

When native build/run fails:

1. reproduce with the smallest relevant command and preserve logs
2. classify build-time analysis versus runtime failure
3. identify the exact class/resource/reflection edge
4. inspect existing Quarkus extension support
5. add the narrowest metadata/configuration
6. rerun the relevant native test
7. document residual platform constraints

Do not immediately add global `--initialize-at-run-time` or broad reflection patterns.

## 12. Flakiness

Common causes:

- shared Dev Service state
- fixed ports
- static mutable application/test state
- asynchronous work not awaited through a deterministic signal
- scheduler running during unrelated tests
- order-dependent profiles/config
- clock/system zone
- container readiness races
- transaction committed after assertion

Do not increase sleeps. Add observable readiness/completion and isolate ownership.

## Suggested gate matrix

| Changed area | Fast gate | Framework gate | Deployment gate |
|---|---|---|---|
| pure domain logic | unit test | none if truly pure | normal repository build |
| CDI qualifier/interceptor | component test | `@QuarkusTest` | packaged only if deployment-sensitive |
| REST contract | mapper/unit tests | HTTP `@QuarkusTest` | integration for packaging/security proxy behavior |
| ORM/query | unit policy tests | DB-backed `@QuarkusTest` | production-dialect/container as needed |
| reactive execution | unit operator test | Quarkus integration path | load/thread evidence if high risk |
| config phase | config test | packaged-mode test | native if native/build-time sensitive |
| reflection/resource | JVM test | packaged test | native integration test |
| messaging semantics | pure handler test | connector/Dev Service | real broker when semantics differ |

## Completion checklist

- [ ] Every test layer is used for a contract it can actually prove.
- [ ] Test discovery and execution were confirmed.
- [ ] Mocks do not erase the boundary under review.
- [ ] Dev Services assumptions are not production defaults.
- [ ] Asynchronous tests use deterministic completion signals.
- [ ] Packaged mode was tested for packaging/config changes.
- [ ] Native mode was tested for native-sensitive production behavior.
- [ ] The final report names gates that were not run.
