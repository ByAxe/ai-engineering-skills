# React and TSX Code Smells (Hooks, Rendering, State)

## Contents
- R-01 Missing dependencies and stale closures
- R-02 Fighting the exhaustive-deps lint rule instead of restructuring
- R-03 useEffect used for derived state
- R-04 Effects that create render loops
- R-05 Async effects without cancellation
- R-06 Subscriptions and event listeners without cleanup
- R-07 Inline objects and functions passed as props
- R-08 Overly broad Context values causing rerenders
- R-09 Prop drilling and unstable component boundaries
- R-10 Index as key and unstable keys in lists
- R-11 Excessive memoization as cargo cult
- R-12 setState during render
- R-13 Duplicate state and sources of truth
- R-14 Conditional hooks and rules-of-hooks violations
- R-15 UI state mixed with server/cache state
- R-16 Missing error boundaries and brittle suspense usage
- Sources

---

## R-01 Missing dependencies and stale closures

### Symptoms
- Effects or callbacks read old values.
- Timers and subscriptions keep using the initial state.
- Bugs appear only after some interaction or navigation.

### Why it matters
- Correctness bugs are worse than maintainability smells.
- Missing dependencies often indicate hidden coupling between render and effect lifecycles.

### Refactor strategy
- Prefer to satisfy the dependency lint rule by restructuring:
  - Move derived values outside the effect.
  - Extract functions inside the effect or memoize them properly.
  - Use refs only for truly non-reactive values, not as a general escape hatch.

React docs discuss why the dependency array exists and how the lint rule surfaces common bugs:
- https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps

---

## R-02 Fighting exhaustive-deps instead of restructuring

### Symptoms
- Disabling the lint rule.
- Adding comments like "ignore deps".
- Manually removing dependencies to control effect timing.

### Why it matters
- Often creates stale closure bugs and makes refactors dangerous.

### Refactor strategy
- Treat the lint rule as a design feedback loop.
- Separate concerns:
  - reactive values: belong in deps
  - non-reactive logic: move to helpers or stable event callbacks
- If the effect needs "latest state" but should not rerun, restructure rather than trick deps.

---

## R-03 useEffect used for derived state

### Symptoms
- State computed from props or other state inside an effect, then stored.
- Flicker or extra renders.

### Why it matters
- Derived state in effects tends to create ordering bugs and extra renders.

### Refactor strategy
- Derive during render:
  - compute value directly
  - memoize only if expensive
- Store only the minimal source-of-truth state.

---

## R-04 Effects that create render loops

### Symptoms
- Effect updates state, which triggers rerender, which triggers effect again.
- Rapid state changes, CPU spikes, infinite loops.

### Refactor strategy
- Ensure the effect is conditional and driven by a stable trigger.
- Move state updates out of effect when they can be derived in render.
- If the effect synchronizes with an external system, ensure it updates only when inputs change.

---

## R-05 Async effects without cancellation

### Symptoms
- Search results or UI data sometimes "rewind" to an older state.
- Requests overlap; slow response wins incorrectly.
- "Set state on unmounted component" patterns.

### Refactor strategy
- Use AbortController when fetch supports it.
- Use a latest-only guard (request id).
- Ensure cleanup cancels or ignores stale work.

See also: `references/async-and-data-smells.md`

---

## R-06 Subscriptions and event listeners without cleanup

### Symptoms
- Memory leaks, duplicated handlers, repeated events.
- Components behave differently after navigating back and forth.

### Refactor strategy
- Always return a cleanup function in effects that attach listeners or subscribe.
- Ensure the same handler reference is removed (avoid recreating inline handlers when removing).
- For DOM events, see MDN: https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener

---

## R-07 Inline objects and functions passed as props

### Symptoms
- Child components rerender on every parent render even when data is unchanged.
- `useMemo` and `useCallback` added everywhere without proof.

### Refactor strategy
- Stabilize values only where needed:
  - Extract objects outside render if constant.
  - Memoize expensive computations.
  - Use callbacks with stable dependencies when passing deep into memoized children.

Avoid adding memoization to everything; it increases complexity.

---

## R-08 Overly broad Context values causing rerenders

### Symptoms
- Changing a tiny part of context rerenders huge subtrees.
- Performance problems tied to Context provider updates.

### Refactor strategy
- Split context by volatility (stable vs frequently changing).
- Provide derived selectors if using a store.
- Keep provider value stable when possible.

---

## R-09 Prop drilling and unstable component boundaries

### Symptoms
- Props passed down many levels.
- Intermediate components know too much about deep children.

### Refactor strategy
- Introduce a boundary:
  - a feature-level container that wires data
  - presentational children with minimal props
- Consider context selectively when it reduces coupling rather than increasing it.

---

## R-10 Index as key and unstable keys in lists

### Symptoms
- Items "swap" state during insertions or sorting.
- UI glitches when list changes.

### Refactor strategy
- Use stable ids from the data as keys.
- If no id exists, generate one at data creation time, not during render.

React docs explain why keys matter for list reconciliation:
- https://react.dev/learn/rendering-lists

---

## R-11 Excessive memoization as cargo cult

### Symptoms
- `useMemo` and `useCallback` everywhere.
- Hard-to-read dependency arrays.
- Bugs introduced by stale memoized values.

### Refactor strategy
- Memoize only when:
  - computation is expensive
  - child subtree is expensive and can skip rerender
- Prefer component splitting and data flow improvements first.

---

## R-12 setState during render

### Symptoms
- Warnings, infinite loops, unpredictable behavior.
- State changes triggered by conditional code in render.

### Refactor strategy
- Move state updates to:
  - event handlers
  - effects triggered by explicit signals
- Derive values in render without storing them.

---

## R-13 Duplicate state and sources of truth

### Symptoms
- Same value stored in multiple states (local state and store).
- Bugs where one updates but the other does not.

### Refactor strategy
- Choose a single source of truth.
- Use derived values instead of duplicated state.

---

## R-14 Conditional hooks and rules-of-hooks violations

### Symptoms
- Hooks inside conditions or loops.
- Runtime bugs: hook order changes.

### Refactor strategy
- Move conditions inside the hook or inside the hook body.
- Split components if necessary.

---

## R-15 UI state mixed with server/cache state

### Symptoms
- Loading states spread across components.
- Data consistency issues.
- Manual caching logic duplicated.

### Refactor strategy
- Separate:
  - server state (fetch, cache, invalidate)
  - UI state (open/closed, selected item)
- Centralize server state handling using existing project patterns.

---

## R-16 Missing error boundaries and brittle suspense usage

### Symptoms
- Small errors crash whole app.
- Unhandled promise rejections in UI.
- Suspense boundaries missing for slow components.

### Refactor strategy
- Add error boundaries around risky subtrees.
- Provide meaningful fallback UI and error states.

---

## Sources

- React exhaustive-deps lint rule: https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps
- React rendering lists and keys: https://react.dev/learn/rendering-lists
- MDN removeEventListener: https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener
