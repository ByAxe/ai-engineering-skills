# API Design, Nullness, and Generics

Design an API around its semantic contract, not around the shortest implementation.

## Start from the caller

For every public or cross-module method, define:

- accepted values and invalid values
- null and empty semantics
- ownership/mutability of arguments and return values
- ordering and duplicate semantics
- failure model
- thread-safety and blocking behavior
- compatibility promise

Do not expose implementation collections, persistence entities, framework request objects, or mutable internals by accident.

## Nullness policy

Use the repository’s existing nullness annotation ecosystem consistently. Do not mix annotation packages merely because an IDE suggests one. Check whether annotations are compile-time-only, runtime-retained, package-defaulted, and understood by configured analysis.

Defaults:

- reject invalid nulls at the boundary with a meaningful contract
- avoid returning null collections; return an empty collection when absence and emptiness are semantically identical
- do not turn a programming error into a fallback silently
- use domain types or result variants when “missing,” “not authorized,” “not loaded,” and “invalid” differ

## `Optional`

Good default: use `Optional<T>` as a return type when a single value may legitimately be absent.

Avoid by default:

- `Optional` fields in entities/DTOs
- `Optional` method parameters
- `Optional<List<T>>` when empty list has the same meaning
- returning null instead of `Optional.empty()`
- calling `get()` without a proven presence condition
- using `orElse(expensiveCall())` when lazy `orElseGet` is intended

An `Optional` is a value-based container, not a serialization or dependency-injection universal.

## Parameter validation

Validate at the first trusted boundary that owns the rule. Distinguish:

- syntax validation: parseable shape
- semantic validation: domain rule
- authorization: actor may perform action
- state validation: action valid now

Avoid duplicate, contradictory validation across controller, service, and repository. Keep invariants close to the model or use case and transport validation at the edge.

## Public type choices

- Return the least specific type that fully communicates semantics. `List` communicates order and duplicates; `Set` communicates uniqueness; `SequencedSet` communicates uniqueness plus order.
- Do not return `Collection` when order is contractual.
- Do not expose mutable implementation types unless mutation is part of the API.
- Prefer domain-specific identifiers/value objects over interchangeable `String`/`long` when mix-ups are plausible.
- Avoid boolean parameters with unclear call sites; use an enum/options type when meanings are not obvious.

## Generics

### Core rules

- eliminate raw types
- keep unchecked casts localized, justified, and tested
- prefer generic methods to returning `Object`
- use bounded type parameters only when the bound enables useful operations
- avoid wildcard-heavy internal code; wildcards are most useful at API boundaries

PECS remains a useful mnemonic:

- producer: `? extends T`
- consumer: `? super T`

Do not apply it mechanically when a concrete invariant is clearer.

### Heap pollution and varargs

Generic varargs can create heap pollution. Use `@SafeVarargs` only when the method is actually safe and eligible; the annotation is a promise, not a warning suppressor. Never write into a generic varargs array in a way that can violate its runtime component type.

### Erasure traps

- overloads that differ only by generic argument erase to the same signature
- runtime type checks cannot inspect type arguments
- generic arrays cannot be created directly
- bridge methods and binary compatibility matter when changing generic inheritance

## Fluent APIs and builders

Use a builder when there are many optional fields, staged validation, or readability benefits. Avoid builders for small records/values where a constructor or named factory is clearer.

A fluent API must define whether instances are mutable, reusable, and thread-safe. Do not return `this` from a mutable object and assume callers understand lifecycle.

## Exceptions in API contracts

Choose checked exceptions when callers are expected and able to recover as part of the API contract; otherwise use focused unchecked/domain exceptions. Do not expose low-level database/client exceptions across domain boundaries unless that coupling is intentional.

Changing a checked exception, generic bound, method return mutability, or nullness contract may be source- or behavior-breaking even when bytecode still links.

## Overloads and defaults

Avoid overload sets where null is ambiguous or numeric widening picks surprising methods. Prefer a parameter object when overload combinations grow. Preserve binary compatibility: adding an overload can change source resolution for downstream code when recompiled.

## Review checklist

- Does each type communicate order, duplicates, mutability, and absence?
- Can invalid states be represented unnecessarily?
- Are nullness annotations consistent with project tooling?
- Is `Optional` limited to meaningful absence?
- Are unchecked operations localized with proof?
- Does the API leak framework/persistence details?
- Are blocking, transaction, or thread-safety requirements visible?
- Would a future variant/field require a breaking change?
