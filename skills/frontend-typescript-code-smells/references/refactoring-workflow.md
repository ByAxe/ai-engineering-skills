# Refactoring Workflow for Frontend TypeScript

## Contents
- Core workflow (universal)
- Workflow A: Refactor a God Component safely
- Workflow B: Fix a render storm without over-memoizing
- Workflow C: Fix stale closures and effect dependency bugs
- Workflow D: Remove `any` and unsafe assertions incrementally
- Workflow E: Untangle async data fetching (races, cancellation, caching)
- Workflow F: Improve module boundaries (adapter, facade, ports)
- When to stop and defer work

---

## Core workflow (universal)

1. **Define success**
   - What must remain identical (UI, behavior, API calls, URL changes)?
   - What must improve (readability, performance, type safety, testability)?

2. **Establish guardrails**
   - Identify tests that cover the path.
   - If tests are missing, create the smallest regression test first.
   - Identify cheap verification steps: typecheck, lint, build.

3. **Detect smells and root causes**
   - Name the smell, point to evidence, and label the risk.
   - Prefer root-cause fixes over symptom patches.

4. **Choose a minimal refactor strategy**
   - Extract pure code first.
   - Stabilize APIs second.
   - Only then introduce new patterns (store changes, new layers).

5. **Apply the patch**
   - Make a diff that a reviewer can follow.

6. **Verify and iterate**
   - Run checks.
   - If something breaks, revert to the last safe checkpoint and try again.

---

## Workflow A: Refactor a God Component safely

Goal: reduce size and complexity without changing behavior.

### Step 0: Map responsibilities
In a single pass, label each block as one of:
- Data fetching
- State management
- Event handling
- Formatting and mapping
- Rendering
- Side effects and subscriptions
- Coordination (routing, analytics)

### Step 1: Extract pure helpers
Extract logic that:
- Has no UI dependencies
- Takes inputs and returns outputs
Examples: formatting, filtering, mapping, validation, calculation.

Outputs:
- `helpers.ts` (pure functions)
- Types for helper inputs and outputs

### Step 2: Extract presentational components
Extract components that:
- Are mostly markup and styling
- Take props and render
- Have minimal internal state

Keep them "dumb" by default:
- No fetching
- No global store access
- No navigation side effects

### Step 3: Extract hooks for stateful logic
Extract logic that:
- Manages state and derived values
- Uses effects, subscriptions, timers
- Coordinates local state transitions

Rules:
- Hook API should be stable and minimal.
- Return stable references when possible (useMemo or useCallback only when needed).

### Step 4: Introduce an adapter boundary (optional)
If the component talks directly to:
- API clients
- Router
- Analytics
- Storage

Add a thin adapter module so UI code depends on an interface, not the implementation.

### Step 5: Verify behavior
- Snapshot tests are not enough.
- Prefer interaction tests and state transition tests.

---

## Workflow B: Fix a render storm without over-memoizing

Goal: reduce render counts and jank with minimal complexity.

### Step 1: Prove the storm exists
- Identify which component re-renders.
- Identify what triggers each re-render.

### Step 2: Classify the cause
Most common causes:
- Prop reference changes (inline objects/functions)
- Context value churn (provider value recreated)
- Derived values recalculated each render
- Global store subscriptions too broad
- Effects that set state on every render

### Step 3: Apply minimal fixes
Prefer in this order:
1. Move inline objects/functions outside render or memoize them.
2. Split component into smaller pieces so only the necessary subtree re-renders.
3. Narrow context value: split contexts or provide stable slices.
4. Use memoization only around expensive computations or expensive subtrees.

### Step 4: Re-measure and stop
If the performance goal is met, stop. Extra memoization is a maintainability smell.

---

## Workflow C: Fix stale closures and effect dependency bugs

Goal: eliminate correctness bugs caused by effects and callbacks reading old values.

### Step 1: Identify which value is stale
Common symptoms:
- UI lags behind state
- Effects run with old props/state
- Timers or subscriptions use outdated handlers
- Race conditions where old response overwrites new state

### Step 2: Choose the right wiring
Options:
- Add missing dependencies and restructure code to satisfy lints.
- Move non-reactive code out of effects (derive values before effect).
- Use stable callbacks that read from refs when appropriate.
- Avoid "tricking" dependencies; restructure instead.

### Step 3: Handle async cancellation
For requests:
- Abort previous requests when starting a new one.
- Use latest-only guards (monotonic request id).
- Ensure state updates apply only to active component.

### Step 4: Add regression coverage
Add a test that reproduces the stale behavior (especially for races).

---

## Workflow D: Remove `any` and unsafe assertions incrementally

Goal: improve type safety without blocking development.

### Step 1: Stop the bleeding
- Prevent new `any` by enabling rules (no-explicit-any) if allowed.
- Keep changes localized if rules cannot be turned on globally.

### Step 2: Convert `any` to `unknown`
- Replace `any` with `unknown` at module boundaries.
- Add narrowing functions:
  - predicate type guards
  - schema validation
  - runtime checks

### Step 3: Replace assertions with modeling
- Prefer discriminated unions over type assertions.
- Prefer optional fields or explicit "loading/error" states over non-null assertions.

### Step 4: Make call sites safer
- Push narrowing to the edges so the core code remains clean.
- Prefer typed adapters for API responses.

---

## Workflow E: Untangle async data fetching

Goal: make data fetching predictable, testable, and resistant to races.

### Step 1: Centralize fetch logic
- Create a single function or hook responsible for fetch, caching, and error state.
- Avoid duplicating fetch code across components.

### Step 2: Model async states explicitly
Prefer explicit union states:
- idle
- loading
- success
- error

### Step 3: Prevent races
- Add cancellation and latest-only semantics.
- Ensure stale requests cannot overwrite the latest state.

### Step 4: Separate concerns
- Presentational components render the states.
- Stateful hook or service drives transitions.

---

## Workflow F: Improve module boundaries

Goal: reduce coupling and make change easier.

Use these patterns:
- Adapter: translate external API shapes into internal domain models.
- Facade: expose a simplified API for a complex subsystem.
- Ports and adapters: define interfaces for side effects; implement them per environment.
- Feature folders: group by user-facing feature, not by file type.

Keep boundaries light. Avoid architecture astronautics.

---

## When to stop and defer work

Stop when:
- The stated goal is met
- The diff is already risky
- You are about to change public APIs without a request

Defer by:
- Listing follow-ups in priority order
- Calling out the next seam to extract
- Explaining what tests or metrics would unlock the next refactor
