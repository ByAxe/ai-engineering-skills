# Toolchain, Analyzers, and Quality Gates

## Contents
- Baseline gates
- Recommended analyzers
- Formatting and imports
- Static analysis strategy
- Version-gated modernization
- CI recommendations

## Baseline gates

For most Go repositories, a strong baseline is:
- formatting check
- `go test ./...`
- `go test -race ./...` when supported and relevant
- `go vet ./...`

These catch a surprising amount of real risk.

## Recommended analyzers

### Staticcheck
Use for correctness and style issues beyond `go vet`.
Treat it as a high-value default for mature repos.

### golangci-lint
Useful as a runner and policy layer when the repo needs multiple analyzers.
Enable rules intentionally; do not turn on everything blindly without tuning noise.

### gopls analyzers
Editors already surface useful diagnostics. Modernization and simplification suggestions from language-server analyzers can help identify dead patterns and version-appropriate cleanup opportunities.

## Formatting and imports

Formatting should be non-negotiable.
Use `gofmt` as the floor. `goimports` can help maintain imports automatically where teams use it.

Formatting smells:
- hand-aligned code
- inconsistent import groups
- style debates solved by anything other than the toolchain

## Static analysis strategy

Use this order:
1. `go vet`
2. Staticcheck
3. repo-specific lints via golangci-lint if configured

Then review findings by category:
- correctness first
- lifecycle and resource safety second
- style last

Do not let pedantic style noise hide real bugs.

## Version-gated modernization

Only recommend these when the repository toolchain supports them and the change is worth it:
- newer benchmark APIs that reduce benchmark footguns
- deterministic concurrency test facilities for hard concurrent code
- newer filesystem safety APIs for traversal-resistant boundaries
- modernize or fix tools that simplify older patterns

State version assumptions explicitly when suggesting any of these.
For specific examples and upgrade guidance, see `references/version-gated-modernization.md`.

## CI recommendations

A practical default CI sequence:
1. format check
2. unit tests
3. race tests for packages where concurrency matters
4. `go vet`
5. Staticcheck or configured lint runner
6. optional benchmark or fuzz jobs on targeted packages

For public libraries, also review:
- exported surface changes
- documentation examples
- compatibility notes
