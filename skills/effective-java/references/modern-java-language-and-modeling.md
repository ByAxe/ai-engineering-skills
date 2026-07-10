# Modern Java Language and Modeling

The project-configured Java release is authoritative. This reference emphasizes Java 21 final features and calls out preview/version gates.

## Release gate

Before using a feature, check all of:

- Maven compiler `release`/toolchain or Gradle toolchain/language version
- CI and production runtime JDK
- preview compiler and runtime flags
- annotation processors and bytecode tools
- framework support, especially Quarkus and native-image toolchain

Do not infer the release from the JDK installed on the agent host.

## Records

Use a record when the type is a transparent carrier whose state is exactly its components.

Good fits:

- request/response DTOs
- immutable command/query data
- value tuples with component-based equality
- projection results

Avoid or scrutinize:

- JPA entities, mutable lifecycle objects, or proxy/subclass requirements
- types whose identity differs from component equality
- components that expose mutable arrays or collections
- components containing secrets, because generated `toString()` exposes component values
- APIs where adding/reordering a component would be a compatibility problem

### Record traps

- Generated equality uses component equality. An array component therefore compares by reference, not contents.
- `final` fields do not make referenced collections or arrays immutable. Defensively copy in the constructor and accessor if ownership requires it.
- A compact constructor validates/normalizes parameters before implicit assignment. Do not assign component fields directly in a compact constructor.
- Overriding accessors with surprising behavior undermines record patterns and the transparent-carrier contract.
- Converting a class to a record changes constructor/accessor names, inheritance, equality, serialization shape, and often framework behavior.

Example with defensive ownership:

```java
public record Batch(List<Job> jobs) {
    public Batch {
        jobs = List.copyOf(jobs);
    }
}
```

This rejects null elements and returns an unmodifiable list; confirm those are desired contracts.

## Sealed hierarchies

Use sealed types when the variant set is intentionally closed and controlled in the relevant module/package.

Benefits:

- explicit domain variants
- exhaustive pattern switches
- fewer invalid fallback branches

Traps:

- adding a broad `default` to an otherwise exhaustive switch hides compiler feedback when a permitted subtype is added
- adding a permitted subtype is a compatibility event for downstream exhaustive logic
- proxies/frameworks may require subclassing; do not seal framework-managed types casually
- use a non-sealed subtype only when extension is genuinely intended

Prefer explicit null policy. A pattern switch without `case null` still throws `NullPointerException`; `default` does not absorb null.

## Pattern matching and switch

Use pattern switches when they make a closed decision table clearer than visitor boilerplate or cast ladders.

Review:

- exhaustiveness and null behavior
- dominance/order of cases
- side effects in guards
- whether the selector’s type is genuinely the right abstraction
- whether a polymorphic method would localize behavior better

Avoid a switch over type codes when the hierarchy is open and behavior belongs on the objects.

## Record patterns

Record patterns are useful for concise deconstruction, especially nested immutable data. Do not over-nest until variable names and domain meaning disappear. Remember that component accessors execute during matching and can fail if they are badly overridden.

## `var`

Use `var` for local variables when the initializer makes the type obvious and the name conveys meaning. Avoid it when:

- the inferred generic/numeric type is non-obvious
- the initializer is a factory with a weak name
- the declared interface is part of the explanation
- it obscures a resource, proxy, or mutable implementation distinction

`var` is not dynamic typing and cannot be used for fields, method parameters, or return types.

## Sequenced collections in Java 21

`SequencedCollection`, `SequencedSet`, and `SequencedMap` express encounter order and provide first/last/reversed operations. Use them when order is an API contract rather than accepting `Collection` and documenting order only in prose.

`reversed()` is a view, not necessarily a copy. Mutations may write through when supported. Some positioning operations remain unsupported for sorted collections.

## Switch expressions

Prefer switch expressions for total value selection. Keep each arm small; extract behavior when arms become workflows. Do not use `yield` blocks as a container for unrelated side effects.

## Text blocks and formatted strings

Text blocks improve embedded SQL/JSON readability but do not parameterize SQL, escape JSON, or normalize indentation exactly as an external protocol might require. Test resulting content when whitespace is contractual.

Use `String.formatted` for readability where locale is irrelevant. For locale-sensitive formatting, use explicit `Locale`/formatters.

## Preview features in Java 21

Structured concurrency (JEP 453) and scoped values (JEP 446) are preview features in Java 21. Do not introduce or enable preview features unless the repository already opts in or the user explicitly accepts the compiler/runtime/deployment implications. Check the exact JDK because these APIs evolved after Java 21.

## Modernization decision

Adopt a feature only when it improves at least one of:

- expressible invariant
- exhaustiveness
- ownership/immutability
- error surface
- readability under the team’s conventions
- measured runtime behavior

Preserve the old code when modernization is merely cosmetic or creates a version/compatibility burden.

## Primary sources

- OpenJDK JEP 431 — Sequenced Collections
- OpenJDK JEP 440 — Record Patterns
- OpenJDK JEP 441 — Pattern Matching for `switch`
- OpenJDK JEP 444 — Virtual Threads
- OpenJDK JEP 446 — Scoped Values (Preview)
- OpenJDK JEP 453 — Structured Concurrency (Preview)
- Oracle Java 21 language guide — Record Classes

Links are cataloged in `source-index.md`.
