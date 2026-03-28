# Security and Authorization for Quarkus Cleanup

Use this guide when auth, roles, or secrets handling need review.

## Prefer Quarkus Security Features Over Ad-Hoc Logic

Build on:

- Quarkus security annotations
- OIDC support when applicable
- explicit role-based access control
- consistent identity extraction

Avoid hand-rolled auth rules in random services.

## Keep Security Close to the Boundary

Common pattern:

- resource enforces endpoint access
- service receives already-authorized context or explicit subject information
- domain rules still validate ownership or business permissions

Do not rely only on UI or client-side behavior.

## OIDC and External Identity

When the service uses OIDC, keep the integration explicit:

- config grouped in one namespace
- token handling centralized
- role mapping visible
- downstream propagation intentional

## Development-Only Auth

Properties-file based auth is for development and testing, not for production.

Treat any lingering dev-only authentication setup in production code as a cleanup target.

## Principle of Least Privilege

Review:

- endpoints too broadly exposed
- “admin” roles reused for normal tasks
- services that trust client-provided IDs without ownership checks
- hidden internal endpoints left open

## Security Logging

Log security-relevant events carefully:

- enough context to investigate
- no secret leakage
- no full token dumps
- no passwords or credential material

## Security Review Questions

- Is authorization explicit at the boundary?
- Are dev-only auth mechanisms confined to dev/test?
- Are subject and role assumptions clear?
- Are secrets and tokens protected in logs?
- Are business ownership checks still enforced after auth?
