# Task

A Quarkus Hibernate ORM service currently:

- returns `OrderEntity` directly from REST;
- implements `equals`/`hashCode` using every mutable field and a generated database ID;
- marks all relationships `EAGER` to avoid lazy-loading errors;
- calls a payment provider inside a database transaction;
- edits an already-applied Flyway migration to add a uniqueness rule.

The endpoint is live and clients depend on the current JSON shape. Create `persistence-risk-assessment.md` with ranked findings, contract evidence to gather, a staged target shape, migration and rollout safety, idempotency and transaction recommendations, and focused tests. Do not replace the whole persistence layer.
