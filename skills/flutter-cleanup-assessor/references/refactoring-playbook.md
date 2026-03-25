# Refactoring Playbook

Use this file when you have identified a smell and need a staged, low-risk way to fix it.

## Playbook 1: Giant screen widget

### Symptoms

- 200 to 600 line `build()` method
- mixed layout, business logic, and side effects
- hard to test specific branches

### Refactor steps

1. Add a widget test for the key render branches.
2. Extract pure visual sections into small widgets with narrow inputs.
3. Move business logic or derived state preparation into bloc, cubit, or a view-specific mapper.
4. Add `const` and narrower rebuild boundaries where natural.
5. Re-run format, analyze, tests.

### Verify

- loading, empty, success, and failure UI still render correctly
- touched widgets rebuild only when relevant inputs change

## Playbook 2: Side effects in `BlocBuilder`

### Symptoms

- navigation in builder
- snackbars in builder
- dialogs in builder

### Refactor steps

1. Add a widget test or focused integration test for the effect.
2. Move one-off effects to `BlocListener` or a dedicated effect handler.
3. Keep `BlocBuilder` pure.
4. Add `listenWhen` if repeated effects are possible.

### Verify

- effect still fires exactly when intended
- builder remains pure
- no duplicate navigation or duplicate snackbars

## Playbook 3: Bloc depends on another bloc

### Symptoms

- stream subscription to sibling bloc
- constructor takes another bloc
- hidden coupling between features

### Refactor steps

1. Identify the actual shared concern.
2. Move the coordination either:
   - up to the UI layer via `BlocListener`, or
   - down to a shared repository stream
3. Remove direct sibling dependency.
4. Add tests around the resulting flow.

### Verify

- feature still responds correctly to upstream changes
- blocs are independently testable

## Playbook 4: Raw maps or DTOs leak into the UI

### Symptoms

- `Map<String, dynamic>` in state
- widgets index into transport fields
- repository returns DTOs directly

### Refactor steps

1. Add mapping tests.
2. Introduce DTO parsing and app-facing models.
3. Make repository return typed models.
4. Update state and UI to consume typed data.
5. Re-run tests.

### Verify

- UI no longer depends on transport keys
- mapping edge cases are covered

## Playbook 5: Over-engineered clean architecture

### Symptoms

- pass-through use cases
- multiple identical model layers
- navigating the feature is harder than understanding it

### Refactor steps

1. Trace one feature vertically.
2. Mark classes that add no policy, no mapping, and no reuse value.
3. Collapse pass-through layers.
4. Keep only the abstractions that isolate real decisions or boundaries.
5. Update tests and imports.

### Verify

- fewer files are needed to understand the feature
- behavior and public API remain stable

## Playbook 6: Broad rebuilds

### Symptoms

- entire page rebuilds for tiny state changes
- large widget trees use root-level `watch`
- performance issue reports mention typing lag or scroll hitching

### Refactor steps

1. Identify the exact state fields each subtree needs.
2. Extract widgets or add `BlocSelector`.
3. Move expensive work out of `build()`.
4. Use lazy list builders and `const` where obvious.
5. Profile if performance is a key concern.

### Verify

- touched widgets rebuild more narrowly
- interaction remains smooth on realistic hardware

## Playbook 7: Async race or stale response bug

### Symptoms

- fast repeated actions show stale results
- later requests are overwritten by earlier completions
- UI status flickers unexpectedly

### Refactor steps

1. Add a unit test that simulates out-of-order completion if feasible.
2. Introduce request identity, cancellation, or guarded emission.
3. Keep status transitions explicit.
4. Separate render state from one-off effects.

### Verify

- stale responses do not overwrite newer intent
- loading and error states still behave correctly

## Playbook 8: Weak tests before a risky cleanup

### Symptoms

- little or no coverage around the touched area
- refactor confidence depends on manual clicking

### Refactor steps

1. Add characterization tests first.
2. Refactor one smell family.
3. Re-run all relevant checks.
4. Only then move to the next structural change.

### Verify

- baseline behavior remains covered
- each batch has a clear green validation path

## Playbook 9: Dependency sprawl

### Symptoms

- many overlapping packages
- old experiments still in `pubspec.yaml`
- nobody knows why a package exists

### Refactor steps

1. Run `flutter pub outdated`.
2. Inventory package purpose and actual usage.
3. Remove clearly unused packages first.
4. Collapse overlapping packages only where the migration is safe.
5. Re-run analyzer, tests, and the touched app flow.

### Verify

- lockfile and build still resolve cleanly
- no package removal breaks runtime behavior

## Playbook 10: Accessibility or localization debt

### Symptoms

- hard-coded strings
- unlabeled controls
- overflow under text scale

### Refactor steps

1. Identify touched user-facing strings and controls.
2. Move strings to localization.
3. Add semantic labels and resilient layout where needed.
4. Add or update widget tests for the touched cases.

### Verify

- layout survives larger text
- controls remain understandable and tappable
- localized messages render correctly

See also:

- `references/assessment-checklists.md`
- `references/idiomatic-examples.md`
