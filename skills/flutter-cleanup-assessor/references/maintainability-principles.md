# Maintainability Principles for Flutter and Dart

Use this file when the user wants cleanup guidance framed through SOLID, DRY, KISS, clean code, cohesion, and coupling.

These principles matter most when they improve readability, safety, and evolution. They are not a license to add ceremony.

## Single Responsibility

A class, widget, cubit, bloc, repository, or helper should have one clear reason to change.

### Good examples

- a widget renders one section of a screen
- a cubit owns one feature's state transitions
- a repository owns one data concern
- a data source talks to one transport or storage mechanism

### Smells

- one widget renders a full screen, owns async work, formats values, and shows side effects
- one bloc owns several unrelated feature flows
- one repository talks to many unrelated endpoints and caches unrelated entities
- one helper class becomes the dumping ground for "shared logic"

## Open for extension, closed for modification

Prefer designs where adding a new state, screen section, or mapping path does not require fragile edits across many unrelated files.

In Flutter this often means:

- composing widgets instead of growing one god widget
- modeling state clearly instead of adding more boolean flags
- introducing typed variants where invalid combinations are becoming common

Do not over-engineer extension points "just in case."

## Liskov and substitutability

If you define interfaces or abstractions, keep their contracts honest.

### Smells

- repository interfaces that promise one thing but implementations quietly do more
- fake implementations that behave very differently from production ones
- public APIs that return nullable values, exceptions, or magic strings depending on the code path

A narrower, more truthful interface is better than a highly abstract but inconsistent one.

## Interface segregation

Prefer small, purpose-built interfaces over giant service surfaces.

### Better

```dart
abstract interface class ProfileRepository {
  Future<UserProfile> loadProfile();
  Future<void> updateProfile(ProfileDraft draft);
}
```

### Worse

```dart
abstract interface class AppRepository {
  Future<dynamic> getStuff(String type);
  Future<void> saveStuff(String type, dynamic payload);
  Stream<dynamic> watchStuff(String type);
}
```

## Dependency inversion, used pragmatically

Depending on abstractions can reduce coupling, but abstract only where it buys something real:

- test seam
- platform seam
- cross-feature reuse
- replacement of infrastructure details

Do **not** create interfaces for every class by reflex.

## DRY without over-generalizing

Avoid duplicating **knowledge**, not every repeated line of syntax.

### Bad DRY

A generic "base screen" or "base repository" adds indirection but hides behavior.

### Good DRY

- one mapping helper shared by several repositories because the policy is identical
- one design token or theme extension for repeated spacing or colors
- one retry view used consistently across features

If two pieces of code look similar but are likely to evolve differently, keep them separate.

## KISS

Choose the smallest design that is correct, readable, and extensible enough.

### Good KISS moves

- collapse pass-through use cases
- remove generic base classes that save little
- keep state shape explicit
- use a plain cubit for straightforward state flow instead of building event hierarchies with no payoff

### KISS is not "make it simplistic"

Do not remove structure that protects important boundaries, business rules, or tests.

## High cohesion, low coupling

### High cohesion

Files that change together should live together.

Prefer feature-first organization when the app grows:

```text
lib/
  features/
    checkout/
    profile/
  core/
```

### Low coupling

- widgets should not know repository internals
- blocs should not know sibling blocs
- repositories should not know Flutter
- UI should not know transport-level details

## Clean code in Flutter terms

Prefer:

- intention-revealing names
- short methods that stay at one abstraction level
- explicit state transitions
- guard clauses over deep nesting
- typed boundaries instead of `dynamic`
- deleting dead code instead of preserving every experiment forever

### Guard clause example

```dart
Future<void> submit() async {
  if (!state.isValid) {
    emit(state.copyWith(errorMessage: 'Please correct the form'));
    return;
  }

  emit(state.copyWith(status: FormStatus.submitting));

  try {
    await _repository.submit(state.form);
    emit(state.copyWith(status: FormStatus.success));
  } catch (error, stackTrace) {
    addError(error, stackTrace);
    emit(state.copyWith(
      status: FormStatus.failure,
      errorMessage: 'Submission failed',
    ));
  }
}
```

## Smell mapping

- giant widgets -> low cohesion
- global mutable shared services -> high coupling
- many boolean flags for state -> poor model clarity
- base classes and generic abstractions everywhere -> misplaced DRY
- copied transport parsing in several widgets -> real duplication worth removing
- one "utils.dart" for the whole app -> poor responsibility boundaries

## Review checklist

- Does each file have a clear reason to change?
- Are abstractions earning their keep?
- Is duplication real knowledge duplication or just superficial similarity?
- Can the feature evolve without touching many unrelated files?
- Is the code simpler after the refactor, not just different?

See also:

- `references/flutter-architecture-principles.md`
- `references/refactoring-playbook.md`
- `references/widget-ui-smells.md`
