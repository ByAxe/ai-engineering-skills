# Tooling, Lints, and Quality Gates

Use this file when the cleanup work should be backed by analyzer rules, consistent formatting, and repeatable checks.

## Baseline commands

For a Flutter app:

```bash
flutter pub get
dart format -o none --set-exit-if-changed .
flutter analyze
flutter test
```

When integration tests exist:

```bash
flutter test integration_test
```

Useful maintenance commands:

```bash
dart fix --dry-run
dart fix --apply
flutter pub outdated
```

Choose the narrowest build command that validates the touched surface only when needed.

## Recommended lint starting point

### Flutter-wide lints

Use `flutter_lints` as the base set unless the project already has a carefully curated alternative.

### Bloc-specific lints

If the app uses bloc heavily, consider adding the recommended bloc lints.

## Sample `analysis_options.yaml`

See `assets/analysis_options.flutter-cleanup.sample.yaml`.

This sample combines:

- `flutter_lints`
- selected analyzer exclusions for generated code
- `bloc_lint` recommended rules

Adjust rather than copy blindly.

## Generated code policy

Generated files should usually be:

- formatted
- excluded from manual cleanup work
- excluded from some analyzer noise when appropriate

But generated output should never become an excuse to ignore broken source annotations or broken source models.

## Useful quality gates

- formatting must be clean
- analyzer must be green or intentionally triaged
- tests for touched features must pass
- dependency drift should be visible
- lint suppressions should be specific and explained

## Smells

- analyzer warnings are normal and ignored
- `ignore_for_file` hides broad categories of issues without explanation
- generated code is edited manually
- old unused packages remain because nothing checks them
- different packages in the repo use conflicting lint baselines without reason

## Suggested CI posture

At minimum, every touched package or app should be able to run:

```bash
dart format -o none --set-exit-if-changed .
flutter analyze
flutter test
```

For monorepos, apply checks per package and per example app as appropriate.

## Review checklist

- Is there a shared lint baseline?
- Is analyzer output clean or intentionally triaged?
- Are generated files handled deliberately?
- Are suppressions minimal and justified?
- Are outdated dependencies reviewed?
- Are quality gates easy to run locally and in CI?

See also:

- `assets/analysis_options.flutter-cleanup.sample.yaml`
- `references/pubspec-and-package-hygiene.md`
- `references/testing-strategy.md`
