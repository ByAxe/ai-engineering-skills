# Testing and Maintainability Smells for Frontend TypeScript

## Contents
- T-01 Snapshot test overuse
- T-02 Testing implementation details
- T-03 Flaky async and timer tests
- T-04 Mocking too much and losing confidence
- T-05 No tests around extracted logic after refactor
- T-06 Missing contract tests for adapters and mappers
- T-07 Inconsistent test data builders
- Refactor-safe testing strategy
- Checklist

---

## T-01 Snapshot test overuse

### Symptoms
- Large snapshots for complex components.
- Frequent snapshot updates without understanding changes.

### Refactor strategy
- Keep snapshots small and stable.
- Prefer interaction and assertion-based tests for behavior.

---

## T-02 Testing implementation details

### Symptoms
- Tests assert on internal component state instead of user-visible output.
- Tests break after refactor without behavior change.

### Refactor strategy
- Test through the public surface:
  - rendered output
  - user events
  - accessibility roles and labels

---

## T-03 Flaky async and timer tests

### Symptoms
- Tests pass locally but fail in CI.
- Timing-sensitive assertions.

### Refactor strategy
- Use deterministic async patterns:
  - await stable UI states
  - avoid arbitrary sleeps
  - control timers with fake timers where appropriate

---

## T-04 Mocking too much and losing confidence

### Symptoms
- Mocking internal modules makes tests meaningless.
- Most logic is mocked away.

### Refactor strategy
- Mock only external boundaries:
  - network layer
  - storage
  - time
- Keep internal logic real.

---

## T-05 No tests around extracted logic after refactor

### Symptoms
- Refactor extracts helpers/hooks but no new tests cover them.
- Risk increases because behavior is spread across modules.

### Refactor strategy
- Add focused unit tests for extracted pure helpers.
- Keep integration tests for the full feature.

---

## T-06 Missing contract tests for adapters and mappers

### Symptoms
- API response changes break UI in unexpected places.
- Types drift from runtime payloads.

### Refactor strategy
- Add a contract test for the mapper:
  - given API payload sample
  - produces domain model
- Ensure failure mode is explicit.

---

## T-07 Inconsistent test data builders

### Symptoms
- Each test hand-writes objects with random shapes.
- Type assertions in tests to silence errors.

### Refactor strategy
- Create small builders and fixtures.
- Keep them typed and reusable.

---

## Refactor-safe testing strategy

When refactoring:
1. Identify behavior that must not change.
2. Add a minimal regression test if none exists.
3. Refactor in small steps with tests passing after each.
4. Prefer testing:
   - state transitions for reducers/hooks
   - rendering for presentational components
   - integration for full flows

---

## Checklist

- [ ] Tests cover the risky part of the change.
- [ ] Tests assert behavior, not internals.
- [ ] Async tests are deterministic.
- [ ] Contract tests exist for boundary mappers where relevant.
- [ ] No new `any` introduced in tests.
