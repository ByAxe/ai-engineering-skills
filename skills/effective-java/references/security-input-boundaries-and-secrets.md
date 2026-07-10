# Security, Input Boundaries, and Secrets

Security review begins with trust and authority, not with a list of sanitizers.

## Map the boundary

For each entry point, identify:

- actor and authentication mechanism
- required authorization/tenant ownership
- untrusted fields and their eventual sinks
- assets affected: data, money, credentials, availability
- side effects and idempotency
- audit requirements
- failure behavior

Validation does not replace authorization. Authentication does not prove permission for a specific object/action.

## Input handling

Use allowlisted structure and typed parsing. Define length, count, depth, numeric range, and normalization rules before expensive work. Validate after decoding/canonicalization at the layer that uses the value.

Avoid generic “sanitize all strings”; escaping is sink/context-specific.

## Injection

- parameterize SQL/JPQL values; dynamic identifiers/order clauses require allowlists or structured APIs
- avoid shell execution; use `ProcessBuilder` with separate arguments only when process execution is necessary
- prevent LDAP/NoSQL/template/expression injection according to the actual library
- use framework output encoding for HTML contexts
- never concatenate untrusted input into logs in a way that enables log forging or leaks secrets

## Path and archive safety

Resolve against a trusted root, normalize/canonicalize as appropriate, then verify containment. Consider symlinks and time-of-check/time-of-use for high-risk operations. Generate server-side filenames for uploads; enforce size/type and store outside executable/static roots.

For archives, validate every entry path and bound entry count, uncompressed size, nesting, and compression ratio.

## SSRF and outbound requests

- parse URI using a real URI type
- allowlist schemes, hosts, ports, and where necessary paths
- resolve and evaluate IP ranges according to threat model
- revalidate redirects
- block metadata/internal/link-local targets
- set timeouts and body limits
- do not put credentials in user-controlled destinations

DNS rebinding and redirects can invalidate a one-time hostname string check.

## Authentication and authorization

Prefer framework-supported mechanisms. Test:

- unauthenticated request
- authenticated but unauthorized role
- object/tenant ownership
- method/path variants
- default/deny behavior
- conflict between annotations and configuration

Do not rely solely on UI hiding or client claims.

## Secrets

- never hardcode, commit, print, or include secrets in exception messages
- use approved runtime secret sources
- redact authorization headers, cookies, tokens, passwords, keys, and sensitive personal/payment fields
- rotate after suspected exposure
- distinguish secret values from non-secret identifiers

Beware configuration debug logging and object/record generated `toString()`.

## Cryptography

Use established high-level libraries/framework features and approved algorithms. Do not invent encryption, signature, token, password hashing, nonce, or key-derivation schemes. Use `SecureRandom` for security tokens. Verify key management, rotation, authenticated encryption, and constant-time comparison where relevant.

## Deserialization and parsers

- avoid untrusted Java native deserialization
- restrict polymorphic JSON types
- disable unsafe XML external entities/DTD behavior
- limit payload/depth/collection sizes
- validate semantic authorization after parsing

## Error handling

Public errors should be useful without exposing stack traces, SQL, file paths, credentials, internal hostnames, or authorization detail. Log unexpected failures at a controlled boundary with correlation context and redaction.

## Availability and abuse

Review:

- unbounded collections/queues/uploads
- regex and parser complexity
- expensive fan-out
- missing rate/concurrency limits
- retry storms
- pagination limits
- cache key cardinality
- decompression bombs
- user-controlled sleeps/timeouts

Virtual threads make threads cheaper, not databases/downstreams/memory unlimited.

## Dependency and build security

Respect dependency verification, repositories, BOMs, lockfiles, and vulnerability policy. Do not add a package from an unverified coordinate suggested by an agent. Separate dependency upgrades and review transitive changes.

## Quarkus

Use Quarkus security/OIDC mechanisms and inspect annotation/config precedence. Read `quarkus-config-security-observability.md`. Native images and build-time config can embed or fix behavior unexpectedly; never bake secrets into build artifacts.

## Security verification

For each control, add a negative test that would fail if the control were absent. Static analysis is supplementary. Record residual threats and operational dependencies.
