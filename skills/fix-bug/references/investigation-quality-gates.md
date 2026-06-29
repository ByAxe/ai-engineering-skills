# Investigation Quality Gates

Use these gates when a defect is production-facing, security-sensitive, auth/payment/data-related, cross-module, regression-prone, or has unclear root cause. For obvious low-risk local bugs, keep the normal fast path.

These gates augment `bugfix-spec-workflow.md`; they do not replace it. When the user asks for OpenSpec scope or artifacts, preserve the full current/expected/unchanged contract, spec sanity pass, dependency-aware tasks, and defect/correction/unchanged regression matrix from that workflow.

## Depth Routing

Choose the lightest path that fits the risk:

- Fast path: isolated defect, obvious reproduction, local fix, small blast radius.
- Evidence path: root cause unclear, data or provider state involved, previous fixes failed, or reproduction is partial.
- Review path: security/auth/payment/data, production impact, cross-module contract, or broad diff risk.

Do not import a full methodology phase sequence. Take only the mechanics that reduce the current risk: project context, readiness, edge-case hunt, adversarial review, checkpoint/readout.

## Evidence Ledger

Before naming root cause, record enough proof to make the claim reviewable:

| Claim | Evidence to collect |
| --- | --- |
| Defect exists | command, test, route, screenshot, data row, log, or user report with exact condition |
| Root cause | file/function path plus why that path produces the defect |
| Fix scope | why the edit is the smallest shared point that covers affected callers |
| Regression guard | defect proof, correction proof, unchanged proof, and relevant edge cases |

If any row is missing, say what is unproven and narrow the completion claim.

Use this compact note shape when the investigation needs to be reviewable:

```markdown
Risk path: Fast | Evidence | Review
Current: WHEN ... THEN ...
Expected: WHEN ... THEN the system SHALL ...
Unchanged: WHEN ... THEN the system SHALL CONTINUE TO ...

Evidence:
- Defect proof:
- Root cause proof:
- Smallest fix point:
- Regression guard:

Hypotheses:
1. ...
2. ...

Edge cases checked:
- ...

Adversarial findings:
- [supported] ...
- [dismissed] ...

Verification:
- ...

Residual gaps:
- ...
```

## Hypothesis Checks

For unclear defects, keep at least two hypotheses until evidence eliminates them. Prefer checks that are cheap and decisive:

- grep every caller before changing a shared function.
- inspect provider/database/event truth before trusting UI or URL state.
- compare real contract values against mocks when mocks may hide the bug.
- reproduce one failing path before editing, or state why reproduction is blocked.

## Readiness Before Implementation

Do not start code changes on a high-risk defect until these are clear:

- Current, expected, and unchanged behavior are written.
- The changed capability and non-goals are named.
- The root-cause evidence points to a bounded edit.
- The regression matrix has a runnable or explicitly documented proof for each row.
- The repository's local instructions and verification commands have been identified.

## Edge-Case Hunt

Check the branches near the fix, not the whole product:

- missing fallback/default branch
- hostile or absent query params
- stale browser history or bfcache restore
- delayed webhook/provider event
- localization pair mismatch
- auth/session mismatch
- duplicate event or idempotency path
- responsive viewport variant for browser-visible defects

Add the smallest test or evidence that would catch the class of bug again. Do not add broad suites unless the root cause is broad.

## Adversarial Review

Before final verification on review-path bugs, do a short negative pass:

1. Assume the fix is wrong or too broad.
2. List the strongest failure modes with file/function/route references.
3. Keep only findings supported by code, tests, data, or documented contracts.
4. Fix real findings; dismiss unsupported ones in the readout.

This prevents "looks good" review while avoiding forced nitpicks.

## Checkpoint Readout

For a non-trivial diff, prepare the review order:

- root cause evidence
- contract/spec delta
- implementation files
- regression tests
- verification output
- residual gaps

If verification cannot run, report the exact command, reason, and residual risk.
