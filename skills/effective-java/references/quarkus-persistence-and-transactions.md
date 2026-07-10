# Quarkus Persistence and Transactions

Choose one persistence model per path and preserve its transaction semantics. Hibernate ORM with Panache and Hibernate Reactive with Panache look similar at the API surface but have different execution, session, and transaction models.

## 1. Identify the stack

Before changing persistence code, confirm:

- Hibernate ORM versus Hibernate Reactive
- Panache active record, Panache repository, or plain Hibernate/JPA
- JDBC datasource versus reactive SQL client
- transaction annotation/model in use
- database and dialect
- migration tool and deployed schema history
- entity enhancement, generated IDs, optimistic locking, and auditing
- blocking, event-loop, worker, or virtual-thread entry point
- test database and production topology

Never infer “reactive” from the presence of `Uni` alone. Check extensions and datasource configuration.

## 2. ORM and reactive persistence do not mix casually

### Hibernate ORM / JDBC

- blocking by nature
- use worker or virtual threads, not an event loop
- transaction demarcation commonly uses `@Transactional`
- streams and lazy associations require an open persistence context/transaction

### Hibernate Reactive

- asynchronous and event-loop oriented
- use reactive session/transaction APIs supported by the project
- Panache guidance commonly uses `@WithTransaction`/reactive transaction helpers rather than Jakarta `@Transactional`
- do not block waiting for `Uni` completion

A reactive HTTP method that calls blocking Panache ORM is still blocking. A blocking endpoint returning a `Uni` from Hibernate Reactive can also violate the intended model.

## 3. Transaction boundaries are business boundaries

Place the transaction around a coherent state transition, not around every repository method.

A transaction decision includes:

- when data is read and locked
- when constraints are checked
- when changes flush
- what events/messages are emitted and when
- how failures mark rollback
- what external calls occur inside the lock/connection lifetime
- what data is available for serialization afterward
- retry and idempotency behavior

Avoid transactions in REST resources merely because it is convenient. A focused application service often makes the boundary more explicit and testable. Avoid pass-through services that add no boundary or policy.

## 4. Interception must actually occur

Transaction annotations rely on framework interception. High-risk cases:

- manually constructing the service with `new`
- private/static/final methods not intercepted as expected
- moving the annotation to an internal helper/self-call
- calling a transactional method during construction/startup before the container path is valid
- testing only with a plain unit instance

Quarkus supports some self-interception beyond portable CDI, but verify the project/version and actual path. Do not assume Spring proxy rules or generic CDI rules blindly.

## 5. Reactive transaction lifetime

For reactive methods, a transaction may remain open until the returned reactive value terminates, not merely until the Java method returns. Preserve:

- success completion and commit
- failure completion and rollback
- cancellation behavior
- recovery operators that may convert failures into apparent success
- side effects scheduled outside the returned chain

Do not launch detached work inside a transaction and return early. The transaction cannot protect work that is no longer part of its lifecycle.

## 6. Panache style is a scale decision

### Active record

Useful for small cohesive applications where entity behavior and persistence convenience remain understandable.

Risks at scale:

- persistence calls spread through resources and business logic
- hard-to-see transaction boundaries
- entities become transport models
- tests require more framework context

### Repository

Useful when persistence needs a focused adapter, multiple query policies, or domain separation.

Risks:

- generic base repositories with no semantic value
- one-line pass-through repositories for every entity
- pretending a repository makes a rich domain model automatically

Choose by change boundaries, not ideology. Refactoring active record to repositories should be staged per feature, not performed as repository-wide churn.

## 7. Entity design

Treat entities as persistence-managed identity objects, not ordinary immutable value carriers.

Check:

- no-arg/proxy/enhancement requirements for the project
- ID generation timing
- `equals`/`hashCode` behavior before and after persistence
- mutable business keys
- lazy collections and bidirectional associations
- cascade/orphan removal ownership
- optimistic version field
- database nullability/uniqueness versus Java annotations
- serialization exclusion

Do not convert entities to records. Do not generate equality over all mutable fields or associations. Do not put an entity with unstable hash code into a `HashSet` and then assign its identifier.

## 8. Query design and N+1

Evidence first:

- enable SQL/query metrics in a safe test environment
- count queries for a representative request
- inspect execution plans for slow queries
- check result cardinality and pagination
- identify lazy access during mapping/serialization

Remedies may include fetch joins, entity graphs, projections, batching, query redesign, or explicit aggregate loading. Global `EAGER` is rarely a safe fix: it shifts cost and can create cartesian explosions.

## 9. Panache streams

Panache stream APIs often require an active transaction and must be closed. Use try-with-resources where the API returns a closeable stream. Do not return a live persistence stream from a transaction method to be consumed later.

Prefer bounded/paginated results for HTTP. A Java stream does not make a database query memory-safe by itself.

## 10. Projections

Projection DTOs or records can reduce entity loading and protect transport boundaries. Verify:

- constructor/component names and parameter metadata requirements
- nested projection support
- native reflection/serialization metadata
- query aliases
- nullability and numeric conversions
- whether the projection is a public HTTP contract or an internal read model

Do not use reflection-heavy mapping assumptions without a native test when native is shipped.

## 11. Constraints and race conditions

Application checks do not replace database constraints for persisted invariants.

Bad pattern:

```java
if (User.count("email", email) == 0) {
    User.persist(new User(email));
}
```

Concurrent requests can both pass the count. Use a unique constraint, handle the constraint violation, and map it to the domain/HTTP outcome. Similar principles apply to balances, inventory, idempotency keys, and state transitions; choose locking or atomic updates based on the invariant.

## 12. External calls inside transactions

A network call inside a database transaction increases lock/connection duration and creates ambiguous failure combinations.

Before moving it out, preserve ordering semantics. Common patterns:

- persist intent, commit, then perform idempotent work
- transactional outbox for message publication
- saga/compensation for multi-system workflows
- timeout and retry with idempotency key

Do not promise atomicity across a database and remote HTTP service without a protocol that provides it.

## 13. Migrations

Treat applied migrations as immutable history unless the deployment process explicitly permits replacement.

- add a new migration rather than editing a deployed one
- design expand/migrate/contract for rolling deployments
- keep application and schema versions compatible during rollout
- test production-like data volume and locks
- preserve defaults/nullability during backfill
- separate irreversible data changes and document rollback/forward-fix

Quarkus schema generation is useful for development but is not a substitute for managed production history where schema evolution matters.

## 14. Persistence tests

Use the smallest faithful layer:

- pure unit tests for domain policies
- repository/component tests for query behavior
- `@QuarkusTest` with the relevant database for ORM integration
- `@TestTransaction` where rollback semantics fit the test
- reactive test helpers for Hibernate Reactive; do not force blocking waits
- Testcontainers/Dev Services when dialect behavior matters

Verify constraints, rollback, locking, pagination, query count, and serialization timing—not only happy-path CRUD.

## High-signal persistence smells

| Signal | Risk | Smallest evidence |
|---|---|---|
| JPA entity returned from REST | lazy loading/API leakage | contract test and SQL trace |
| `EAGER` added to fix exception | over-fetch/cartesian cost | query count and endpoint payload |
| `@Transactional` moved to private helper | no interception/changed boundary | integration rollback test |
| count-then-insert | race | concurrent test plus DB constraint inspection |
| broad cascade/orphan removal | accidental deletion | lifecycle test with existing relationships |
| ORM call in reactive method | event-loop blocking | extension and thread trace |
| reactive call followed by `.await()` | blocked event loop | execution model and timeout test |
| stream returned outside transaction | closed session/resource leak | consumption test after method return |
| migration file rewritten | environment divergence | deployed migration history |
| external HTTP inside long transaction | lock/connection exhaustion | timing, lock, and failure matrix |

## Completion checklist

- [ ] The persistence stack and thread model are explicit.
- [ ] Transaction start/end and async completion are understood.
- [ ] Constraints protect persisted invariants.
- [ ] Entity equality and serialization are safe.
- [ ] Query cardinality and N+1 risk were checked.
- [ ] Resources/streams close inside their valid lifecycle.
- [ ] Migration compatibility is staged.
- [ ] JVM/native behavior is tested where relevant.
