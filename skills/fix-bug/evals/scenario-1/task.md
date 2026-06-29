# Task

A tester reports that opening `/payment/result/?state=paid` with no trusted order status can show success-oriented payment copy. Payments are live, so the user wants a small bugfix spec before code changes. Pending, canceled, failed, retry, and delayed-webhook flows must keep working.

Create `payment-result-advisory-bugfix-plan.md` with the OpenSpec-compatible bugfix analysis, proposed design, task sequence, capability delta, and regression coverage. The grading expects that file as the solution artifact.
