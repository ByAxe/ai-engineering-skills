# Quarkus REST, REST Clients, and Execution Model

A Quarkus REST signature is also an execution-model decision. Review HTTP contract, thread selection, blocking behavior, transaction scope, cancellation, serialization, and client lifecycle together.

## 1. Trace the complete path

For each touched endpoint or filter, record:

- resource method and annotations
- request/response DTOs and validation
- declared return type
- event-loop, worker, or virtual-thread execution
- blocking calls: ORM/JDBC, filesystem, legacy clients, locks, DNS, crypto, templates
- transaction and security interceptors
- exception mapping
- downstream REST client timeouts/retries
- serialization and native reflection
- tests that exercise the real path

Do not infer safety from an isolated `Uni`/`CompletionStage` return type. Trace every call below it.

## 2. Blocking versus non-blocking

Quarkus REST chooses an execution model from method signatures and annotations, with rules that vary by stack/version. Commonly, synchronous methods run on worker threads and reactive return types run on event-loop threads; `@Blocking`, `@NonBlocking`, transaction annotations, and virtual-thread annotations can override or influence dispatch.

Required discipline:

1. inspect the exact Quarkus REST guide for the project version
2. identify the actual blocking operations
3. make thread intent explicit when inference is unsafe or surprising
4. add a test or runtime check for the important path
5. never “fix” event-loop blocking by wrapping a call in a reactive type without moving the work

### Blocking operations often missed by agents

- Hibernate ORM/Panache ORM and JDBC
- synchronous REST clients
- file and classpath resource I/O
- `Thread.sleep`, locks, and blocking queues
- password hashing or CPU-heavy crypto
- template/PDF/image generation
- process execution
- library calls with hidden network I/O
- lazy entity traversal that triggers SQL during serialization

## 3. Resource boundaries

Keep resource methods responsible for transport concerns:

- parse and validate HTTP input
- invoke a focused use case/service
- choose status, headers, and representation
- translate domain outcomes through a consistent mapping

Avoid resources that perform validation, pricing, persistence, retries, mapping, event publication, and telemetry in one method. Also avoid a ceremonial service layer that only forwards every argument; extract where it creates a transaction, policy, or test boundary.

## 4. Typed responses and `Response`

Typed return values improve schema and serialization clarity. `Response` is appropriate when status/headers/entity vary materially.

Do not return raw `Response` everywhere as a reflex. Conversely, do not force a single typed body when the endpoint contract genuinely has multiple statuses or no body.

Verify:

- status for success and every failure
- `Location`, cache, retry, content-type, and pagination headers
- empty-body versus `null` semantics
- validation error shape
- exception mapper precedence
- serialization of generic collections and polymorphic types

## 5. DTOs, entities, and serialization

Do not expose JPA/Panache entities directly unless the coupling is explicitly accepted. Risks:

- lazy loading during serialization
- accidental fields/relationships in the wire contract
- cycles and large graphs
- persistence annotations defining public API shape
- mass-assignment on request binding
- optimistic-lock/internal identifiers leaking
- transaction lifetime coupled to serialization

Use request/response models that express the HTTP contract. Mapping can be manual and small; do not add a mapper framework merely to copy three fields.

Records can be useful DTOs when the serialization extension supports them and generated equality/component exposure matches the contract.

## 6. Validation

Use Bean Validation and explicit checks as complementary tools:

- structural constraints at the transport boundary
- domain invariants in domain/application code
- authorization after identity and resource resolution
- database constraints for persisted invariants

Do not confuse syntactic validation with authorization. Avoid returning internal exception messages as validation detail. Test nested validation, collection elements, absent body, malformed JSON, unknown fields according to configured policy, and boundary sizes.

## 7. Exception mapping

Centralize stable translations while preserving domain context.

Check:

- most-specific mapper wins as intended
- causes are retained in logs but not leaked to clients
- validation, not-found, conflict, authn, authz, timeout, and dependency failure remain distinct
- reactive failures are mapped rather than swallowed
- transaction rollback behavior matches the HTTP status
- logs do not duplicate one failure at every layer

Do not catch `Exception` in every resource and return 500 manually; that erases framework behavior and makes observability inconsistent.

## 8. Filters and interceptors

Pre-matching/request filters can run in a context different from the resource method. A blocking call in authentication, logging, body inspection, or tenant-resolution filters can block the event loop even when the endpoint itself is dispatched safely.

Review filters for:

- blocking I/O
- body buffering and size limits
- secret/token logging
- response mutation order
- duplicate telemetry
- context propagation
- request-context availability
- exception and abort semantics

## 9. Virtual-thread endpoints

Where supported, `@RunOnVirtualThread` can let I/O-bound blocking code retain a synchronous style. It is not permission to ignore resource limits.

Check:

- project JDK and Quarkus support
- operation is mostly blocking I/O, not CPU saturation
- downstream connection pools remain bounded
- no virtual-thread pooling
- thread-local memory and context behavior
- cancellation/timeout path
- pinning diagnostics for the actual JDK; remedies differ after JDK 24
- load test under realistic downstream limits

A million virtual threads cannot create a million database connections. Concurrency must remain bounded at scarce resources.

## 10. Reactive endpoints

For `Uni`, `Multi`, `CompletionStage`, or publisher-based paths:

- do not call blocking ORM/JDBC or synchronous client code on the event loop
- preserve cancellation and timeout signals
- avoid nested subscriptions and manual blocking (`await`, `join`, `get`)
- use framework-supported context propagation
- keep failure recovery narrow and observable
- do not hide errors with broad `onFailure().recoverWithNull()`
- ensure transaction lifetime follows asynchronous completion when required

Reactive is an end-to-end execution model, not a return-type decoration.

## 11. REST Client design

For Quarkus REST Client interfaces and injected clients:

- verify the correct extension/generation and annotation package
- define base URL/config key according to project conventions
- configure connect/read/request timeouts deliberately
- map non-2xx responses into stable application outcomes
- handle retry only for safe/idempotent operations or with an idempotency key
- avoid constructing a new client per request
- redact authorization headers and sensitive bodies
- account for redirects, DNS, proxy, TLS, and SSRF controls
- close manually created clients/resources

Do not add a fallback that turns dependency failure into fabricated success.

## 12. Context propagation

Request identity, security context, trace context, MDC, locale, and tenant context can be lost across executor/reactive boundaries.

Never solve this by copying arbitrary `ThreadLocal` values globally. Use the stack’s supported context propagation and test the value at the asynchronous consumer, including cleanup to prevent cross-request leakage.

## 13. HTTP compatibility

A refactor can break clients without changing Java signatures. Protect:

- path and HTTP method
- status code
- header names/values
- media type and charset
- JSON names, types, null/absent policy, order only if contractual
- date/time/decimal representation
- pagination and error envelope
- authentication challenge behavior
- OpenAPI schema when published

Use contract tests or golden payloads for sensitive endpoints.

## High-signal REST smells

| Signal | Risk | Evidence to collect |
|---|---|---|
| reactive signature calls ORM/JDBC | event-loop blocking | thread dump, call graph, extension type |
| endpoint calls `.await()`, `.join()`, `.get()` | deadlock/blocking/timeout loss | execution thread and timeout behavior |
| entity returned directly | lazy/cycle/API coupling | serialization trace and schema |
| raw `Response` everywhere | inconsistent contract | status/header matrix |
| resource catches all exceptions | lost mapping/rollback | mapper and log behavior |
| no client timeout | resource exhaustion | config and failure test |
| retry on POST/payment | duplicate side effect | idempotency contract |
| filter reads full body | memory/DoS/event-loop risk | body limit and thread model |
| `@RunOnVirtualThread` on CPU-heavy route | carrier saturation | profile and throughput measurement |
| synchronous client per request | leaks/latency | allocation/lifecycle and connection reuse |

## Verification matrix

| Change | Minimum useful proof |
|---|---|
| DTO or serialization | request/response contract test |
| exception mapper | status/body test for each mapped outcome |
| execution annotation | integration test plus runtime/thread evidence where material |
| REST client timeout/retry | deterministic fake dependency or test resource |
| virtual threads | JDK-specific diagnostics and constrained load test |
| reactive transaction | test that observes commit/rollback after async completion |
| security filter | authn/authz tests including failure and body/secret handling |
