# Task

A Quarkus service has four findings:

1. A feature toggle expected to change via an environment variable at runtime is read by code generated during augmentation.
2. Authentication failures log the complete bearer token.
3. `@RolesAllowed("support")` protects `GET /accounts/{id}`, but any support user can request any account; the product contract requires tenant ownership except for supervisors.
4. A counter uses `accountId` as a metric label.

Create `security-config-observability-review.md` that ranks the findings, proves the relevant contract or framework phase, recommends the smallest remedies, and defines tests/operational verification. Keep authentication, authorization, ownership, logging, and telemetry concerns distinct.
