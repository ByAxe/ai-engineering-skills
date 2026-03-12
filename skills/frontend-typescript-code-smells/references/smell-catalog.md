# Frontend TypeScript Code Smell Catalog

This catalog is framework-agnostic by default, with notes for React, Angular, and Vue when relevant.

## Contents
- How to use this catalog
- Smell severity and prioritization
- Category 1: Component and module boundaries
- Category 2: State and data flow
- Category 3: Effects, lifecycle, subscriptions
- Category 4: Performance and rendering
- Category 5: TypeScript typing and safety
- Category 6: Async and data fetching
- Category 7: Styling and UI composition
- Category 8: Accessibility and semantics
- Category 9: Testing and maintainability
- Category 10: Security and trust boundaries
- Common refactoring moves (index)

---

## How to use this catalog

1. Start with the user's goal (bug fix, maintainability, performance, type safety).
2. Identify the smell(s) with evidence.
3. Choose the smallest refactor that removes the smell.
4. Verify with lint, typecheck, tests, and build.

For deeper guidance, jump to the referenced files listed in each smell.

---

## Smell severity and prioritization

Prioritize smells in this order:
1. Correctness and data integrity
2. Security
3. Performance cliffs (jank, leaks)
4. Maintainability and architecture
5. Type safety and developer experience
6. Accessibility regressions

---

# Category 1: Component and module boundaries

## B-01 God component

**Looks like**
- A single component handles data fetching, state, formatting, and rendering.
- Many nested conditionals and handlers.

**Why it hurts**
- Hard to reason about, hard to test, high regression risk.

**Fix**
- Extract pure helpers, then presentational components, then hooks.
- See: `references/refactoring-workflow.md`

---

## B-02 Mixed responsibilities (UI plus domain logic)

**Looks like**
- Business rules and mapping logic live inside UI components.

**Why it hurts**
- Domain logic becomes untestable and duplicated across UI.

**Fix**
- Extract domain logic to pure functions or a domain module.
- Keep components focused on wiring and rendering.

---

## B-03 Prop explosion

**Looks like**
- Component takes 15 to 30 props, many related.
- Many boolean flags or optional props.

**Why it hurts**
- Hard to understand the component API; easy to break call sites.

**Fix**
- Group props into typed objects.
- Replace boolean flags with options objects or mode unions.
- See: `references/typescript-type-smells.md` (boolean trap)

---

## B-04 Deeply nested conditional rendering

**Looks like**
- Nested ternaries and deeply nested condition blocks in TSX.

**Why it hurts**
- Readability suffers; small changes introduce bugs.

**Fix**
- Extract rendering branches into named components or functions.
- Prefer early returns or a render switch based on a discriminated union.

---

## B-05 Duplicate UI patterns with subtle differences

**Looks like**
- Multiple components implement "the same" widget differently.

**Why it hurts**
- Inconsistent UX and repeated bug fixes.

**Fix**
- Extract a shared component with a stable API.
- Keep customization via composition rather than flags.

---

## B-06 Tight coupling to router or global singletons

**Looks like**
- Components import router, storage, analytics directly.
- Hard to test or reuse.

**Fix**
- Introduce adapter modules and pass dependencies through a boundary.
- Consider a thin "container" component that owns integrations.

---

## B-07 Implicit contracts hidden in naming

**Looks like**
- Prop names inconsistent: onSubmit vs handleSubmit vs submit.
- Event payload shapes vary per component.

**Fix**
- Standardize naming conventions and event payload types.
- Use shared types for common callbacks.

---

## B-08 Cross-feature imports and circular dependencies

**Looks like**
- Feature A imports internals from Feature B.
- Circular dependency warnings or runtime weirdness.

**Fix**
- Introduce a shared module or invert dependency direction.
- Add clear public entry points per feature.

---

# Category 2: State and data flow

## S-01 Duplicate sources of truth

**Looks like**
- Same value stored in local state and global store.
- Same data stored in two different stores.

**Why it hurts**
- Drift causes correctness bugs.

**Fix**
- Choose one source of truth and derive the rest.
- See: `references/react-smells.md` (duplicate state)

---

## S-02 Derived state stored instead of derived

**Looks like**
- Storing computed values in state, updated by effects.

**Fix**
- Compute during render; memoize only if expensive.
- See: `references/react-smells.md` (derived state)

---

## S-03 Mutating state

**Looks like**
- State arrays or objects modified in place.
- UI does not rerender reliably.

**Fix**
- Use immutable updates.
- Add readonly types where appropriate.
- See: `references/typescript-type-smells.md` (readonly)

---

## S-04 Global state used for local UI concerns

**Looks like**
- Modal open state or form field values in global store.

**Why it hurts**
- Unnecessary coupling and rerender scope increases.

**Fix**
- Keep ephemeral UI state local.
- Keep global state for shared and persistent state.

---

## S-05 Local state used for shared app concerns

**Looks like**
- User identity, permissions, or app-wide settings stored in random components.

**Fix**
- Move to a shared store or context with a stable boundary.

---

## S-06 State updates during render

**Looks like**
- setState called conditionally in render path.

**Fix**
- Move updates to handlers or effects.
- See: `references/react-smells.md` (setState during render)

---

## S-07 Non-idempotent reducers

**Looks like**
- Reducer performs side effects or depends on external mutable values.

**Fix**
- Keep reducers pure; move side effects elsewhere.
- See: `references/async-and-data-smells.md` (side effects in reducers)

---

## S-08 Monolithic context values

**Looks like**
- One huge context provides many unrelated values.

**Fix**
- Split context by volatility and responsibility.
- See: `references/react-smells.md` (context churn)

---

## S-09 Form state inconsistencies

**Looks like**
- Mixed controlled and uncontrolled inputs.
- Validation logic duplicated.

**Fix**
- Choose one approach per form.
- Extract validation rules to a shared module.

---

# Category 3: Effects, lifecycle, subscriptions

## E-01 Missing cleanup for subscriptions

**Looks like**
- Subscriptions or event listeners added without cleanup.

**Fix**
- Add cleanup; ensure handler reference is stable.
- See: `references/react-smells.md` and MDN removeEventListener.

---

## E-02 Stale closures in effects or callbacks

**Looks like**
- Effect uses old props/state.

**Fix**
- Fix dependencies and restructure.
- See: `references/react-smells.md`

---

## E-03 Effects used as event handlers

**Looks like**
- Using effects to respond to user input instead of handlers.

**Fix**
- Use event handlers for user events; effects for external synchronization.

---

## E-04 Infinite effect loops

**Looks like**
- Effect updates state on every run.

**Fix**
- Ensure effect has correct deps and guards.
- See: `references/react-smells.md`

---

## E-05 Timers not cleaned up

**Looks like**
- setInterval/setTimeout created but not cleared.

**Fix**
- Clear timers in cleanup; avoid creating timers repeatedly.

---

## E-06 Observables or streams without unsubscribe

**Looks like**
- Subscription created but not disposed.

**Fix**
- Unsubscribe on cleanup; use takeUntil patterns if used in project.

---

# Category 4: Performance and rendering

## P-01 Render storms

**Looks like**
- Excessive rerenders.

**Fix**
- Identify triggers, stabilize props, split boundaries.
- See: `references/performance-and-rendering.md`

---

## P-02 Expensive work in render

**Looks like**
- Sorting, filtering, parsing in render.

**Fix**
- Extract helpers; memoize expensive computations.

---

## P-03 Inline objects/functions passed as props

**Fix**
- Hoist or memoize where needed.
- See: `references/react-smells.md`

---

## P-04 Over-memoization

**Looks like**
- Memo hooks everywhere, complex deps.

**Fix**
- Remove unnecessary memoization; split components instead.
- See: `references/react-smells.md`

---

## P-05 Large lists without virtualization

**Fix**
- Virtualize; render fewer nodes.

---

## P-06 Unstable keys in lists

**Looks like**
- Index as key, random keys.

**Fix**
- Use stable ids.
- See: `references/react-smells.md` and React list docs.

---

## P-07 Layout thrash and forced reflow

**Fix**
- Batch reads/writes; avoid sync layout in loops.
- See: `references/performance-and-rendering.md`

---

## P-08 Unthrottled high-frequency events

**Fix**
- Throttle/debounce; use passive listeners where appropriate.

---

# Category 5: TypeScript typing and safety

## TS-01 `any` leakage

**Fix**
- Replace with unknown and narrow.
- See: `references/typescript-type-smells.md`

---

## TS-02 Unsafe type assertions

**Fix**
- Replace with runtime checks or better modeling.

---

## TS-03 Non-null assertion overuse

**Fix**
- Replace with modeling or runtime checks.
- See: `references/typescript-type-smells.md`

---

## TS-04 Inconsistent nullability

**Fix**
- Choose one representation and apply consistently.

---

## TS-05 Boolean trap and flag arguments

**Fix**
- Options objects or literal union modes.

---

## TS-06 Stringly typed domains

**Fix**
- Branded ids or domain-specific types.

---

## TS-07 God interfaces with optional fields

**Fix**
- Discriminated unions and explicit states.

---

## TS-08 Overly complex types

**Fix**
- Replace with named types and runtime mapping where appropriate.

---

# Category 6: Async and data fetching

## A-01 Fetch in render path

**Fix**
- Move to effect, hook, loader.

---

## A-02 Duplicated fetching logic

**Fix**
- Centralize in hook/service; provide typed domain output.

---

## A-03 Race conditions and out-of-order responses

**Fix**
- Cancellation and latest-only semantics.
- See: `references/async-and-data-smells.md`

---

## A-04 Missing loading and error modeling

**Fix**
- Explicit async states.
- See: `references/async-and-data-smells.md`

---

## A-05 Silent failures

**Fix**
- Surface errors; add error boundaries where needed.

---

# Category 7: Styling and UI composition

## UI-01 Mixed styling paradigms in one feature

**Looks like**
- Mixing CSS modules, inline styles, and CSS-in-JS in one component tree.

**Fix**
- Standardize within a feature boundary.

See: `references/styling-and-css-smells.md`

---

## UI-02 Inline style objects recreated frequently

**Fix**
- Hoist constants; avoid new objects per render when not necessary.

---

## UI-03 Specificity wars and global CSS leakage

**Fix**
- Prefer scoped styles, CSS modules, or a design system convention.

---

## UI-04 Magic class names and inconsistent naming

**Fix**
- Standardize naming; use typed variants if using a component library.

---

# Category 8: Accessibility and semantics

## AX-01 Non-semantic interactive elements

**Fix**
- Use button/a/input; ensure keyboard and labels.
- See: `references/accessibility-and-ux-smells.md`

---

## AX-02 Missing accessible names

**Fix**
- Labels and aria-label where needed.

---

## AX-03 Focus management bugs

**Fix**
- Manage focus for dialogs, menus.

---

# Category 9: Testing and maintainability

## T-01 Snapshot test overuse

**Fix**
- Prefer behavior tests.
- See: `references/testing-and-maintainability.md`

---

## T-02 Testing implementation details

**Fix**
- Test user-visible output and events.

---

## T-03 Flaky async tests

**Fix**
- Deterministic async; avoid sleeps.

---

## T-04 Missing contract tests for adapters

**Fix**
- Add boundary tests for mappers and adapters.

---

# Category 10: Security and trust boundaries

## SEC-01 Unsafe HTML injection

**Looks like**
- Setting innerHTML/dangerouslySetInnerHTML with unsanitized data.

**Why it hurts**
- XSS risk.

**Fix**
- Avoid raw HTML or sanitize using project-approved sanitizer.
- Prefer rendering text nodes.

See: `references/security-smells.md`

---

## SEC-02 Leaking secrets into client bundles

**Looks like**
- Hardcoded keys or secrets in frontend code.

**Fix**
- Move to server; ensure env variables are safe for client exposure.

See: `references/security-smells.md`

---

## SEC-03 Eval and dynamic code execution

**Fix**
- Avoid eval/new Function; use safe parsing.

---

# Common refactoring moves (index)

- Extract pure helper
- Extract presentational component
- Extract custom hook
- Introduce adapter or mapper
- Split context or narrow subscriptions
- Add cancellation and latest-only semantics
- Add regression tests for edge cases

See: `references/refactoring-workflow.md` and `references/checklists.md`
