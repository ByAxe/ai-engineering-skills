# Accessibility and UX Smells in Frontend TypeScript

## Contents
- AX-01 Non-semantic interactive elements
- AX-02 Missing labels and accessible names
- AX-03 Keyboard navigation gaps
- AX-04 Focus management bugs
- AX-05 Inaccessible custom components
- AX-06 Announcements and live regions missing
- AX-07 Color-only communication
- AX-08 Motion and animation without reduced-motion handling
- AX-09 Error messages not associated with fields
- Quick a11y refactor checklist
- Sources

---

## AX-01 Non-semantic interactive elements

### Symptoms
- Click handlers on div or span.
- Missing role, tabIndex, keyboard handling.

### Refactor strategy
- Use semantic elements:
  - button for actions
  - a for navigation
  - input for inputs
- If a custom element is necessary, add:
  - role
  - tabIndex
  - keyboard handlers (Enter/Space)
  - focus styles

---

## AX-02 Missing labels and accessible names

### Symptoms
- Inputs without labels.
- Icon-only buttons without aria-label.

### Refactor strategy
- Prefer visible labels with label-for wiring.
- Provide accessible name:
  - aria-label
  - aria-labelledby

---

## AX-03 Keyboard navigation gaps

### Symptoms
- Cannot complete workflows without a mouse.
- Focus gets lost after actions.

### Refactor strategy
- Ensure tab order is logical.
- Ensure every interactive element is reachable.
- Ensure key handlers exist where needed.

---

## AX-04 Focus management bugs

### Symptoms
- Modal opens but focus stays behind it.
- Closing a dialog loses focus.

### Refactor strategy
- On open: move focus to dialog or first focusable control.
- On close: restore focus to the trigger.
- Ensure focus is trapped inside modal when appropriate.

---

## AX-05 Inaccessible custom components

### Symptoms
- Custom selects, menus, tabs without keyboard behavior.
- ARIA attributes incomplete.

### Refactor strategy
- Prefer proven component libraries or established patterns.
- If building custom, implement expected keyboard interactions and ARIA states.

---

## AX-06 Announcements and live regions missing

### Symptoms
- Screen reader users do not get notified on async updates.
- Toast notifications are invisible to assistive tech.

### Refactor strategy
- Use aria-live regions for important announcements.
- Ensure error and success messages are reachable.

---

## AX-07 Color-only communication

### Symptoms
- State indicated only by color (red/green).
- Low-contrast UI.

### Refactor strategy
- Add text or icons with accessible labels.
- Ensure contrast meets standards.

---

## AX-08 Motion and animation without reduced-motion handling

### Symptoms
- Animations cause discomfort or are distracting.
- No respect for prefers-reduced-motion.

### Refactor strategy
- Use prefers-reduced-motion media query to reduce or disable animations.

---

## AX-09 Error messages not associated with fields

### Symptoms
- Form errors shown but not connected to input.
- Screen reader does not announce errors.

### Refactor strategy
- Associate errors using aria-describedby.
- Ensure error message is present in DOM when relevant.

---

## Quick a11y refactor checklist

- [ ] Use semantic elements by default.
- [ ] Ensure accessible names for all controls.
- [ ] Ensure keyboard navigation and focus management.
- [ ] Ensure errors are announced and associated.
- [ ] Validate with automated checks and manual keyboard test.

---

## Sources

- MDN removeEventListener (cleanup best practice for interactive widgets): https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener
