# Go Refactor Report Template

## Goal
- Desired outcome:
- Scope:
- Compatibility constraints:

## Smells found
- Smell:
  - Evidence:
  - Risk:
  - Root cause:

## Refactor plan
1.
2.
3.

## Patch summary
- Files changed:
- Public API changes:
- Ownership/lifecycle changes:

## Verification
```text
gofmt -l .
go test ./...
go test -race ./...
go vet ./...
staticcheck ./...   # if available
golangci-lint run   # if configured
```

## Risk notes
- Compatibility:
- Concurrency:
- Performance:
- Rollout:

## Follow-ups
- Deferred improvement:
- Cleanup ticket:
