# Angular Frontend Smells (TypeScript + Templates)

## Contents
- NG-01 Subscriptions without teardown
- NG-02 Excessive manual subscribe in components
- NG-03 Missing trackBy in large ngFor lists
- NG-04 Heavy template logic
- NG-05 Change detection thrash and missing OnPush where appropriate
- NG-06 Non-null assertions in templates hiding real null states
- NG-07 Shared services as global mutable state
- NG-08 Leaky abstractions between components and services
- NG-09 Overusing any in inputs and outputs
- NG-10 Routing and resolvers doing too much
- Sources

---

## NG-01 Subscriptions without teardown

### Symptoms
- `subscribe()` in a component without unsubscribe.
- Memory leaks after navigation.

### Refactor strategy
- Prefer async pipe in templates when possible.
- Otherwise, ensure teardown:
  - takeUntil pattern
  - Subscription management in ngOnDestroy

---

## NG-02 Excessive manual subscribe in components

### Symptoms
- Components coordinate many streams with nested subscribes.
- Hard to reason about.

### Refactor strategy
- Compose streams in services or facades.
- Expose a view-model observable to the component.
- Keep the component mostly declarative.

---

## NG-03 Missing trackBy in large ngFor lists

### Symptoms
- List rerenders unnecessarily; UI jank.

### Refactor strategy
- Provide `trackBy` with stable ids.
- Ensure ids are stable across reloads.

---

## NG-04 Heavy template logic

### Symptoms
- Complex conditions and formatting in templates.
- Inline functions in templates.

### Refactor strategy
- Move logic to component class or pure pipes.
- Precompute view models.

---

## NG-05 Change detection thrash

### Symptoms
- Frequent change detection cycles; performance issues.

### Refactor strategy
- Use OnPush strategically when inputs are immutable and stream-driven.
- Reduce event storms.
- Avoid creating new objects in bindings when possible.

---

## NG-06 Non-null assertions in templates hide real null states

### Symptoms
- Using non-null assertions to silence template errors.

### Refactor strategy
- Model async states explicitly.
- Use safe navigation and explicit loading states.

---

## NG-07 Shared services as global mutable state

### Symptoms
- Services hold mutable state used by many components.
- Hard to trace changes.

### Refactor strategy
- Prefer explicit state stores or observable state with clear update APIs.
- Keep services as boundaries, not dumping grounds.

---

## NG-08 Leaky abstractions between components and services

### Symptoms
- Components import low-level API clients directly.
- Services expose raw response shapes.

### Refactor strategy
- Use adapters/mappers in services.
- Expose domain models to components.

---

## NG-09 Overusing any in inputs and outputs

### Symptoms
- @Input() typed as any or unknown without narrowing.
- @Output() emits loosely typed payloads.

### Refactor strategy
- Define and share event payload types.
- Make inputs strict; validate boundary values.

---

## NG-10 Routing and resolvers doing too much

### Symptoms
- Resolver contains business logic and mapping.
- Navigation triggers unpredictable side effects.

### Refactor strategy
- Keep resolvers focused on fetching required data.
- Move domain logic to services.
- Model loading and error states explicitly.

---

## Sources

- TypeScript non-null assertion operator: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-2-0.html
