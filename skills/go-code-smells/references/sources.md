# Sources and Further Reading

## Contents
- Skill authoring guidance
- Official Go guidance
- Go testing and review guidance
- Tooling and analyzers
- Performance and observability
- Security and boundary guidance
- Community style guides

## Skill authoring guidance

- Anthropic, *The Complete Guide to Building Skills for Claude*
- Anthropic, *Skill authoring best practices*

## Official Go guidance

- Go Wiki: Code Review Comments
- Effective Go
- Package names
- Go Modules Reference
- Organizing a Go module
- Managing module source
- Keeping Your Modules Compatible
- Working with Errors in Go 1.13
- Errors are values
- Contexts and structs
- Go Concurrency Patterns: Context
- Data Race Detector
- Go Fuzzing
- Traversal-resistant file APIs
- More predictable benchmarking with testing.B.Loop
- Testing concurrent code with testing/synctest
- Testing Time (and other asynchronicities)
- Structured Logging with slog

## Go testing and review guidance

- Go Wiki: Go Test Comments
- `cmp` and `cmpopts` package docs where semantic comparison helps

## Tooling and analyzers

- `go vet`
- Staticcheck checks and configuration docs
- golangci-lint documentation
- gopls analyzer and modernization docs
- `go fix` / modernize guidance where toolchain support is relevant

## Performance and observability

- `go tool pprof`
- `go tool trace`
- benchmark and profile documentation from the Go toolchain
- PGO guidance for supported toolchains

## Security and boundary guidance

- `database/sql` docs: transactions, cancellation, queries, prepared statements, SQL injection avoidance
- `net/http` docs on response body lifecycle
- `encoding/json` docs including strict-decoding options
- `crypto/rand` and secure-randomness guidance

## Community style guides

- Google Go Style Guide / Best Practices
- Uber Go Style Guide

## Notes on version-gated guidance

Some modernization advice in this skill is intentionally version-gated. When using:
- newer benchmark APIs
- deterministic concurrency test packages
- newer filesystem boundary APIs
- newer `go fix` or analyzer features

state the minimum supported toolchain clearly before recommending the change.
