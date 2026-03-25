# Flutter Cleanup Assessment Template

Use this template when reporting a cleanup assessment.

## 1. Smells found

- **Smell:** 
  - Evidence:
  - Risk:
  - Likely root cause:

## 2. Top risks

1. 
2. 
3. 

## 3. Target architecture decision

- Recommended shape:
- Keep:
- Remove or collapse:
- Why this is the smallest good shape:

## 4. Refactor plan

1. 
   - Safety check:
2. 
   - Safety check:
3. 
   - Safety check:

## 5. Concrete file-level changes

- `path/to/file.dart`
  - Change:
  - Why:

## 6. Verification

```bash
dart format -o none --set-exit-if-changed .
flutter analyze
flutter test
```

Manual checks:

- 
- 

## 7. Deferred follow-ups

- 
- 
