---
name: flutter-cleanup-assessor
description: Assesses and refactors Flutter and Dart codebases into idiomatic, maintainable Flutter. Use when the user asks to clean up Flutter code, remove code smells, review or modernize bloc/cubit or clean architecture, reduce rebuilds or jank, improve layering, testing, accessibility, localization, or package hygiene without changing behavior.
license: MIT
metadata:
  author: ByAxe
  version: 1.0.0
  category: software-development
  environment: Flutter and Dart projects. Works best with repository access and ability to run flutter or dart commands for format, analyze, test, and build.
  tags:
    - flutter
    - dart
    - bloc
    - cubit
    - clean-architecture
    - refactoring
    - code-smells
    - performance
    - testing
---

# Flutter Cleanup Assessor

Assess a Flutter codebase after feature work is complete, then refactor it toward idiomatic Dart, maintainable Flutter architecture, predictable state, low-friction testing, and clean long-term evolution.

This skill is for cleanup, reassessment, and structural hardening. It is **not** a feature-generation skill.

## Important

- Preserve behavior first. Favor incremental refactors that keep the UI, navigation, API contracts, and persisted data behavior stable unless the user explicitly wants behavior changes.
- Prefer official Flutter architecture principles over dogma. Use clear UI/data boundaries, unidirectional flow, immutable state, repositories, and thin widgets. Add a separate domain/use-case layer only when complexity clearly justifies it.
- Keep widgets declarative. Rendering code should stay easy to skim, cheap to rebuild, and light on business logic.
- Prefer simple state shapes. Avoid "clever" state machines, layered abstractions, or generic base classes unless they remove more complexity than they add.
- Treat bloc or cubit as one implementation of the business-logic layer, not as permission to move UI concerns into state classes or business-logic components.
- Make refactors measurable. Always include exact verification commands and the expected green path.
- When generated code exists, edit the source of truth, not the generated file.

## Workflow

### Step 1: Establish a Baseline

- Identify project type:
  - Flutter app
  - Flutter package or plugin
  - Multi-package monorepo
- Identify toolchain and conventions:
  - Flutter and Dart versions
  - `analysis_options.yaml`
  - state-management library or mix of libraries
  - routing, DI, code generation, and persistence approach
- Run the narrowest useful baseline:
  - `flutter pub get`
  - `dart format -o none --set-exit-if-changed .`
  - `flutter analyze`
  - `flutter test`
  - `flutter test integration_test` when integration tests exist
  - project-specific build command only when needed to validate the touched surface
- Record current behavior and high-risk workflows:
  - app startup
  - auth
  - list/detail flows
  - form submission
  - offline/cache flows
  - deep links or navigation restoration
  - localization/accessibility-sensitive screens

### Step 2: Inventory Architecture and State Flow

- Map the current structure:
  - feature-first, layer-first, package-per-feature, or mixed
  - where widgets, state, repositories, DTOs, use cases, and platform code live
- Identify the effective source of truth for each important data type.
- Trace one vertical slice end-to-end:
  - widget -> event or action -> business logic -> repository -> data source -> mapped state -> widget
- Note layering violations, duplicated state, and hidden side effects.
- Detect if the codebase is over-abstracted:
  - pass-through use cases
  - generic repository wrappers with no value
  - multiple model types with identical fields and no boundary benefit

### Step 3: Detect Smells

Use the reference pack and classify findings under these groups:

- Architecture and layering: `references/flutter-architecture-principles.md`
- General maintainability principles: `references/maintainability-principles.md`
- Bloc and cubit usage: `references/bloc-and-cubit-guidelines.md`
- Widget and UI smells: `references/widget-ui-smells.md`
- Data layer and error handling: `references/data-layer-and-error-handling.md`
- Async work, isolates, and side effects: `references/async-concurrency-and-side-effects.md`
- Performance and rebuilds: `references/performance-and-rebuilds.md`
- Testing: `references/testing-strategy.md`
- Accessibility, localization, and adaptivity: `references/accessibility-localization-and-adaptivity.md`
- Tooling, lints, and quality gates: `references/tooling-lints-and-quality-gates.md`
- Pubspec and package hygiene: `references/pubspec-and-package-hygiene.md`
- Dart language and API design: `references/dart-language-and-api-design.md`

### Step 4: Choose the Target Shape

Choose the **smallest** architecture that fits the codebase:

- Small or medium feature with straightforward business rules:
  - UI layer + business logic component + repository + data source
- Larger app with multiple coordinated flows and meaningful business rules:
  - add a domain/use-case layer only where it reduces coupling or duplication
- Package or plugin:
  - keep the public API minimal, typed, and stable
- Bloc or cubit:
  - keep state immutable
  - keep side effects out of builders
  - keep Flutter imports out of business logic components
  - avoid bloc-to-bloc sibling dependencies

When in doubt, simplify instead of adding another abstraction layer.

### Step 5: Refactor in Safe Batches

Refactor file-by-file or feature-by-feature:

1. Add or tighten tests around current behavior.
2. Fix one smell family at a time.
3. Re-run format, analyze, and tests.
4. Only then continue to the next family.

Preferred order:

1. correctness and state integrity
2. architecture and boundaries
3. widget readability and rebuild scope
4. async safety and side-effect placement
5. test gaps
6. accessibility/localization hardening
7. performance work backed by evidence
8. dependency and tooling cleanup

### Step 6: Validate and Harden

- Re-run:
  - `dart format -o none --set-exit-if-changed .`
  - `flutter analyze`
  - `flutter test`
  - integration tests or the smallest app build that validates the touched platform surface
- If state-management changes touched rebuild behavior, inspect the affected screens manually.
- If performance was part of the refactor, validate in profile mode on a realistic device.
- If UI structure changed, verify accessibility labels, tap targets, text scaling, and localization output.
- Summarize:
  - what changed
  - why it is more idiomatic Flutter or Dart
  - how to verify it
  - what you deliberately deferred

## High-Signal Smells

### Architecture and Layering

- Widgets call data providers directly.
- Repositories are bypassed for convenience.
- Business logic lives inside widgets or `build()`.
- Every feature has a rigid clean-architecture stack even when most layers are pass-through.
- The same entity exists as UI model, domain model, repository model, DTO, and state payload with no boundary value.
- The same data is owned by multiple blocs, cubits, or widgets.

Use: `references/flutter-architecture-principles.md`

### Bloc and Cubit

- `BlocBuilder` performs navigation, snackbars, dialogs, analytics, or I/O.
- Business-logic components import Flutter.
- One bloc listens directly to another bloc.
- A bloc exposes custom public methods instead of receiving events.
- A cubit exposes public methods that return data instead of only driving state changes.
- A huge state object causes nearly every widget in a screen to rebuild.
- Event and state names are vague or inconsistent.

Use: `references/bloc-and-cubit-guidelines.md`

### Widgets and UI

- Giant screen widgets with 200+ line `build()` methods.
- Helper functions return widgets instead of extracting small widgets with clear inputs.
- `setState()` is called high in the tree for tiny changes.
- Controllers, focus nodes, or subscriptions are not disposed.
- Hard-coded strings, padding, colors, and styles are scattered everywhere.
- Conditional rendering is unreadable or repeated across sibling widgets.

Use: `references/widget-ui-smells.md`

### Data and Errors

- Raw `Map<String, dynamic>` or JSON reaches widgets and state classes.
- Repositories merely forward raw DTOs instead of normalizing them.
- Methods return `null`, `false`, or magic strings for failure.
- Exceptions are caught and ignored.
- `throw e` is used instead of `rethrow`.
- Caching or persistence logic is duplicated across repositories.

Use: `references/data-layer-and-error-handling.md`

### Async and Side Effects

- Network calls start inside `build()`.
- `then` chains make control flow harder to read than `async` or `await`.
- `Completer` is used where a simple `Future` or callback would do.
- Screens race multiple requests and show stale data.
- Heavy parsing or computation runs on the UI isolate and causes jank.
- UI state changes depend on untracked lifecycle timing.

Use: `references/async-concurrency-and-side-effects.md`

### Performance and Rebuilds

- Expensive work happens on every rebuild.
- Parent widgets watch entire bloc state objects when they only need one field.
- Long lists use eager children instead of lazy builders.
- Missing `const` constructors inflate rebuild cost and hide intent.
- Render-heavy effects like clipping, opacity, or offscreen layers are used carelessly.
- Performance fixes are proposed without profile data.

Use: `references/performance-and-rebuilds.md`

### Tests and Quality Gates

- Refactors change structure without characterization tests.
- Widgets are only tested through integration tests.
- Business logic is only tested through widgets.
- Analyzer warnings are ignored.
- Generated code is committed but source files are not verified.
- Dependencies drift because nobody checks outdated packages.

Use: `references/testing-strategy.md`, `references/tooling-lints-and-quality-gates.md`, and `references/pubspec-and-package-hygiene.md`

## Output Contract

When assessing a codebase, respond in this order:

1. **Smells found**
   - smell name
   - evidence
   - risk level
   - likely root cause
2. **Top risks**
   - top 3 to 7 issues ordered by impact
3. **Target architecture decision**
   - what shape the code should move toward
   - what abstractions should stay
   - what abstractions should be removed or collapsed
4. **Refactor plan**
   - 3 to 8 incremental steps
   - safety checks after each step
5. **Concrete file-level changes**
   - specific files or folders to touch
   - what to move, rename, split, or delete
6. **Verification**
   - exact commands
   - manual checks for touched flows
7. **Deferred follow-ups**
   - good ideas that should wait for safety or scope reasons

When refactoring code directly, output:

- what changed
- why it is more idiomatic Flutter or Dart
- how rebuild scope, layering, or testability improved
- how to verify it

## Practical Rules of Thumb

- Prefer feature-oriented boundaries over giant global `widgets`, `utils`, and `services` folders.
- Prefer high cohesion and low coupling: files that change together should live together, and sibling features should not reach into each other's internals.
- Prefer one clear source of truth per concern.
- Prefer repositories that return typed models, not transport-level maps.
- Prefer immutable state and explicit state transitions.
- Prefer `BlocListener` or dedicated effect handling for one-off side effects.
- Prefer small extracted widgets over helper methods that close over parent state.
- Prefer `async` or `await` over nested futures.
- Prefer `const`, lazy builders, and scoped rebuilds before more advanced optimization.
- Prefer lint and test automation over relying on memory.

## Reference Navigation

- Architecture principles: `references/flutter-architecture-principles.md`
- Maintainability principles: `references/maintainability-principles.md`
- Bloc and cubit rules: `references/bloc-and-cubit-guidelines.md`
- Widget-level cleanup guide: `references/widget-ui-smells.md`
- Data, mapping, and error handling: `references/data-layer-and-error-handling.md`
- Async work and side effects: `references/async-concurrency-and-side-effects.md`
- Performance and rebuild scope: `references/performance-and-rebuilds.md`
- Testing strategy: `references/testing-strategy.md`
- Accessibility, localization, adaptivity: `references/accessibility-localization-and-adaptivity.md`
- Tooling and lints: `references/tooling-lints-and-quality-gates.md`
- Dependency hygiene: `references/pubspec-and-package-hygiene.md`
- Dart language and API design: `references/dart-language-and-api-design.md`
- Refactoring playbooks: `references/refactoring-playbook.md`
- Checklists: `references/assessment-checklists.md`
- Idiomatic examples: `references/idiomatic-examples.md`
- Assessment template: `assets/flutter-cleanup-assessment-template.md`
- Sample analyzer config: `assets/analysis_options.flutter-cleanup.sample.yaml`
- Source index: `references/sources.md`

## Examples

### Example 1: Full repo assessment

User: "Assess this Flutter repo that grew fast and now feels messy."

Action:
- Run Steps 1 through 6.
- Classify smells by architecture, widget/UI, bloc/cubit, async, data, performance, tests, accessibility, and dependency hygiene.
- Choose the smallest viable target architecture.
- Produce a staged refactor plan and exact verification commands.

### Example 2: Bloc cleanup

User: "This screen uses bloc but rebuilds too much and navigation is flaky."

Action:
- Audit builders, listeners, selectors, state shape, and rebuild boundaries.
- Move one-off effects out of `BlocBuilder`.
- Scope rebuilds with `BlocSelector`, extracted widgets, or local builders.
- Tighten tests around the touched flows.

### Example 3: Clean-architecture simplification

User: "We added use cases everywhere and now it feels over-engineered."

Action:
- Trace vertical slices.
- Remove pass-through use cases and wrappers that add no decision-making value.
- Keep the domain layer only where business rules or cross-feature reuse justify it.
- Preserve repositories and typed boundaries.

### Example 4: Data cleanup after rapid feature work

User: "The feature works but raw JSON leaks into the UI."

Action:
- Introduce typed DTOs, repository mapping, and typed state.
- Remove transport shapes from widgets and blocs.
- Add parsing, mapping, and error tests.

## Troubleshooting

### The repo mixes multiple state-management approaches

Do not rewrite the whole app for consistency alone. First clean the touched feature and define boundaries. Standardize only when the payoff is obvious and the migration path is safe.

### The repo already uses clean architecture

Keep what pays rent. Collapse pass-through abstractions. A "clean" folder tree that obscures flow is not an improvement.

### Generated files dominate analyzer output

Exclude generated files from manual cleanup and targeted lint noise where appropriate, but fix the source annotations or source models that generate the bad output.

### Performance complaints are vague

Do not blindly add memoization or caching. First identify rebuild scope, expensive work in `build()`, and obvious list/layout issues. Use profile-based evidence before deeper optimization.

### Tests are weak

Add characterization tests around the risky flows before restructuring. Refactor after the green baseline exists.

### The request only includes snippets

Assess the snippet locally, name the missing context, state your assumptions once, and still provide the smallest safe refactor plus verification guidance.

## Trigger Test Suite

Should trigger:

- "Clean up this Flutter codebase"
- "Assess Flutter code smells"
- "Refactor this bloc architecture"
- "Make this Dart and Flutter code idiomatic"
- "Reassess this feature for Flutter best practices"
- "Reduce rebuilds and clean architecture issues in this Flutter app"

Should not trigger:

- "Create a new Flutter feature from scratch"
- "Design the UI in Figma"
- "Help me with Java backend refactoring"
- "Write pure Python scripts"
