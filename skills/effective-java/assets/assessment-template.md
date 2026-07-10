# Effective Java Assessment

## Scope

- Repository/module:
- Requested mode: assess / review / refactor candidate / modernization candidate
- Java release/toolchain:
- Build system/wrapper:
- Quarkus version/platform/extensions, if present:
- Deployment targets: JVM / container / native
- Commands run and baseline result:
- Constraints and public contracts:

## Executive summary

Summarize the top three to five risks, not every style observation. State whether the code is safe to change now and what evidence is missing.

## Confidence vocabulary

- **Confirmed defect:** reproduced or directly violates an authoritative contract.
- **High-confidence risk:** code/execution evidence makes failure likely, but trigger was not reproduced.
- **Candidate:** heuristic or smell requiring semantic inspection.
- **Preference:** legitimate design trade-off, not a defect.

## Findings

### EJ-001 — Finding title

- **Classification:** confirmed defect / high-confidence risk / candidate / preference
- **Severity:** critical / high / medium / low
- **Confidence:** high / medium / low
- **Category:** Java semantics / API / collections / concurrency / persistence / security / build / test / Quarkus / maintainability
- **Evidence:** `path/File.java:line`, symbol, command output, trace, metric, or contract
- **Observed behavior:**
- **Expected or protected contract:**
- **Impact and trigger:**
- **Why this is not merely stylistic:**
- **Smallest remedy:**
- **Verification:** exact test/command/observable proof
- **Compatibility/rollback:**
- **Legitimate exception considered:**

Repeat only for evidence-backed findings.

## Risk-ranked summary

| Rank | ID | Severity | Confidence | Contract/risk | Suggested batch |
|---:|---|---|---|---|---|
| 1 | EJ-001 | high | high |  | 1 |

## Target shape

Describe the smallest coherent target, including what should remain unchanged. Reject unnecessary layers or framework migration explicitly.

## Staged plan

| Batch | Depends on | Change surface | Risk removed | Verification | Rollback point |
|---:|---|---|---|---|---|
| 1 | baseline |  |  |  |  |

## Gate matrix

| Gate | Command | Result | Evidence/notes |
|---|---|---|---|
| baseline build/test |  | passed / failed / not run |  |
| focused tests |  |  |  |
| static analysis/format |  |  |  |
| integration/package/native |  |  |  |

Never mark an unrun gate as passed.

## Deferred items

List lower-value or out-of-scope opportunities. Explain why they are deferred. Do not turn this into a generic backlog.

## Residual risk and unknowns

Name environment limits, missing production evidence, unavailable dependencies, or contracts that need an owner decision.
