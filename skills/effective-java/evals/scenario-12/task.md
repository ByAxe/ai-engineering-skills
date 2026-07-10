# Task

Assess a multi-module Java 21 Quarkus service after a large feature merge. It uses Maven wrappers, Quarkus REST, Hibernate ORM Panache, Kafka messaging, OIDC, OpenTelemetry, Flyway, and a production native executable. The review environment can run unit tests but has no Docker-compatible runtime and cannot build a native executable. The user wants actionable cleanup, not generic SOLID advice or an immediate rewrite.

Create `java-quarkus-assessment.md` with the project profile to gather, top risk-ranked findings format, behavior/compatibility contracts, minimal target shape, dependency-aware refactor batches, exact verification per batch, Quarkus-specific checks, and a residual-risk section that clearly separates executed from blocked gates.
