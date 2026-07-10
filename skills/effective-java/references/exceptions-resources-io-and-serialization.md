# Exceptions, Resources, I/O, and Serialization

Boundary code must make failure, lifetime, encoding, and data-shape semantics explicit.

## Exception design

Use exceptions to communicate failure at the abstraction level the caller understands.

- preserve the original cause when translating
- catch the narrowest useful type
- do not catch `Throwable` for ordinary application recovery
- avoid empty catches and fallback values that erase failure
- avoid logging and rethrowing at every layer; log once where context and ownership are sufficient
- do not expose database/client stack details in public responses
- distinguish expected domain outcomes from programming/infrastructure failures

A broad `catch (Exception)` can be justified at a process or protocol boundary that converts all failures, but it still needs cancellation/interruption and fatal-error policy.

## Interrupted execution

When catching `InterruptedException`, either propagate it or restore the interrupt flag with `Thread.currentThread().interrupt()` before translating/returning. Do not treat interruption as an ordinary retryable error. In async/reactive code, preserve cancellation semantics rather than wrapping everything indiscriminately.

## Try-with-resources

Use try-with-resources for owned `AutoCloseable` resources. It preserves suppressed exceptions when both work and close fail. Clarify ownership: do not close a stream/client/session passed in by a caller unless the API transfers ownership.

Streams from I/O sources such as `Files.lines` must be closed; collection streams normally do not need closing.

## File I/O

- specify `Charset`, usually UTF-8 when the format says so
- bound input size before reading all bytes/text
- distinguish create, replace, append, and atomic-replace semantics
- write to a temporary file and atomically move when partial output is unacceptable and the filesystem supports it
- preserve permissions/ownership when required
- handle symlinks and canonical containment for untrusted paths
- do not use user input directly as a path or filename

A lexical `normalize()` alone does not prove a path remains inside a trusted root when symlinks or filesystem races matter.

## Network and HTTP clients

Always define:

- connect timeout
- request/read timeout
- maximum response/body size when untrusted
- redirect policy
- retry/idempotency policy
- TLS/hostname verification
- URI construction and encoding
- client lifecycle and connection-pool ownership

Do not concatenate URL query strings manually. Distinguish encoding a path segment from encoding a whole URI.

## Text and regex

- use explicit charset for `String`/byte conversion
- quote untrusted literal text used in regex (`Pattern.quote`) when regex semantics are not intended
- consider catastrophic backtracking and input length for untrusted regex processing
- avoid platform line separator assumptions in wire formats

## JSON and transport serialization

Treat serialization as a public contract:

- property names and aliases
- required/optional/null/absent semantics
- enum representation
- numeric precision
- date/time format and zone
- unknown-field behavior
- polymorphic type policy
- constructor/accessor visibility
- collection order

Use transport DTOs when entity/domain shape and wire shape have different lifecycles. A record can be a good DTO when its generated constructor/equality/toString and framework support are suitable.

Never enable unsafe global polymorphic deserialization for untrusted input. Use explicit allowlisted subtypes or framework-supported sealed models.

## Java native serialization

Avoid Java object deserialization for untrusted data. Existing serialized forms are compatibility contracts; changing fields, class names, hierarchy, or `serialVersionUID` can break stored or transmitted data. Prefer explicit versioned formats for new external contracts.

## XML and archive inputs

Disable unsafe external entity/DTD behavior using the chosen parser’s supported secure configuration. Bound nested depth, entity expansion, archive entry count/size, and decompression ratio. Prevent Zip Slip by validating each resolved entry path remains under the destination.

## Logging failures

Do not log secrets, authorization headers, tokens, full payment data, or unbounded untrusted payloads. Use parameterized logging rather than string concatenation. Include stable correlation identifiers, not sensitive data. Preserve stack traces for unexpected failures at the owner boundary.

## Native-image implications

Reflection, resource loading, dynamic proxies, and runtime class generation can differ in a native executable. Prefer framework-integrated serialization and precise registration. Validate the actual native artifact when the changed boundary relies on reflection/resources.

## Review checklist

- Is the exception translated at the correct abstraction boundary?
- Are causes, interruption, and cancellation preserved?
- Who owns and closes each resource?
- Are charset, size, timeout, redirect, and retry policies explicit?
- Are untrusted paths/URLs contained after canonicalization and redirects?
- Is serialization versioned and free of entity/internal leakage?
- Are parser/deserializer features safe for hostile input?
