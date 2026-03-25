# Accessibility, Localization, and Adaptivity

Use this file when the cleanup scope includes user-facing polish that affects long-term product quality.

## Accessibility

Treat accessibility as a correctness concern, not a finishing touch.

### Check for

- controls without clear labels
- icon-only buttons with no semantic meaning
- tap targets that are too small
- poor contrast
- text that truncates or overlaps badly under larger text scale
- focus order that becomes confusing in complex layouts
- status messages that are visible but not announced clearly

### Practical fixes

- add semantic labels where the visible UI is ambiguous
- make tap targets comfortably large
- ensure important controls remain reachable under text scaling
- keep visible text and announced text consistent
- test critical flows with a screen reader and with increased text scale

## Localization

The cleanup phase is a good time to remove hard-coded strings.

### Smells

- raw user-facing strings in widgets
- date or number formatting scattered across the UI
- layouts that only work for short English text
- string concatenation that will localize badly

### Prefer

- localized message access through your chosen localization setup
- formatting via localization-aware APIs
- layouts that tolerate longer strings and different pluralization

## Adaptivity and responsive resilience

A cleaned-up screen should still behave well when constraints change.

Check:

- small phones
- large phones
- tablets or split-screen scenarios
- landscape
- larger text scale
- keyboard-open states
- web/desktop pointer and window resizing if the app supports them

## Example: removing hard-coded strings

### Before

```dart
Text('Retry')
```

### After

```dart
Text(context.l10n.retryButtonLabel)
```

## Example: resilient layout

### Before

```dart
Row(
  children: [
    const Icon(Icons.warning),
    Text(errorMessage),
    ElevatedButton(
      onPressed: onRetry,
      child: const Text('Retry'),
    ),
  ],
)
```

This can overflow quickly.

### Better

```dart
Wrap(
  spacing: 12,
  runSpacing: 12,
  crossAxisAlignment: WrapCrossAlignment.center,
  children: [
    const Icon(Icons.warning),
    ConstrainedBox(
      constraints: const BoxConstraints(maxWidth: 320),
      child: Text(errorMessage),
    ),
    ElevatedButton(
      onPressed: onRetry,
      child: Text(context.l10n.retryButtonLabel),
    ),
  ],
)
```

## Review checklist

- Are user-facing strings localizable?
- Do important controls have clear labels?
- Do layouts survive larger text and longer translations?
- Are tap targets large enough?
- Does the touched flow work with assistive technologies?
- Does the screen behave under realistic size changes?

See also:

- `references/widget-ui-smells.md`
- `references/testing-strategy.md`
- `references/assessment-checklists.md`
