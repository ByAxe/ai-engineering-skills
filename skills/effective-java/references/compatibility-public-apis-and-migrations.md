# Compatibility, Public APIs, and Migrations

Compatibility has multiple dimensions. A patch can be binary-compatible and still break users.

## Compatibility dimensions

- **source:** downstream source still compiles
- **binary:** existing compiled bytecode still links
- **behavioral:** results, failures, timing, order, mutability remain acceptable
- **wire:** HTTP/JSON/event/schema clients remain compatible
- **data:** persisted rows/files/serialized objects remain readable and correct
- **operational:** configuration, logs, metrics, health, startup, resource usage remain compatible
- **security:** permissions and trust boundaries do not weaken

State which dimensions apply.

## Public Java API changes

Potentially breaking:

- removing/renaming/moving public types or methods
- changing return/parameter type or generic bounds
- adding checked exceptions
- reducing visibility
- changing abstract/default methods
- changing nullness or mutability
- adding overloads that alter source resolution
- changing equality/hash/order semantics
- changing blocking/thread-safety contract

Adding a method to an interface can break implementers unless a safe default exists. A default method can still create conflicts or behavioral surprises.

## Records

Adding, removing, reordering, or changing a record component changes constructor/accessors, equality/hash/toString, deconstruction patterns, and serialization shape. Treat it as an API/data event, not a private-field edit.

## Sealed types and enums

Adding a permitted subtype or enum constant can break exhaustive downstream switches or unknown-value handling. Removing or renaming is more obviously breaking. Design wire formats to tolerate future variants where openness is required.

## Collections and exceptions

Changing a returned list from mutable to unmodifiable, ordered to unordered, live view to snapshot, or null-tolerant to null-rejecting is behavioral compatibility. Changing exception type/status/rollback behavior can break callers and retries.

## Wire contracts

Review:

- field names and aliases
- required/optional/null/absent
- enum values/discriminator
- numeric precision
- date/time format
- ordering when clients rely on it
- error status/code/body
- pagination tokens/sort stability
- unknown field/value tolerance

Use contract tests and schemas where available. Do not expose entity shape as an accidental API.

## Database migration compatibility

For rolling deploys, old and new application versions may overlap. Use expand/contract:

1. add compatible schema
2. deploy code that handles both
3. backfill
4. switch reads/writes
5. remove old schema in a later release

Avoid rename/drop/not-null changes in one step unless deployment is coordinated and downtime accepted.

## Configuration compatibility

Renaming a property requires alias/deprecation or coordinated rollout. Quarkus build-time-fixed properties may require rebuilding rather than runtime configuration change. Defaults are behavior; changing them can be breaking.

## Deprecation

A useful deprecation includes:

- replacement
- migration instructions
- semantic differences
- removal timeline/version policy
- tests until removal

Do not keep two implementations drifting indefinitely.

## Migration design

For behavior/API migration:

- inventory consumers
- define old/new overlap
- add adapters or dual read/write only when necessary
- instrument adoption
- provide rollback
- remove compatibility layer after evidence

## Refactor compatibility check

Before claiming behavior preservation, compare:

- public signatures
- serialized output
- equality/hash/order/mutability
- exceptions/statuses
- transactions and side-effect timing
- thread/execution model
- config keys/defaults
- logs/metrics relied on operationally

Compilation alone proves only a small part of compatibility.
