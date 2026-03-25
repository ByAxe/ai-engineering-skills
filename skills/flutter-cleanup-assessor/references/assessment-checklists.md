# Assessment Checklists

Copy the relevant checklist into the response and mark progress as you work.

## Baseline checklist

- [ ] Identify Flutter app, package, plugin, or monorepo structure
- [ ] Note Flutter and Dart versions if available
- [ ] Inspect `analysis_options.yaml`
- [ ] Identify routing, DI, persistence, codegen, and state libraries
- [ ] Run or specify baseline commands
- [ ] Record high-risk user flows

## Architecture checklist

- [ ] Clear UI and data boundaries
- [ ] One source of truth per major concern
- [ ] Repositories own data access complexity
- [ ] Widgets are not calling data providers directly
- [ ] Domain/use-case layer exists only where it pays rent
- [ ] Folder structure matches change boundaries

## Bloc and cubit checklist

- [ ] Builders are pure
- [ ] Listeners handle one-off effects
- [ ] Business logic avoids Flutter imports
- [ ] No sibling bloc dependencies
- [ ] Rebuild scope is intentional
- [ ] State is immutable
- [ ] Event and state naming is consistent

## Widget checklist

- [ ] `build()` methods are readable
- [ ] Small widgets extracted where useful
- [ ] Local UI state is local
- [ ] Controllers and subscriptions are disposed
- [ ] Strings are localizable
- [ ] Styling is consistent and theme-aware

## Data checklist

- [ ] DTOs are contained at boundaries
- [ ] Repositories return typed models
- [ ] Raw maps do not leak into widgets or state
- [ ] Error handling is consistent
- [ ] No swallowed exceptions
- [ ] Cache and persistence logic is centralized where appropriate

## Async checklist

- [ ] No side effects in `build()`
- [ ] `async` and `await` used where clearer
- [ ] No unnecessary `Completer`
- [ ] Race-prone flows are guarded
- [ ] Heavy work is not causing UI jank
- [ ] Lifecycle-sensitive work is safe

## Performance checklist

- [ ] Expensive work removed from `build()`
- [ ] Large lists use lazy builders
- [ ] `const` added where natural
- [ ] Rebuilds are scoped
- [ ] Render-heavy effects are intentional
- [ ] Performance claims are backed by evidence

## Testing checklist

- [ ] Characterization tests added before large refactors
- [ ] Business logic has unit coverage
- [ ] Important screens have widget coverage
- [ ] Critical flows have integration coverage where appropriate
- [ ] Mapping and parsing have focused tests
- [ ] Verification commands are explicit

## Accessibility and localization checklist

- [ ] User-facing strings are localizable
- [ ] Important controls have clear labels
- [ ] Tap targets are comfortably sized
- [ ] Text scale does not break the touched UI
- [ ] Layout tolerates longer strings
- [ ] Touched flows are tested for accessibility-sensitive regressions

## Dependency and tooling checklist

- [ ] `flutter_lints` or a deliberate alternative exists
- [ ] analyzer output is clean or intentionally triaged
- [ ] `bloc_lint` considered when bloc is central
- [ ] generated code is handled deliberately
- [ ] outdated dependencies are reviewed
- [ ] CI or local commands are easy to run

## Final response checklist

- [ ] Smells found
- [ ] Top risks
- [ ] Target architecture decision
- [ ] Refactor plan
- [ ] File-level changes
- [ ] Verification
- [ ] Deferred follow-ups
