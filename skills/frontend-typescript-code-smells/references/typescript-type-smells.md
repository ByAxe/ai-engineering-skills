# TypeScript Type Smells and Refactoring Recipes

## Contents
- Core principles for type-safe frontend code
- Smell TS-01: `any` leakage
- Smell TS-02: Overusing type assertions
- Smell TS-03: Non-null assertion operator overuse
- Smell TS-04: Inconsistent nullability
- Smell TS-05: Broad primitive types instead of constrained domains
- Smell TS-06: Stringly typed ids and tokens
- Smell TS-07: Boolean trap parameters and flag arguments
- Smell TS-08: God interfaces with many optional fields
- Smell TS-09: Unmaintainable union or conditional type complexity
- Smell TS-10: Mutable types where readonly is intended
- Smell TS-11: Unsafe DOM typing and event typing
- Smell TS-12: Leaky abstraction types across modules
- Refactoring recipes (copy-paste patterns)
- Sources

---

## Core principles for type-safe frontend code

1. **Make invalid states unrepresentable**
   - Use discriminated unions for loading and error states.
   - Prefer explicit "none" states rather than null sprinkled everywhere.

2. **Keep runtime and types aligned**
   - Type assertions and non-null assertions are compile-time only; they do not add runtime checks.
   - When safety depends on runtime behavior, add runtime checks close to the boundary.

3. **Push uncertainty to the edges**
   - Boundary layers: API decoding, localStorage parsing, DOM lookups, environment variables.
   - Core layers: pure business logic should operate on validated, well-typed data.

4. **Prefer small, composable types**
   - Model domains with small primitives, then compose.
   - Avoid mega-interfaces that represent multiple concepts.

---

## Smell TS-01: `any` leakage

### Symptoms
- Function parameters typed as `any` or returned values typed as `any`.
- `JSON.parse` result used directly.
- Third-party library types bypassed with `as any`.

### Why it matters
- Disables type checking and often masks correctness bugs until runtime.

### Refactor strategy
1. Replace `any` with `unknown` at the boundary.
2. Narrow before use:
   - predicate type guards
   - runtime validation
   - schema-based parsing if the project already uses it
3. Improve the type at the source (API client, adapter) so callers stay clean.

### Example
Bad:
```ts
function parseUser(raw: any) {
  return raw.user.name.toUpperCase();
}
```

Better:
```ts
type User = { name: string };

function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null && typeof (value as any).name === "string";
}

function parseUser(raw: unknown): User {
  if (!isUser(raw)) throw new Error("Invalid user payload");
  return raw;
}
```

---

## Smell TS-02: Overusing type assertions

### Symptoms
- Frequent use of `as Something` to silence errors.
- Assertions around API data or DOM queries without runtime checks.

### Why it matters
- Assertions are removed at compile time; incorrect assertions become runtime bugs.

### Refactor strategy
- Prefer narrowing via checks.
- Introduce helper functions that validate and return typed results.
- Use `satisfies` for shape checking without changing the inferred type.

---

## Smell TS-03: Non-null assertion operator overuse

### Symptoms
- `value!.prop` appears frequently.
- Used as a shortcut around strict null checks.

### Why it matters
- The non-null assertion operator is removed in emitted JavaScript. If the value is actually nullish at runtime, the code still throws.

### Refactor strategy
1. Prefer modeling:
   - Use discriminated unions for async states.
   - Ensure required props are required at the type level.
2. Prefer runtime checks close to the source.
3. Prefer early returns for nullish states.

Example:
Bad:
```ts
const el = document.getElementById("root")!;
el.innerHTML = "Hello";
```

Better:
```ts
const el = document.getElementById("root");
if (!el) throw new Error("Missing #root element");
el.textContent = "Hello";
```

---

## Smell TS-04: Inconsistent nullability

### Symptoms
- Some functions return `T | null`, others return `T | undefined` for the same concept.
- UI state mixes "not loaded yet" with "loaded but empty" using the same null.

### Refactor strategy
- Choose one representation per concept:
  - Optional field for "not present"
  - Explicit union state for async
- Create shared types and use them consistently across modules.

---

## Smell TS-05: Broad primitive types instead of constrained domains

### Symptoms
- Everything is `string`, `number`, or `boolean`.
- Many bug-prone conditions in code.

### Refactor strategy
- Use literal unions:
```ts
type SortOrder = "asc" | "desc";
```
- Use branded types for ids:
```ts
type Brand<T, B extends string> = T & { readonly __brand: B };
type UserId = Brand<string, "UserId">;
```
- Parse at the boundary and enforce internally.

---

## Smell TS-06: Stringly typed ids and tokens

### Symptoms
- Function signature: `(id: string)` used for many different id concepts.
- Token and id passed interchangeably.

### Refactor strategy
- Introduce branded types or dedicated wrappers.
- Provide explicit constructors at boundaries.

---

## Smell TS-07: Boolean trap parameters and flag arguments

### Symptoms
- `fn(value, true)` where `true` means something unclear.
- Multiple boolean flags: `fn(x, true, false, true)`.

### Refactor strategy
- Replace with:
  - Options object with named fields
  - Literal union mode

Bad:
```ts
renderToast(message, true);
```

Better:
```ts
renderToast(message, { persistent: true });
```

---

## Smell TS-08: God interfaces with many optional fields

### Symptoms
- A single interface used for multiple states.
- Many optional fields and checks everywhere.

### Refactor strategy
- Use discriminated unions:
```ts
type RequestState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: Data }
  | { status: "error"; error: Error };
```

---

## Smell TS-09: Unmaintainable union or conditional type complexity

### Symptoms
- Types that are hard to read or change.
- Deep conditional types that slow down compilation.

### Refactor strategy
- Replace with explicit named types.
- Prefer runtime mapping plus simple types over type-level programming for UI layers.

---

## Smell TS-10: Mutable types where readonly is intended

### Symptoms
- Objects mutated after creation.
- Arrays modified in place, causing subtle UI bugs.

### Refactor strategy
- Use `readonly` for props and state where possible.
- Return new objects for state updates.

---

## Smell TS-11: Unsafe DOM typing and event typing

### Symptoms
- DOM elements typed with assertions instead of checks.
- Event handlers typed as `any`.

### Refactor strategy
- Prefer proper generics and correct event types.
- For DOM queries, check for null and use specific element types.

---

## Smell TS-12: Leaky abstraction types across modules

### Symptoms
- UI components depend on raw API response shapes.
- API client types leak into many layers.

### Refactor strategy
- Introduce a mapper:
  - API type in api layer
  - Domain type internally
- Make UI depend on stable domain types.

---

## Refactoring recipes

### Recipe: Replace `any` with `unknown` at boundaries
1. Change type to `unknown`.
2. Add runtime checks or schema validation.
3. Create a typed result.

### Recipe: Replace assertion with predicate guard
```ts
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
```

### Recipe: Use `satisfies` to check shapes without widening
```ts
const routes = {
  home: "/",
  users: "/users",
} satisfies Record<string, string>;
```

---

## Sources

- TypeScript Handbook (type assertions): https://www.typescriptlang.org/docs/handbook/2/everyday-types.html
- TypeScript 2.0 release notes (non-null assertion operator): https://www.typescriptlang.org/docs/handbook/release-notes/typescript-2-0.html
