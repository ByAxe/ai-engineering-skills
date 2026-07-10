# Evidence-First Java Workflow

Use this procedure for fixes, risky refactors, reviews, and ambiguous implementation tasks.

## 1. Establish a reproducible baseline

Capture:

- repository commit or working-tree state
- build tool and wrapper
- JDK used locally and JDK configured by toolchain/release
- relevant module and dependency graph
- exact baseline command and exit status
- existing failures unrelated to the task

Do not run `clean` automatically before collecting evidence; stale-output suspicion is a reason to run it deliberately, not a default that erases useful state.

## 2. Build a contract matrix

| Dimension | Current | Requested | Must remain unchanged | Proof |
|---|---|---|---|---|
| functional result | | | | test/example |
| failure behavior | | | | exception/status |
| null/empty/duplicate | | | | boundary cases |
| order/mutability | | | | assertions |
| public/wire contract | | | | schema/contract test |
| transaction/data | | | | integration test |
| concurrency/time | | | | deterministic test/trace |
| security/authorization | | | | negative test |
| operational behavior | | | | log/metric/health/build |

Omit irrelevant rows, but do not omit a row merely because the expected behavior is unknown; mark it unknown and investigate.

## 3. Maintain an evidence ledger

For each material conclusion, record:

```text
Claim: OrderService double-charges after timeout retry.
Evidence: failing test X; trace IDs Y/Z; call site A retries POST without idempotency key.
Confidence: confirmed / high / candidate.
Alternative explanations checked: client duplicate submission; message redelivery.
Change implication: retry policy or idempotency boundary, not a formatting refactor.
```

A line match, static analyzer warning, or intuition is evidence of a candidate, not automatically of the runtime claim.

## 4. Use competing hypotheses for unclear failures

Keep at least two plausible explanations until a cheap discriminating check eliminates one. Examples:

- missing transaction versus serialization after transaction
- event-loop blocking versus downstream latency
- entity equality bug versus detached instance lifecycle
- stale generated source versus wrong dependency version
- test race versus production race

Choose checks that separate hypotheses, not checks that merely repeat the failure.

## 5. Define the smallest defensible change

A good change plan states:

- exact files/symbols
- why each file is necessary
- contract changed or preserved
- generated/source-of-truth relationship
- dependency or configuration impact
- rollback path
- verification command

Split structural movement, behavior change, build change, and framework migration into separate batches whenever possible.

## 6. Implement one semantic cluster at a time

Recommended order:

1. reproduce or characterize
2. add/adjust a focused test where feasible
3. implement root-cause change
4. compile touched module
5. run focused test
6. inspect diff
7. widen gates

Do not accumulate a large patch before the first compile.

## 7. Validate claims at the right layer

| Claim | Minimum useful evidence |
|---|---|
| syntax/type correctness | repository compiler on configured release |
| pure business behavior | unit or property/parameterized test |
| CDI/interceptor/config behavior | component or Quarkus test |
| HTTP contract | endpoint/contract test |
| persistence/transaction behavior | database-backed integration test |
| built artifact behavior | integration test against packaged app |
| native compatibility | native build/test for changed surface |
| performance | representative benchmark/profile before and after |
| security control | negative/abuse test plus configuration review |

A unit test cannot prove a native reflection configuration, and a native build alone cannot prove authorization behavior.

## 8. Handle unavailable gates honestly

Report:

- exact command attempted
- why it could not complete
- what narrower evidence did complete
- residual risk
- command the maintainer should run in the proper environment

Never substitute “looks correct” for a failed or unavailable build.

## 9. Final adversarial pass

Assume the patch is wrong or too broad. Check:

- hidden behavior changes
- tests that would pass before the fix
- missing negative paths
- version/API mismatch
- changed generated output
- new dependency or executor ownership
- transaction/event-loop/native implications
- secrets or sensitive logs
- accidental public API/wire/schema changes

Keep only findings supported by evidence.

## Output distinction

Use explicit labels:

- **Observed:** directly seen in code/output.
- **Inferred:** reasoned from observed facts; explain the inference.
- **Unverified:** plausible but not tested.
- **Deferred:** intentionally outside scope with reason.
