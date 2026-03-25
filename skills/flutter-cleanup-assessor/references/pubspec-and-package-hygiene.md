# Pubspec and Package Hygiene

Use this file when dependency sprawl, stale packages, mixed patterns, or package-level confusion is hurting maintainability.

## What to check

### Dependencies

- Are there multiple packages solving the same problem without a reason?
- Is the app mixing several state-management approaches in one feature?
- Are packages pinned so tightly that safe upgrades become painful?
- Are there old packages with no active use?
- Are `path:` or git dependencies used where published versions would be safer?

### Dev dependencies

- Is code generation present but barely used?
- Are testing and lint packages current and still aligned with the codebase?
- Are old build tools still present after architecture changes?

### Assets and configuration

- Are assets declared and actually used?
- Are fonts, localization generation, or plugin setup files coherent with the current codebase?
- Do package names and descriptions still reflect what the package does?

## Smells

- `pubspec.yaml` grows forever and nobody removes packages
- old experiments remain in dependencies
- several packages offer similar DI, state, or networking responsibilities
- package overrides are used as a quiet long-term workaround
- generated code and generators exist for one tiny use case that no longer pays off

## Cleanup moves

- remove unused runtime and dev dependencies
- collapse overlapping packages where a simpler stack is enough
- review `dependency_overrides` with suspicion
- align lint and test tools with how the team actually works
- make asset declarations and localization config intentional

## Commands

```bash
flutter pub outdated
flutter pub get
flutter analyze
flutter test
```

If the repo is multi-package, run these in each affected package.

## Package-hygiene review checklist

- Which packages are clearly unused?
- Which packages overlap in purpose?
- Are dependency constraints reasonable?
- Are there risky overrides?
- Are codegen tools still earning their complexity?
- Does each package in the repo have a clear role?

See also:

- `references/tooling-lints-and-quality-gates.md`
- `references/flutter-architecture-principles.md`
