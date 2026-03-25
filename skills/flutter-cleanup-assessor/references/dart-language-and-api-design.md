# Dart Language and API Design

Use this file when the cleanup scope includes naming, null safety, imports, public APIs, modern Dart features, or style consistency.

## Naming and file organization

Prefer:

- `UpperCamelCase` for types
- `lowerCamelCase` for variables, methods, parameters, and named constants
- `lowercase_with_underscores` for file names

Choose names that say what the thing is or does. Avoid vague abbreviations unless they are standard in the project domain.

## Imports

- Do not import another package's `src/`.
- Keep imports stable and clear.
- Avoid awkward relative import paths that cross too many boundaries when package imports would be clearer.
- Group imports consistently.

## Null safety

- Use non-nullable types by default.
- Do not hide state-machine complexity inside nullable fields unless the absence is truly the only additional meaning.
- Avoid unnecessary `!`.
- Prefer explicit states or typed results over nullable "maybe it failed" values.

## Public API design

- Prefer narrow, typed public APIs.
- Do not expose mutable internals.
- Prefer immutable models where practical.
- Avoid custom equality on mutable classes.

## Modern Dart features that can help

### Class modifiers

Use `final`, `sealed`, `base`, or `interface` when they clarify intent.

### Patterns and records

Use them when they improve readability, not just because they are available.

#### Example

```dart
switch (result) {
  case LoadProfileSuccess(profile: final profile):
    return ProfileLoadedView(profile: profile);
  case LoadProfileFailure(message: final message):
    return ErrorView(message: message);
}
```

### Sealed result objects

Useful for typed outcomes:

```dart
sealed class SaveOrderResult {
  const SaveOrderResult();
}

final class SaveOrderSuccess extends SaveOrderResult {
  const SaveOrderSuccess(this.orderId);

  final String orderId;
}

final class SaveOrderFailure extends SaveOrderResult {
  const SaveOrderFailure(this.message);

  final String message;
}
```

## Prefer `final` and `const`

Use `final` for values that are assigned once.
Use `const` for compile-time constants and immutable widget construction where natural.

## Exception handling

- Catch specific exceptions when you can act on them.
- Use `rethrow` when preserving the original exception.
- Avoid broad catches that erase meaning.
- Do not catch `Error` just to silence it.

## Smells

- vague names like `data`, `model`, `manager`, `helper`, `util`
- `dynamic` or `Object?` where a real type is available
- `!` scattered as a design strategy
- mutable model classes with custom equality
- public APIs that return many unrelated shapes depending on hidden conditions

## Review checklist

- Are names consistent and intention-revealing?
- Are imports clean and stable?
- Is null safety used well rather than worked around?
- Do modern Dart features make the code clearer?
- Are public APIs small and typed?
- Are exceptions handled precisely?

See also:

- `references/data-layer-and-error-handling.md`
- `references/idiomatic-examples.md`
