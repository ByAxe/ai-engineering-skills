# Interfaces, Generics, and Type Design Smells

## Contents
- Interface ownership
- When the producer should define the interface
- Common interface smells
- Receivers and parameter choices
- Slices, maps, and ownership
- Generics: use, overuse, and deletion
- Nil and zero-value traps

## Interface ownership

Default rule:
- the consumer defines the interface
- the producer returns a concrete type

This keeps APIs flexible because concrete types can grow methods later without forcing callers into the wrong abstraction.

## When the producer should define the interface

Producer-owned interfaces are justified when the interface is itself the product or protocol, for example:
- standard protocol-style abstractions
- generated service boundaries
- plugin systems with multiple implementations and documented behavior

Even then, document behavior, concurrency expectations, and edge cases.

## Common interface smells

### Producer-owned interface for mocking
Smell when:
- the package exports an interface purely to let tests mock it
- the interface duplicates the concrete implementation's full surface

Refactor toward:
- real tests over the public API
- consumer-owned narrow interfaces where needed
- concrete types exported by default

### Fat interface
Smell when:
- an interface has many methods that most callers do not need
- test doubles become huge
- implementations drag unrelated responsibilities together

Refactor toward smaller, composable interfaces shaped by actual use.

### Returning interface unnecessarily
Smell when:
- the constructor returns an interface but only one implementation exists
- callers lose useful methods and configuration surface

Refactor toward returning the concrete type.

### Pointer to interface
Almost always a smell.
Pass interfaces by value. Use a pointer to a concrete type if mutation or shared state is needed.

### Interface pair explosion
Smell when the package has many `Foo`, `Fooer`, `fooImpl`, `MockFoo`, `fooAdapter` shapes with little semantic difference.
Delete layers first.

## Receivers and parameter choices

### Mixed receiver types
Smell when a type mixes value and pointer receivers without a strong reason.
Pick one receiver model for the type.

### Passing pointers just to save bytes
Smell when small values or interface values are passed by pointer only out of habit.
Prefer values unless mutation, synchronization, or clear large-copy cost requires pointers.

### Copying synchronized structs
Any struct containing `sync.Mutex`, `sync.RWMutex`, or similar should generally use pointer receivers and should not be copied after first use.

## Slices, maps, and ownership

### Sharing caller-owned slices or maps accidentally
Smell when:
- a constructor stores the caller's slice or map directly
- a getter returns internal mutable state directly

Refactor toward copying at boundaries when ownership should remain private.

### Nil vs empty semantics are unclear
Smell when public APIs inconsistently return `nil` and empty slices or maps without documenting the meaning.
Pick and document one semantic story.

### `time.Time` compared with `==`
Usually a smell.
Prefer `t.Equal(u)` unless the code specifically wants full structural equality.

## Generics: use, overuse, and deletion

Use type parameters when:
- you are writing the **same algorithm** multiple times for different types
- the implementation is meaningfully identical across types
- you are building a true reusable data structure or helper

Smells:
- generic code before duplicated code exists
- replacing interfaces with type parameters when dynamic behavior is the real need
- type parameters where each type needs different behavior anyway
- complex constraints that hide the actual domain

Refactor toward:
- ordinary concrete code first
- interfaces when behavior varies
- generics only when type-based duplication is real and the implementation is shared

## Nil and zero-value traps

### Nil interface trap
An interface value can be non-nil while holding a typed nil pointer.
Smell signs:
- `return (*MyError)(nil)` assigned to `error`
- confusing nil checks around interfaces

Refactor toward returning plain `nil` when there is no error/value.

### Invalid zero values without guardrails
Smell when a type looks easy to instantiate but the zero value is actually invalid and silently dangerous.

Refactor toward:
- making fields unexported and forcing construction through `New...`
- or explicitly designing the zero value to be usable when that makes sense

### Missing compile-time interface assertions where contract matters
If a concrete type is intended to implement an important public interface, a compile-time assertion may improve maintenance:

```go
var _ io.Reader = (*MyReader)(nil)
```

Do this sparingly, where the contract is part of the design.
