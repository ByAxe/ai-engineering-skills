# Checklists and Templates for Frontend TypeScript Refactoring

## Contents
- Refactor safety checklist
- Smell triage rubric
- Patch template
- Performance triage checklist
- Async correctness checklist
- Type-safety upgrade checklist
- Accessibility checklist
- Review checklist for PRs

---

## Refactor safety checklist

Use this when changing production UI code.

- [ ] Identify the **observable behavior** that must remain the same (UI output, network calls, analytics, side effects).
- [ ] Confirm where state lives (component state, global store, URL, cache).
- [ ] Confirm where side effects live (effects, subscriptions, services).
- [ ] Make the smallest change that improves one dimension (correctness, maintainability, performance).
- [ ] Keep the diff reviewable: extraction first, then behavior changes.
- [ ] Run lint, typecheck, tests, build.
- [ ] If performance-related: capture before/after measurements (render count, long tasks, interaction timings).
- [ ] Document intentional non-changes (what was intentionally not refactored yet).

---

## Smell triage rubric

Score each smell from 0 to 3 in each dimension.

- Correctness risk
  - 0: cosmetic
  - 1: minor bug potential
  - 2: likely bug in edge cases
  - 3: active bug or frequent incidents
- Performance risk
  - 0: negligible
  - 1: small overhead
  - 2: noticeable in common flows
  - 3: cliff (render storm, jank, memory leak)
- Maintainability risk
  - 0: local and readable
  - 1: some friction
  - 2: high cognitive load
  - 3: blocks change; frequent regressions
- Security or a11y risk (optional)
  - 0: none
  - 1: potential issue
  - 2: likely issue
  - 3: confirmed issue

Prioritize the highest combined scores, but fix correctness and security first.

---

## Patch template

Use this structure for refactor output.

1. Smells found
   - Smell: ...
   - Evidence: ...
   - Risk: ...
2. Refactor plan
   - Step 1 (safe extraction): ...
   - Step 2 (behavior-preserving rewrite): ...
3. Patch
   - File: path/to/file.ts
   - File: path/to/component.tsx
4. Verification
   - Commands
   - Expected outputs
5. Follow-ups (optional)
   - Safe next refactors
   - Deferred improvements

---

## Performance triage checklist

Use when the user reports sluggish UI or re-render storms.

- [ ] Identify which interaction is slow (typing, scrolling, opening modal, navigation).
- [ ] Determine whether it is:
  - [ ] Too many renders
  - [ ] Expensive render work
  - [ ] Expensive effects
  - [ ] Layout thrash
  - [ ] Large bundle or slow hydration
  - [ ] Memory leak
- [ ] Find the top offenders:
  - React: Profiler flamegraph, "why did this render" tools, console counters
  - Browser: Performance panel, long tasks, forced reflow warnings
- [ ] Fix by narrowing the cause:
  - [ ] Stabilize props references
  - [ ] Split component boundaries
  - [ ] Memoize only the expensive path
  - [ ] Virtualize large lists
  - [ ] Reduce context churn
  - [ ] Defer or schedule work
- [ ] Re-measure after changes.

---

## Async correctness checklist

Use when UI shows stale data, wrong results, or flickers.

- [ ] Identify the data source and caching layer.
- [ ] Confirm whether the issue is:
  - [ ] Race between overlapping requests
  - [ ] Stale closure reading old state
  - [ ] Missing cancellation or cleanup
  - [ ] Out-of-order updates applied last
  - [ ] Cache invalidation bug
- [ ] Ensure the code has:
  - [ ] Abort or cancellation support
  - [ ] A monotonic request id or latest-only strategy
  - [ ] Correct dependency wiring (effects and callbacks)
  - [ ] Error handling and retries where appropriate
- [ ] Add a regression test for the failure mode.

---

## Type-safety upgrade checklist

Use when removing `any` or strengthening types.

- [ ] Turn unsafe `any` into `unknown` and add narrowing.
- [ ] Prefer domain types: branded ids, literal unions, discriminated unions.
- [ ] Avoid non-null assertions; prefer runtime checks or better modeling.
- [ ] Replace broad types with exact ones (prefer readonly, exact field sets).
- [ ] Ensure public APIs remain stable unless the user asked for breaking changes.
- [ ] Verify strict null checks paths and error states.

---

## Accessibility checklist (fast)

Use when refactoring UI elements or building new components.

- [ ] Use semantic elements when possible (button, a, input, label).
- [ ] Ensure all inputs have labels.
- [ ] Ensure interactive elements are keyboard accessible.
- [ ] Manage focus for dialogs and menus.
- [ ] Provide text alternatives for icons and images.
- [ ] Validate color contrast and focus styles.

---

## PR review checklist for refactors

- [ ] Diff is readable: extraction separated from behavior changes.
- [ ] Types got stricter, not looser.
- [ ] New abstractions reduce duplication and clarify boundaries.
- [ ] Performance changes are justified and measured.
- [ ] Cleanup and cancellation exist for subscriptions and event listeners.
- [ ] Tests cover the risky parts.
