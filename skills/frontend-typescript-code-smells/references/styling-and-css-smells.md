# Styling and CSS Smells in Frontend TypeScript

## Contents
- CSS-01 Specificity wars and fragile overrides
- CSS-02 Global leakage and collisions
- CSS-03 Inline styles used as a default
- CSS-04 Recreated style objects and class strings on every render
- CSS-05 Styling logic mixed into business logic
- CSS-06 Design tokens and theming inconsistencies
- CSS-07 Magic numbers and layout coupling
- Refactor patterns

---

## CSS-01 Specificity wars and fragile overrides

### Symptoms
- Deep selectors, !important, cascading overrides.
- Small change breaks styling elsewhere.

### Refactor strategy
- Prefer scoped styles (CSS modules, scoped CSS, component styles).
- Prefer design system primitives and variants.
- Reduce selector depth.

---

## CSS-02 Global leakage and collisions

### Symptoms
- Global class names collide between features.
- Styling depends on load order.

### Refactor strategy
- Use local scoping.
- Create a clear "global styles" boundary and keep it small.

---

## CSS-03 Inline styles used as a default

### Symptoms
- Many inline style objects.
- Hard to share or theme.

### Refactor strategy
- Use classes and variants for reusable styling.
- Keep inline styles only for truly dynamic values.

---

## CSS-04 Recreated style objects and class strings on every render

### Symptoms
- Performance regression from new objects each render.
- Memoized children rerender.

### Refactor strategy
- Hoist constant style objects.
- Use stable className composition helpers.

---

## CSS-05 Styling logic mixed into business logic

### Symptoms
- Business rules decide CSS class names directly.
- Many string concatenations.

### Refactor strategy
- Map domain states to presentation variants in one place.
- Prefer typed variant maps.

---

## CSS-06 Design tokens and theming inconsistencies

### Symptoms
- Hard-coded colors and spacing.
- Theme switching inconsistent.

### Refactor strategy
- Use CSS variables or design token system.
- Centralize tokens and document them.

---

## CSS-07 Magic numbers and layout coupling

### Symptoms
- Layout depends on arbitrary pixel values scattered across files.

### Refactor strategy
- Use shared constants and tokens.
- Prefer layout primitives (grid, flex) and spacing scales.

---

## Refactor patterns

- Introduce component variants instead of boolean flags.
- Create a design-token module for shared constants.
- Replace fragile selectors with scoped styles and simpler class structure.
