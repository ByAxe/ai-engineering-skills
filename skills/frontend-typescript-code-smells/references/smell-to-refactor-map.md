# Smell to Refactor Map (Frontend TypeScript)

Use this as a quick index when planning a refactor.

## Contents
- Boundary and component smells
- State and data flow smells
- Effects and async smells
- Performance smells
- TypeScript type smells
- Styling, a11y, testing, security smells

---

## Boundary and component smells

- B-01 God component -> Extract helpers -> Extract presentational components -> Extract hook -> Optional adapter boundary
- B-02 Mixed responsibilities -> Move domain logic to pure module; keep UI thin
- B-03 Prop explosion -> Group props; options object; split component
- B-04 Deep conditional rendering -> Extract branches; discriminated union render switch
- B-08 Circular dependencies -> Create public entry points; invert dependency direction

See: `references/refactoring-workflow.md`

---

## State and data flow smells

- S-01 Duplicate sources of truth -> Choose one; derive others
- S-02 Derived state stored -> Compute in render; memoize expensive only
- S-03 Mutating state -> Immutable updates; readonly types
- S-04 Global state for local UI -> Move to local state
- S-08 Monolithic context -> Split contexts; narrow provider updates

---

## Effects and async smells

- E-01 Missing cleanup -> Add cleanup; stable handler refs
- E-02 Stale closures -> Fix deps; restructure; avoid ignoring lint rules
- E-04 Effect loops -> Guard updates; model state properly
- A-04 Races -> Abort or latest-only guard; add regression tests
- A-03 Missing async states -> Model idle/loading/success/error

See: `references/async-and-data-smells.md` and `references/react-smells.md`

---

## Performance smells

- P-01 Render storms -> Stabilize props; split component; narrow subscriptions/context
- P-02 Expensive render work -> Extract/memoize expensive computations
- P-05 Large lists -> Virtualize
- P-07 Layout thrash -> Batch reads/writes; requestAnimationFrame

See: `references/performance-and-rendering.md`

---

## TypeScript type smells

- TS-01 any leakage -> unknown + narrowing
- TS-03 non-null assertions -> modeling + runtime checks
- TS-05 boolean trap -> options object or mode union
- TS-07 god interfaces -> discriminated unions

See: `references/typescript-type-smells.md`

---

## Styling, a11y, testing, security smells

- CSS-01 specificity wars -> scope styles; reduce selector depth
- AX-01 non-semantic controls -> semantic elements + keyboard support
- T-02 implementation-detail tests -> behavior tests
- SEC-01 unsafe HTML injection -> render text or sanitize with allowlist

See:
- `references/styling-and-css-smells.md`
- `references/accessibility-and-ux-smells.md`
- `references/testing-and-maintainability.md`
- `references/security-smells.md`
