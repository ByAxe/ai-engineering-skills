# Package and API Design Smells

## Contents
- Package-first review questions
- Naming and stutter
- Package size and cohesion
- `internal/`, `cmd/`, and module layout
- Export surface smells
- Constructors, options, and defaults
- Globals, registries, and `init()`
- Compatibility and change strategy

## Package-first review questions

Start every Go review here:
- Is the package name short, clear, and non-stuttering?
- Do exported identifiers read well at the call site?
- Does the package expose only what users genuinely need?
- Are dependencies flowing in one sensible direction?
- Is the package mixing unrelated domains just because the files are nearby?

## Naming and stutter

Smells:
- package names like `util`, `common`, `misc`, `api`, `types`, `interfaces`
- exported names that repeat the package name, such as `cache.CacheClient`
- getters named `GetX` without a strong reason

Preferred refactors:
- rename packages to domain nouns
- drop redundant prefixes from exported names
- use noun-like names for query methods and verb-like names for actions

## Package size and cohesion

A large package is a smell when:
- users import it for one type and inherit many unrelated exports
- tests are hard because private details are entangled
- the package changes for unrelated reasons

Split a package when there is a durable boundary:
- transport vs domain
- storage vs orchestration
- reusable internal utility vs product surface

Do **not** split just to create more folders.

## `internal/`, `cmd/`, and module layout

Strong default layout:
- `cmd/<tool>` for binaries
- `internal/` for non-public implementation packages
- exported library packages only where reuse is a real requirement

Module guidance:
- start with one module per repository unless there is a genuine independent release boundary
- split into multiple modules only when versioning and release cadence truly differ
- use workspaces for concurrent development across related modules, not as an excuse for premature module splitting

## Export surface smells

### Too many exports
Smell when:
- helper types and internal config leak into the public surface
- exported structs expose fields that should be invariants
- callers can misuse lifecycle methods in unsafe order

Refactor toward:
- unexported fields
- constructors with validation
- internal implementation packages
- concrete return types with focused methods

### Public embedding of implementation details
Smell when:
- embedding exposes mutexes, transports, or fields that are implementation details
- callers can reach through the API and couple to internals

Refactor toward explicit named fields and forwarding methods only when they add a real contract.

### Exported interface without a product reason
Smell when:
- a package exports `Fooer` and `Foo` with one implementation
- the interface exists mainly to support mocking or future possibility

Refactor toward exporting only the concrete type unless the interface is the actual product or protocol.

## Constructors, options, and defaults

### Constructor smell: bool or string mode soup
Signs:
- `NewClient(addr string, secure bool, retries int, logJSON bool, mode string)`

Refactor toward:
- explicit required parameters
- a config struct for many required fields
- functional options only when there are many optional parameters with stable defaults and the option set is expected to grow

### Option struct smell
A config or option struct is a smell when:
- it mixes per-call data with long-lived dependencies
- it becomes a dumping ground for every future knob
- it hides mandatory fields through zero values that are not actually valid

### Functional options smell
Functional options are useful, but become a smell when:
- there are only two or three arguments and no growth pressure
- call sites become opaque
- invariants are only discovered at runtime

Use them when optional behavior is real and defaults are meaningful.

## Globals, registries, and `init()`

Smells:
- mutable package globals
- hidden singletons
- `init()` performing I/O, network setup, goroutine startup, or registration with global state
- plugin registries that make tests order-dependent

Refactor toward:
- explicit constructors
- dependency injection via parameters or fields
- registration driven from `main` or top-level wiring code
- objects that own their own background lifecycle

## Compatibility and change strategy

For public packages, prefer:
- add, do not change or remove
- new options rather than semantic breakage in existing methods
- concrete return types that can grow methods over time
- documentation that explains behavioral contracts

When proposing a breaking refactor, state it plainly and separate:
- what is improved
- who breaks
- migration path
- whether an adapter or compatibility layer is worthwhile
