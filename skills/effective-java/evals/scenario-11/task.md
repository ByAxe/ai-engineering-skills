# Task

A three-line null-handling defect in a Java service received a 1,400-line patch. The patch adds six one-implementation interfaces, three builders for simple immutable values, a mapping framework dependency, a Java/Quarkus version upgrade, repository-wide formatting, and interaction-heavy mocks. It deletes the original failing test because it was "too coupled" and replaces it with tests that mock the service under test. The author says all checks pass but provides no command output.

Create `patch-scope-review.md` with a root-cause reconstruction, keep/revert/change decision for each patch cluster, a minimal replacement patch plan, regression strategy, diff-scope checks, and exact verification requirements.
