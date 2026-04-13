# Classical Smells Through a Go Lens

## Contents
- Why translation is needed
- Bloaters in Go
- Object-orientation abusers translated to Go
- Change preventers in Go
- Dispensables in Go
- Coupling smells in Go
- SOLID through Go, carefully adapted

## Why translation is needed

Many classical smell catalogs assume classes, inheritance hierarchies, and heavyweight polymorphism.
Go puts pressure elsewhere:
- packages instead of classes
- exported APIs instead of inheritance trees
- interfaces as small consumer-side contracts
- explicit errors, cleanup, and concurrency lifecycles

So the right question is not "Where is the Large Class?" but often:
- which package is doing too much?
- which export locks callers into the wrong abstraction?
- where is ownership of cancellation, cleanup, or mutation unclear?

## Bloaters in Go

### Long Method → Long function or orchestration closure
Smell when:
- one function mixes validation, I/O, retries, metrics, and formatting
- the function has multiple ownership responsibilities
- tests can only cover it end-to-end

Refactor toward:
- pure helpers
- clear error and cleanup boundaries
- small orchestration functions that call well-named steps

### Large Class → God package, god struct, or god service
Smell when:
- one package owns unrelated domains
- a single exported type coordinates storage, HTTP, validation, retries, metrics, and config
- callers import one package to reach many unrelated concepts

Refactor toward:
- smaller packages organized by stable domain or boundary
- private helpers and internal packages
- constructors that inject dependencies explicitly

### Primitive Obsession → Stringly typed domain and `map[string]any` sprawl
Smell when:
- IDs, states, permissions, and modes are all raw strings
- request and config data move around as generic maps
- callers must remember undocumented allowed values

Refactor toward:
- domain types
- typed config structs
- narrow enums or constants when the set is closed
- validation close to boundaries

### Long Parameter List → Ownership or config unclear
In Go, explicit parameters are often good.
It becomes a smell when:
- the function takes many loosely related values with unclear ownership
- multiple parameters always travel together
- booleans and strings encode modes that should be structural

Refactor toward:
- a small domain type or request struct
- explicit dependencies via constructor fields
- variadic options only when there are many optional knobs and stable defaults

### Data Clumps → Repeated request bundles
Common signs:
- the same `(ctx, logger, tracer, clock, cfg, userID)` cluster appears everywhere
- helpers only exist to shuttle contextless data around

Refactor toward:
- moving stable dependencies onto a type
- keeping per-call data as explicit parameters
- avoiding the mistake of hiding `context.Context` inside a struct

## Object-orientation abusers translated to Go

### Switch Statements
A `switch` is **not** automatically a smell in Go.
It is often the clearest solution for:
- tokens and protocol states
- small closed sets
- formatting or decoding decisions

It becomes a smell when:
- the same `switch` is duplicated across packages
- the cases are open-ended and change frequently
- the switch hides package-boundary problems

Refactor only when the duplication or volatility justifies a new abstraction.

### Refused Bequest / Parallel Inheritance Hierarchies
Go does not have classical inheritance hierarchies, but similar pain appears as:
- wrapper types that mirror another type with pass-through methods
- generated-looking interface and implementation pairs with no real boundary
- duplicated package trees that must evolve in lockstep

Refactor toward:
- concrete types plus small consumer-owned interfaces
- composition without mirrored APIs
- deleting layers that do not create a real seam

### Speculative Generality
This is one of the most common Go smells.
Signs:
- interfaces before a second implementation exists
- generic types before duplicated code exists
- factories, registries, and adapters without a real boundary

Refactor by deleting the abstraction first.

## Change preventers in Go

### Divergent Change
Common Go form:
- one package changes for API, database, HTTP, logging, and metrics reasons all at once
- exported types force many packages to update together

Refactor toward:
- narrower package purpose
- concrete internal implementation behind a smaller exported surface
- separation between transport, domain, and storage where real boundaries exist

### Shotgun Surgery
Common Go form:
- changing one concept requires editing many duplicated interfaces, mocks, constructors, and wrappers

Root cause is often:
- producer-owned interfaces
- giant option plumbing
- too many mirrored abstractions

Refactor by collapsing the abstraction graph.

## Dispensables in Go

### Comments as deodorant
Comments are valuable for contracts, invariants, and behavior.
They are a smell when they only explain confusing code that should be simplified instead.

### Duplicate Code
Important in Go, but do not remove all duplication blindly.
A little duplication is often cheaper than an early abstraction.
Remove duplication when:
- behavior truly must stay consistent
- bugs already arise from drift
- there is a real common concept, not just similar syntax

### Lazy Class / Dead Abstraction
Go version:
- tiny wrapper packages with almost no logic
- interfaces with one implementation and no boundary value
- helper types whose only job is to forward calls

Delete aggressively.

## Coupling smells in Go

### Feature Envy
Go version:
- one package reaches deeply into another package’s data and rules
- behavior lives far from the data or invariants it depends on

Move behavior closer to the package that owns the invariant.

### Middle Man
Common signs:
- a package exists mostly to forward to another package
- wrapper methods add no semantics, safety, or compatibility protection

Delete or merge unless the wrapper is a meaningful boundary.

### Inappropriate Intimacy
Go version:
- packages rely on shared mutable globals
- callers depend on undocumented side effects or initialization order
- tests need package internals because the public API is not coherent

Refactor toward explicit dependencies and coherent exports.

## SOLID through Go, carefully adapted

Use SOLID as a lens, not as a mandate.

### SRP: Single Responsibility Principle
In Go, apply SRP mainly to packages and exported types.
Ask:
- does this package have one clear reason to change?
- does this exported type mix unrelated roles?

### OCP: Open/Closed Principle
Do not force open-ended polymorphism everywhere.
In Go, closed sets and `switch` statements are often correct.
Apply OCP when there is a genuine extension boundary, such as plugins, storage backends, or transport adapters.

### LSP: Liskov Substitution Principle
Most relevant for interfaces.
Ask:
- does the interface document behavior, not just method signatures?
- can callers rely on all implementations behaving within the same contract?

### ISP: Interface Segregation Principle
This maps extremely well to Go.
Prefer tiny interfaces owned by the consumer and shaped by actual use.

### DIP: Dependency Inversion Principle
Good Go tends to use explicit constructor injection and parameter passing, not service locators or ambient globals.
Apply DIP by depending on small contracts at the consuming boundary, not by manufacturing interfaces everywhere.
