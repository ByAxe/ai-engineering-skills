# Persistence, JPA, and Transactions

Persistence semantics span the object model, database constraints, transaction manager, isolation, serialization boundary, and migration history.

## Entity modeling

Entities are lifecycle-managed identity objects, not ordinary records by default. Review:

- identifier generation and unsaved state
- constructor/proxy requirements
- mutability and encapsulation
- `equals`/`hashCode` across transient, managed, detached, and proxied states
- lazy associations
- cascade and orphan lifecycle
- optimistic version field
- collection ownership/order

Avoid generated `equals`/`hashCode` over all mutable associations. Avoid including lazy graphs in `toString`.

## Equality strategy

There is no one universal entity equality recipe. Choose based on stable natural key, assigned ID, or generated ID and test it across lifecycle states. Consider proxy classes. Never mutate fields used as hash keys while the entity is in a set/map.

## Transaction boundaries

Place the boundary around one coherent business operation. Check:

- which method is actually intercepted
- nested propagation semantics
- rollback rules for checked/unchecked exceptions
- flush timing
- lazy-loading/serialization after return
- events/messages emitted before commit
- remote calls inside a database transaction
- lock duration

Moving `@Transactional` is a behavior change, even if tests still compile.

## Flush and database truth

ORM changes may be deferred until query/flush/commit. A method can appear successful before a constraint or optimistic lock fails. Force flush only when immediate feedback is required; it can reduce batching/performance and does not replace commit.

Use database constraints for uniqueness/referential invariants. “Check then insert” is race-prone without a constraint or appropriate lock/isolation.

## Fetching and N+1

Do not solve lazy failures by marking every association eager. Design query fetch shape for the use case:

- join fetch/entity graph/projection
- batch fetching
- explicit pagination strategy
- DTO mapping inside the transaction when needed

Measure query count and payload. Multiple collection joins can multiply rows or break pagination.

## Queries

- parameterize values
- allowlist dynamic identifiers/sort fields
- request stable ordering for pagination
- avoid loading all rows to filter in Java
- consider database null/collation/time-zone semantics
- inspect query plans for performance claims

## Locking and concurrency

- optimistic locking detects conflicting updates; define retry/user conflict behavior
- pessimistic locks require a live transaction and can deadlock/block
- isolation level affects phantom/non-repeatable reads
- lock ordering and timeout matter

A retry after optimistic conflict must be safe and must re-read/reapply intent rather than blindly repeat stale mutations.

## DTO and serialization boundary

Do not expose entities over HTTP/events by convenience. Risks include lazy access, recursive graphs, over-posting, internal field leakage, unstable schema, and transaction-dependent output. Use focused request/response/event models where contracts differ.

Records are often good projections/DTOs but usually not entities.

## Migrations

- treat applied migrations as immutable; add a new migration
- make forward/backward compatibility explicit for rolling deployment
- expand/contract for breaking schema changes
- backfill in bounded/restartable batches
- preserve defaults/nullability behavior
- test migration from representative prior schema/data
- coordinate code and database deployment order

Schema auto-generation is not a production migration strategy unless explicitly accepted for that environment.

## Idempotency and messaging

Database transactions do not automatically make external messages/calls atomic. Consider outbox/inbox, idempotency keys, deduplication, and commit ordering for cross-system workflows.

## Testing

Use a real database family when dialect, constraints, locking, SQL, or migration behavior matters. Verify transaction rollback/commit semantics rather than assuming a test annotation. Avoid shared state and unspecified ordering.

## Reactive persistence

Reactive sessions/transactions are tied to reactive context and completion. Do not move entities across arbitrary threads or mix blocking ORM and reactive APIs casually. Use framework-specific transaction operators/annotations consistently.

## Review checklist

- Is entity identity/equality stable across lifecycle?
- Are invariants enforced by the database where races matter?
- Is transaction interception and rollback behavior real?
- Can serialization touch lazy state after transaction close?
- Are query count, ordering, and pagination deliberate?
- Are retries idempotent?
- Is migration deployable with old/new code overlap?
