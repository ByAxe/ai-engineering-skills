# Quarkus Messaging, Scheduling, and Fault Tolerance

Messages and scheduled jobs are distributed-system entry points. Threading, acknowledgment, transaction, retry, ordering, and idempotency are part of their public contract.

## 1. Trace a message end to end

Record:

- incoming channel/connector and payload schema
- deserialization and validation
- execution thread/context
- acknowledgment strategy and timing
- transaction boundary
- state change and emitted messages
- retry/redelivery/dead-letter behavior
- ordering and partition/key assumptions
- idempotency/deduplication
- telemetry and correlation
- shutdown/drain behavior

Do not treat a successful method return as proof of durable acknowledgment without checking the connector and acknowledgment strategy.

## 2. Blocking and reactive consumers

Messaging methods can run on event loops, worker pools, ordered worker contexts, or virtual threads depending on signatures/annotations/version.

Before calling ORM/JDBC, filesystem, or blocking clients:

- identify the current execution context
- use the framework-supported blocking dispatch annotation/configuration where appropriate
- preserve message ordering requirements
- bound concurrency to downstream capacity
- test failure and cancellation

Changing to unordered or higher concurrency can violate per-key ordering even if throughput improves.

## 3. Acknowledgment

Understand whether acknowledgment occurs:

- before processing
- after successful processing
- manually
- after a returned reactive stage completes
- through connector-specific transactional semantics

Early acknowledgment can lose work on failure. Late acknowledgment can redeliver after a side effect. Pair acknowledgment policy with idempotency and transaction design.

## 4. Delivery semantics

“Exactly once” is not a generic method annotation. End-to-end behavior depends on broker, connector, transactions, database, retries, and external side effects.

Design for at-least-once unless stronger semantics are demonstrably configured:

- stable message/event ID
- database uniqueness or deduplication record
- idempotent state transition
- idempotency key for external calls
- safe replay and poison-message path

Do not use only an in-memory set for deduplication in a multi-instance or restartable service.

## 5. Database and message atomicity

Writing the database and publishing a message are two separate systems. Common safe patterns include:

- transactional outbox
- connector/broker transaction where supported end to end
- idempotent consumer with reconciliation
- saga/compensation

Do not claim atomicity because both calls occur inside a Java method annotated `@Transactional`.

## 6. Failure and dead-letter handling

Classify failures:

- transient dependency failure
- permanent validation/schema failure
- authorization/policy failure
- poison message
- code defect
- capacity/timeout failure

Define:

- retry count/backoff/jitter
- maximum processing time
- dead-letter destination and payload redaction
- alerting and replay procedure
- whether retry preserves order
- what is logged once versus per attempt

A broad retry on every exception can amplify outages and repeatedly execute permanent failures.

## 7. Payload contracts

Protect:

- schema version and compatibility
- required/optional fields
- unknown-field policy
- decimal/time-zone representation
- enum evolution
- message key/partitioning
- headers and correlation IDs
- maximum size

Do not publish JPA entities directly. Use stable event contracts separate from current persistence shape.

## 8. Scheduled jobs

For every job, decide:

- may executions overlap?
- may multiple application instances run it?
- what happens after a missed trigger?
- what time zone applies?
- is work idempotent?
- how is ownership elected/locked?
- what timeout/cancellation applies?
- how is failure surfaced?

An in-process scheduler does not automatically provide cluster-singleton execution. Use a database lock, leader election, external scheduler, or supported clustered mechanism when one execution is required.

## 9. Time and calendars

Avoid system-default zone in schedules. Inject `Clock` into calculation logic and test:

- daylight-saving gaps/overlaps
- month/year boundary
- leap day where relevant
- delayed startup/misfire
- duplicate trigger/restart
- UTC versus business zone

Keep trigger configuration and business-calendar policy separate.

## 10. Fault tolerance

Timeout, retry, circuit breaker, fallback, and bulkhead annotations/interceptors change semantics. Apply them at a stable external boundary, not randomly on every method.

### Retry

- only when operation is safe/idempotent or protected by idempotency
- narrow exception set
- bounded attempts and total deadline
- jitter to avoid synchronized retry storms
- metrics distinguish attempts from logical operations

### Timeout

- must propagate to the actual client/operation when possible
- interruption/cancellation support varies
- a wrapper timeout that leaves work running can consume resources after callers give up

### Circuit breaker

- choose failure classification and window deliberately
- fallback must not fabricate successful business outcomes
- avoid one global circuit for unrelated tenants/endpoints unless intended

### Bulkhead

- size from downstream capacity and latency, not CPU count alone
- define queue/rejection behavior
- virtual threads do not remove the need to bound scarce resources

## 11. Context and security

Message/scheduled execution may not have an HTTP request/security context. Do not assume an injected request identity survives.

Carry only explicit, authenticated/verified metadata needed for the operation. Avoid trusting user/tenant headers from a broker without producer and channel trust controls.

## 12. Tests

Test more than invocation:

- ack after success
- nack/redelivery on failure
- duplicate delivery
- poison message/dead letter
- ordering under concurrency
- transaction rollback plus retry
- outbox publication/recovery
- job overlap and multi-instance lock
- timeout and retry budget
- shutdown while work is active

Use connector test companions, in-memory connectors, Dev Services, or real broker containers according to the contract. An in-memory test cannot prove broker-specific ordering/transactions.

## High-signal smells

| Signal | Risk | Evidence |
|---|---|---|
| message acknowledged before DB commit | lost processing | failure between ack and commit |
| side effect then late ack without idempotency | duplicate side effect | redelivery test |
| retry catches all failures | poison-loop/outage amplification | permanent-failure test |
| `@Transactional` assumed to cover broker | false atomicity | broker/DB failure matrix |
| unordered concurrency introduced | per-key order break | partition/key test |
| scheduler runs on every replica | duplicate job | multi-instance test |
| system zone cron/business time | DST/host variance | fixed-zone boundary tests |
| fallback returns success/default | hidden dependency failure | response/event semantics |
| virtual threads with unbounded DB calls | pool exhaustion | load test against connection limit |
| in-memory dedupe | restart/cluster duplicates | restart/multi-instance test |

## Completion checklist

- [ ] Execution context and blocking calls are compatible.
- [ ] Acknowledgment timing is explicit.
- [ ] Redelivery is safe or deduplicated durably.
- [ ] DB/message atomicity is not overstated.
- [ ] Retry/timeout/circuit/bulkhead policies are bounded.
- [ ] Ordering and partition assumptions are protected.
- [ ] Scheduled overlap and cluster ownership are defined.
- [ ] Payload schema evolution is tested.
- [ ] Telemetry counts logical outcomes accurately.
