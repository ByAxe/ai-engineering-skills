# Async and Data Fetching Smells in Frontend TypeScript

## Contents
- A-01 Fetching during render
- A-02 Duplicated fetching logic across components
- A-03 Missing loading and error modeling
- A-04 Race conditions and out-of-order responses
- A-05 Missing cancellation and cleanup
- A-06 Mixing side effects into reducers or selectors
- A-07 Unstable cache invalidation
- A-08 Unhandled promises and silent failures
- A-09 Excessive waterfalls in component trees
- Recipes
- Sources

---

## A-01 Fetching during render

### Symptoms
- Fetch or async call happens directly in render or component body.
- Multiple fetches per render.

### Refactor strategy
- Move fetching into:
  - a dedicated hook
  - a service layer
  - a framework data loader if available
- Ensure requests are triggered by explicit inputs.

---

## A-02 Duplicated fetching logic across components

### Symptoms
- Many components have similar fetch code.
- Inconsistent error handling and caching.

### Refactor strategy
- Introduce a single fetch adapter or hook:
  - handles request creation
  - handles caching and dedupe (if used)
  - exposes a stable domain model to UI

---

## A-03 Missing loading and error modeling

### Symptoms
- UI assumes data exists and uses non-null assertions.
- No consistent empty/error UI.

### Refactor strategy
- Model async states explicitly.
- Render based on state:
  - loading: skeleton or spinner
  - error: inline message and retry
  - success: data UI
  - empty: empty state

---

## A-04 Race conditions and out-of-order responses

### Symptoms
- Search results show wrong items.
- Switching filters quickly causes stale data to appear.

### Root causes
- Requests overlap; earlier request resolves later and overwrites state.

### Refactor strategy
Choose one:
1. **Abort previous request**
2. **Latest-only guard**
   - request id counter
   - apply result only if id matches latest
3. **Central cache** that dedupes by key

Add a regression test that reproduces the race.

---

## A-05 Missing cancellation and cleanup

### Symptoms
- Memory leaks or duplicated subscriptions.
- Updating state after unmount patterns.

### Refactor strategy
- Ensure cleanup cancels:
  - timers
  - subscriptions
  - event listeners
  - in-flight requests (when possible)

---

## A-06 Mixing side effects into reducers or selectors

### Symptoms
- Reducers call APIs or trigger side effects.
- Selectors perform fetches or subscriptions.

### Refactor strategy
- Keep reducers pure.
- Put side effects in:
  - effects layer
  - middleware
  - services
- Keep selectors pure and memoized if necessary.

---

## A-07 Unstable cache invalidation

### Symptoms
- UI shows stale data after mutations.
- Refetch logic inconsistent.

### Refactor strategy
- Centralize invalidation with clear keys.
- Use a single "source of truth" for cache state.

---

## A-08 Unhandled promises and silent failures

### Symptoms
- Errors swallowed in catch blocks.
- UI fails silently.

### Refactor strategy
- Surface errors to:
  - UI state
  - error boundary
  - logging/monitoring layer if present

---

## A-09 Excessive waterfalls in component trees

### Symptoms
- Parent loads, then child loads, then grandchild loads.
- Slow navigation and repeated spinners.

### Refactor strategy
- Batch requests when possible.
- Move fetching up to a feature boundary, then pass data down.
- Prefetch on navigation or idle time if supported.

---

## Recipes

### Latest-only guard pattern
- Keep a counter or token in scope.
- Apply state only for the latest request.

### AbortController pattern
- Create AbortController per request.
- Abort on cleanup.

---

## Sources

- React exhaustive-deps lint rule discussion: https://react.dev/reference/eslint-plugin-react-hooks/lints/exhaustive-deps
- MDN removeEventListener (cleanup pattern): https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener
