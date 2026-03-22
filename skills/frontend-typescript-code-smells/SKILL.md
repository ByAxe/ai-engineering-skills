---
name: frontend-typescript-code-smells
description: Identifies and refactors frontend TypeScript code smells in React, Angular, Vue, or vanilla TS. Use when the user asks to clean up or refactor UI code, reduce re-renders, fix effect or subscription bugs, remove unsafe any usage, untangle state and data flow, improve component boundaries, or strengthen TypeScript types without changing behavior.
license: MIT
metadata:
  author: ByAxe
  version: 1.0.0
  category: software-development
  environment: Frontend TypeScript projects using TS or TSX. Works best with repository access and ability to run npm scripts for lint, typecheck, test, and build.
  tags:
    - typescript
    - frontend
    - refactoring
    - code-smells
    - react
    - angular
    - vue
    - performance
---

# Frontend TypeScript Code Smells

Use this skill to **diagnose** frontend TypeScript smells and to **refactor safely** while preserving behavior.

This skill is optimized for:
- TypeScript and TSX codebases
- SPA frameworks (React, Angular, Vue) and framework-agnostic UI code
- Refactors that must not break behavior, types, or rendering performance

## Operating rules

Follow these rules unless the user explicitly requests otherwise:

1. **Preserve behavior first.** Avoid "rewrite from scratch" solutions.
2. **Refactor in small, reviewable steps.** Prefer 2–5 small commits over one giant diff.
3. **Prefer types that prevent bugs.** Avoid `any`, excessive assertions, and non-null assertions.
4. **Make performance measurable.** Only add memoization or optimizations when there is a clear render or runtime cost.
5. **Avoid framework-specific assumptions.** If the framework is not specified, stay framework-agnostic and ask at most one clarification when it materially changes the solution.
6. **Always include verification steps.** Provide commands and checkpoints (lint, typecheck, tests, build).
7. **Explain the intent, not the history.** Keep reasoning tied to the observed smell and the change.

## Workflow checklist

Copy and follow this checklist for each request:

```
Refactor checklist
- [ ] Clarify the goal: bug fix, readability, performance, type-safety, or architecture
- [ ] Identify and name the smells (with risk level: correctness, performance, maintainability, security, a11y)
- [ ] Choose the smallest refactor that removes the smell
- [ ] Apply the change as a patch (file-by-file, diff-style)
- [ ] Strengthen types and remove unsafe assertions introduced by the smell
- [ ] Add or update tests only where behavior could regress
- [ ] Verify: lint, typecheck, unit tests, build; add perf checks if relevant
- [ ] Summarize what changed and why, plus follow-up refactors (optional)
```

## What to ask from the user

If the request does not include enough context, ask for the smallest missing piece and proceed with reasonable assumptions.

Prefer these questions (in order):
1. Framework and environment: React, Angular, Vue, or vanilla TS?
2. Target scope: one file, a component, or a whole feature?
3. Constraints: allowed dependencies, lint rules, state library, API layer, styling system?

If code is provided as a snippet, assume:
- TypeScript strict mode is desired
- Existing public APIs should remain stable
- Rendering behavior should remain identical unless the smell is a correctness bug

## Output contract

When providing a refactor, output these sections in this order:

1. **Smells found**
   - bullet list: smell name, evidence, risk, and likely root cause
2. **Refactor plan**
   - 3–7 steps, ordered, with the smallest step that creates value first
3. **Patch**
   - show updated code (or diff) with file paths
4. **Verification**
   - exact commands and what success looks like
5. **Follow-ups**
   - optional: additional improvements deferred for safety or scope

## Smell navigation

Use progressive disclosure. Keep the active response focused and pull detailed material only when needed.

- Full catalog (all smells, symptoms, and fixes): `references/smell-catalog.md`
- TypeScript-only smells and safe typing recipes: `references/typescript-type-smells.md`
- React-specific smells (hooks, rendering, state): `references/react-smells.md`
- Performance and rendering playbook: `references/performance-and-rendering.md`
- Async and data fetching pitfalls (cancellation, races, caching): `references/async-and-data-smells.md`
- Accessibility and semantic HTML smells: `references/accessibility-and-ux-smells.md`
- Testing smells and refactor-safe test strategy: `references/testing-and-maintainability.md`
- Angular-specific smells (RxJS, change detection, templates): `references/angular-smells.md`
- Vue-specific smells (Composition API, templates, reactivity): `references/vue-smells.md`
- Styling and CSS smells (specificity, theming, performance): `references/styling-and-css-smells.md`
- Frontend security smells (XSS, redirects, trust boundaries): `references/security-smells.md`
- SOLID and architecture guidance for frontend TypeScript: `references/architecture-and-solid.md`
- Smell-to-refactor quick map: `references/smell-to-refactor-map.md`
- Sources and further reading: `references/sources.md`
- Ready-to-copy checklists and refactor templates: `references/checklists.md`

## Refactoring heuristics

### Prioritize by risk

Sort findings by:
1. **Correctness bugs** (stale closures, race conditions, invalid assumptions, broken cleanup)
2. **Security** (unsafe HTML injection, exposed secrets, unsafe token handling)
3. **Performance cliffs** (render storms, layout thrash, large lists without virtualization)
4. **Maintainability** (god components, duplicated logic, unclear boundaries)
5. **Type safety** (any leakage, unsound assertions, inconsistent nullability)
6. **A11y regressions** (non-semantic controls, missing labels, keyboard traps)

### Choose the smallest effective refactor

Prefer these moves (in order):
- Rename for clarity, reorder code, and extract helpers
- Extract pure functions (domain logic) out of components
- Extract a component or hook with a stable API
- Introduce a boundary module (adapter, mapper, facade)
- Only then: restructure folders, switch state libraries, large rewrites

### Common verification commands

If a repo exists, prefer:
- `npm run lint`
- `npm run typecheck` or `npx tsc --noEmit`
- `npm test`
- `npm run build`

If performance is involved:
- Use a framework profiler (React DevTools Profiler) or run a Lighthouse pass.
- Validate that render counts and long tasks improve after the refactor.

## Troubleshooting patterns

### User says: "It re-renders too much"
- Identify the state or props causing the render storm.
- Look for referential instability (new objects/functions each render) and over-broad context updates.
- Produce a minimal change that stabilizes references or narrows context value updates.
- Consult: `references/performance-and-rendering.md`

### User says: "useEffect is buggy" or "stale values"
- Treat as a correctness issue first.
- Ensure dependencies are correct and remove hidden coupling between renders and effects.
- Consult: `references/react-smells.md` and `references/async-and-data-smells.md`

### User says: "Remove any" or "make this type-safe"
- Replace `any` with `unknown` and narrow.
- Model domain constraints with literal unions and discriminated unions.
- Consult: `references/typescript-type-smells.md`

### User says: "This component is huge"
- Identify responsibility seams: data fetching, state, rendering, formatting, event handling.
- Extract in this order: pure helpers, presentational components, hooks, then adapters.
- Consult: `references/smell-catalog.md` and `references/refactoring-workflow.md`

## Examples

### Example 1: React performance
User: "This TSX component re-renders constantly. Refactor it."
Action: Diagnose render triggers, remove referential instability, narrow context/state updates, and verify with profiler and tests.

### Example 2: Type safety
User: "Replace all anys in this file and keep behavior."
Action: Introduce safe types, add narrowing helpers, and eliminate unsafe assertions while keeping call sites stable.

### Example 3: Async correctness
User: "Our search box sometimes shows the wrong results."
Action: Diagnose race conditions, introduce cancellation and request sequencing, and add a regression test.

## Trigger test suite

These should trigger:
- "Refactor this TypeScript component, it is unreadable"
- "Find code smells in my React TSX code"
- "Remove any usage and make types strict"
- "Fix stale closure or useEffect dependency bugs"
- "Why is my page re-rendering so much"
- "Clean up our frontend state management code"

These should not trigger:
- "Write a SQL query"
- "Help me with backend Java code"
- "Summarize this article"
- "Plan a vacation itinerary"
