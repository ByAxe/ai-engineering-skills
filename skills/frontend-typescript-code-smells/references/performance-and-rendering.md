# Performance and Rendering Playbook for Frontend TypeScript

## Contents
- How to diagnose before optimizing
- Common performance smells
- Render and reconciliation smells
- Main-thread and layout performance smells
- Bundle and loading performance smells
- Refactor patterns that usually help
- Verification and measurement checklist
- Sources

---

## How to diagnose before optimizing

Performance work should start with **evidence**.

1. Identify the slow user flow:
   - typing, scrolling, opening a modal, filtering, navigation
2. Identify the bottleneck category:
   - too many renders
   - expensive render work
   - expensive effects or subscriptions
   - layout thrash and forced reflow
   - large bundle or slow initial load
   - memory leak
3. Capture a baseline measurement:
   - framework profiler
   - browser performance recording
   - lighthouse score and key metrics if relevant

Stop when the improvement is achieved. Additional optimization is often a maintainability smell.

---

## Common performance smells (overview)

- P-01 Render storms (too many rerenders)
- P-02 Expensive work inside render
- P-03 Referential instability (new objects/functions every render)
- P-04 Large lists without virtualization
- P-05 Context churn (provider value recreated frequently)
- P-06 Layout thrash (read/write layout in loops)
- P-07 Unthrottled high-frequency events
- P-08 Too much work in effects (fetch loops, timers)
- P-09 Unnecessary bundle weight (importing entire libraries)
- P-10 Hydration or initial render bottlenecks

---

## P-01 Render storms

### Symptoms
- Typing or small interactions lag.
- Many components rerender per interaction.

### Typical root causes
- State updates at a high level instead of localizing state.
- Context updates causing large subtree rerenders.
- Passing unstable props.

### Fix patterns
- Split components and localize state.
- Narrow context.
- Stabilize props where needed.

---

## P-02 Expensive work inside render

### Symptoms
- Render itself is slow; profiler shows expensive component.
- Heavy mapping, sorting, filtering, parsing in render.

### Fix patterns
- Extract pure functions.
- Cache expensive computations:
  - compute once in memo only if expensive and stable
- Precompute in data layer instead of UI layer.

---

## P-03 Referential instability

### Symptoms
- Child rerenders because a prop reference changes.
- Memoized child does not skip renders.

### Fix patterns
- Avoid creating new objects/functions in render when passing down.
- Use stable callbacks or hoist constants.
- Memoize only when there is a measurable benefit.

---

## P-04 Large lists without virtualization

### Symptoms
- Scrolling is janky.
- DOM node count huge.

### Fix patterns
- Virtualize lists.
- Render placeholders and progressively load.

---

## P-05 Context churn

### Symptoms
- Provider rerenders cause whole app to rerender.
- Context value built with inline object.

### Fix patterns
- Split contexts by volatility.
- Use selectors or multiple providers.
- Keep provider values stable.

---

## P-06 Layout thrash

### Symptoms
- Forced reflow warnings in performance trace.
- Reading layout (offsetHeight, getBoundingClientRect) and then writing styles repeatedly.

### Fix patterns
- Batch reads and writes.
- Use requestAnimationFrame for animation loops.
- Prefer CSS transforms for animations.

---

## P-07 Unthrottled high-frequency events

### Symptoms
- scroll, resize, mousemove handlers doing heavy work.
- Frequent state updates.

### Fix patterns
- Throttle or debounce when appropriate.
- Use passive listeners for scroll where appropriate.
- Move heavy work off the critical path.

---

## P-08 Too much work in effects

### Symptoms
- Effects trigger often and do heavy work.
- Fetch loops and repeated subscriptions.

### Fix patterns
- Fix dependency wiring.
- Add guards and cancellation.
- Move work to dedicated services or caches.

---

## P-09 Unnecessary bundle weight

### Symptoms
- Slow load, large JS bundle.
- Importing large libraries for small tasks.

### Fix patterns
- Prefer selective imports.
- Lazy load rarely used routes/components.
- Replace heavyweight dependencies if allowed by project constraints.

---

## P-10 Hydration or initial render bottlenecks

### Symptoms
- Server-rendered apps are slow to become interactive.
- Large hydration cost.

### Fix patterns
- Reduce initial component tree complexity.
- Defer non-critical widgets.
- Split bundles and hydrate selectively if supported.

---

## Refactor patterns that usually help

- Extract heavy pure logic out of components.
- Split components and narrow props.
- Use stable boundaries and stable keys.
- Centralize cache and async state, remove duplicate fetches.
- Avoid unnecessary memoization until a profiler shows a hotspot.

---

## Verification and measurement checklist

- [ ] Baseline measurement captured.
- [ ] Hypothesis stated (what causes the slow path).
- [ ] Minimal fix applied.
- [ ] Post-change measurement shows improvement.
- [ ] No regression in tests, typecheck, lint, build.
- [ ] No new complexity introduced without justification.

---

## Sources

- React rendering lists and keys: https://react.dev/learn/rendering-lists
- MDN removeEventListener: https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener
