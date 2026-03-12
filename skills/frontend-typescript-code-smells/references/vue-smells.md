# Vue Frontend Smells (TypeScript + Composition API)

## Contents
- VUE-01 Mutating props or relying on implicit mutation
- VUE-02 Watchers used where computed would be safer
- VUE-03 Index as key in v-for and unstable keys
- VUE-04 Overusing reactive for complex objects without boundaries
- VUE-05 Side effects hidden in computed or getters
- VUE-06 Inconsistent typing between props, emits, and state
- VUE-07 Too much logic in templates
- VUE-08 Mixing server state with UI state
- Sources

---

## VUE-01 Mutating props

### Symptoms
- Child changes a prop value directly.
- Hard-to-track state changes.

### Refactor strategy
- Emit events upward and let the owner update state.
- Copy to local state intentionally when needed.

---

## VUE-02 Watchers used where computed would be safer

### Symptoms
- Watchers compute derived values and store them.
- Ordering issues and extra updates.

### Refactor strategy
- Prefer computed for derived values.
- Use watchers for side effects only.

---

## VUE-03 Index as key in v-for

### Symptoms
- Component state appears to jump between list items.

### Refactor strategy
- Use stable ids for keys.
- Generate ids at data creation time if necessary.

---

## VUE-04 Overusing reactive without boundaries

### Symptoms
- Large reactive objects passed around.
- Updates trigger large rerenders.

### Refactor strategy
- Split state into focused refs.
- Create view-model computed values and expose minimal interfaces.

---

## VUE-05 Side effects hidden in computed or getters

### Symptoms
- Computed triggers network calls or mutations.
- Unpredictable behavior.

### Refactor strategy
- Keep computed pure.
- Put side effects in explicit actions or effects.

---

## VUE-06 Inconsistent typing between props, emits, and state

### Symptoms
- Props typed loosely; emits payload not typed.
- Runtime mismatches.

### Refactor strategy
- Define shared types for props and events.
- Validate at boundaries when values come from untyped sources.

---

## VUE-07 Too much logic in templates

### Symptoms
- Complex conditional rendering and formatting inline.

### Refactor strategy
- Move to script setup:
  - computed values
  - helpers
- Extract components.

---

## VUE-08 Mixing server state with UI state

### Symptoms
- Data fetching logic is scattered.
- Inconsistent caching and error handling.

### Refactor strategy
- Centralize server state handling in composables or a data layer.
- Keep UI state local.

---

## Sources

- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html
