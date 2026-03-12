# SOLID and Frontend Architecture Guidance for TypeScript

This reference adapts SOLID principles to frontend TypeScript. The goal is pragmatic: reduce coupling, improve testability, and make UI changes safer.

## Contents
- Single Responsibility in UI code
- Open/Closed via composition and extension points
- Liskov Substitution and component contracts
- Interface Segregation for props and contexts
- Dependency Inversion with adapters and ports
- Practical patterns
- Anti-patterns to avoid

---

## Single Responsibility in UI code

A component should have one primary reason to change. In frontend code, responsibilities commonly include:
- data fetching
- state transitions
- formatting and mapping
- presentation (rendering and styling)
- orchestration (routing, analytics, storage)

Refactor toward:
- pure helpers for calculations and mapping
- presentational components for rendering
- hooks or services for stateful logic
- adapters for integrations

See: `references/refactoring-workflow.md`

---

## Open/Closed via composition and extension points

Prefer extension without editing internals:
- composition: pass children or render props
- variants: typed variant props rather than many booleans
- theming: design tokens and theming providers

Avoid:
- adding another boolean flag for every new case
- large switch statements inside a shared component without an extension point

---

## Liskov Substitution and component contracts

If Component B claims to be usable wherever Component A is used (same props contract), it must behave consistently:
- same required props semantics
- same event payload expectations
- same accessibility contracts (keyboard, focus)

Make contracts explicit:
- shared prop types
- shared event payload types
- storybook or examples that validate expectations

---

## Interface Segregation for props and contexts

Avoid forcing consumers to depend on unused fields.
- Keep props small and focused.
- Prefer multiple small contexts over one mega-context.
- Prefer explicit view models over raw API shapes.

See: `references/smell-catalog.md` (prop explosion, monolithic context)

---

## Dependency Inversion with adapters and ports

UI code should depend on abstractions of side effects, not concrete implementations.

Practical approaches in TypeScript:
- Adapter modules that wrap:
  - API clients
  - router navigation
  - analytics events
  - storage
- Inject functions as dependencies:
  - pass an api object into hooks
  - pass a navigation function into helpers
- Use context as a dependency injection mechanism sparingly.

Aim for:
- UI uses `UserRepository` interface
- Implementation uses `fetch` or a specific client behind an adapter

---

## Practical patterns

- Adapter + mapper at boundaries: raw payload -> domain model -> UI model
- Container/presenter split at feature boundary
- Custom hooks as state machines
- Discriminated unions for async state and UI state

---

## Anti-patterns to avoid

- "Architecture astronautics" in UI layers (too many layers without value)
- Shared god components that become dumping grounds
- Excessive abstraction without clear reuse
- Memoization everywhere without measurement
