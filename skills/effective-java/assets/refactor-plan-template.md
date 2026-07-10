# Effective Java Refactor Plan

## Intent

- Problem or requested outcome:
- Refactor / fix / modernization / optimization:
- Behavior that may change:
- Behavior that must not change:
- Out of scope:

## Project profile

- Java release/toolchain:
- Maven/Gradle wrapper and modules:
- Quarkus/platform/extensions, if present:
- Execution model:
- Persistence/transaction model:
- Public/wire/schema contracts:
- Generated sources/source of truth:
- Deployment targets:

## Baseline evidence

| Evidence | Command/location | Result |
|---|---|---|
| build/test |  |  |
| failing behavior/characterization |  |  |
| static analysis/profile |  |  |

## Contract matrix

| Dimension | Current | Target | Must remain unchanged? | Proof |
|---|---|---|---|---|
| input/null/empty |  |  | yes/no |  |
| output/order/mutability |  |  |  |  |
| equality/numeric/time |  |  |  |  |
| error/status/logging |  |  |  |  |
| transaction/side effects |  |  |  |  |
| concurrency/cancellation |  |  |  |  |
| serialization/API/schema |  |  |  |  |

## Evidence ledger

| Claim | Evidence | Confidence | Decisive next check |
|---|---|---|---|
|  |  |  |  |

## Batches

### Batch 1 — Characterize and establish seam

- **Depends:** baseline
- **Files/symbols:**
- **Change:**
- **Reason:**
- **Compatibility:**
- **Verify:**
- **Rollback:**
- **Do not include:**

### Batch 2 — Smallest semantic/structural change

- **Depends:** Batch 1
- **Files/symbols:**
- **Change:**
- **Reason:**
- **Compatibility:**
- **Verify:**
- **Rollback:**

Add batches only when independently verifiable.

## Quarkus-specific decisions, if applicable

- build-time versus runtime config:
- CDI discovery/scope/qualifier/interceptor:
- event-loop/worker/virtual thread:
- blocking versus reactive persistence:
- transaction completion:
- packaged/native proof:

## Verification ladder

1. compile/test-compile touched module:
2. focused unit/component tests:
3. affected integration/contract tests:
4. formatter/static analysis:
5. module/repository test/check/verify:
6. packaged/native/load/security gate when required:

## Rollout and rollback

- deployment order:
- schema/config compatibility window:
- feature flag only if needed and runtime-safe:
- monitoring signal:
- rollback or forward-fix:

## Completion conditions

- [ ] Each batch has observable proof.
- [ ] Public and semantic contracts are protected.
- [ ] No unrelated churn or generated edits.
- [ ] Versioned APIs compile in the repository.
- [ ] Unrun gates and residual risks are explicit.
