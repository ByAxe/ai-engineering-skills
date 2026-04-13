# Version-Gated Modernization Opportunities

## Contents
- How to use this file
- Go 1.24+ opportunities
- Go 1.25+ opportunities
- Go 1.26+ opportunities
- Editor and analyzer modernization
- Upgrade decision rules

## How to use this file

Use this file only when the repository's supported toolchain matters.
Do not recommend version-gated changes casually.

Decision order:
1. Is the repo already on a toolchain that supports the feature?
2. Does the feature remove a real smell, bug class, or maintenance burden?
3. Is the migration smaller than the ongoing cost of the old pattern?

## Go 1.24+ opportunities

### `testing.B.Loop` for benchmarks
Use when the repository supports a toolchain that includes the newer benchmark loop API.

Good fit when:
- existing benchmarks are easy to get wrong
- benchmark bodies need clearer setup/measurement separation
- the team is actively improving benchmark quality

Do not migrate every benchmark just for fashion. Use it where it improves clarity or removes benchmark footguns.

### `os.Root` for traversal-resistant file boundaries
Use when code must constrain file operations to a specific root and the supported toolchain includes the newer filesystem root API.

Good fit when:
- path traversal risk is real
- the code handles user-controlled path components
- boundary semantics are security-sensitive

### `testing/synctest` as experiment
In the 1.24 line, deterministic concurrency testing support existed behind an experiment.
Use only if the repository explicitly opts into that setup and the benefit is worth the complexity.

## Go 1.25+ opportunities

### `testing/synctest` for deterministic concurrent tests
For repositories on a toolchain with general-availability support, this can be a major improvement over sleep-driven concurrent tests.

Good fit when:
- tests rely on `time.Sleep`
- concurrent logic is timing-sensitive
- shutdown, timeout, or `Context` logic is hard to test reliably

### General modernization review
When a repo reaches this toolchain range, it is worth reviewing whether older homegrown test and scheduling patterns can be simplified away.

## Go 1.26+ opportunities

### Newer `go fix` modernization support
If the repository uses a toolchain with the newer `go fix` modernization behavior, it may be able to simplify older patterns automatically or semi-automatically.

Use this when:
- you want to modernize broadly after verifying toolchain support
- you want machine-assisted cleanup before doing manual design refactors

Do not trust tool-driven modernization blindly. Review API and behavioral implications carefully.

## Editor and analyzer modernization

Even without changing code manually, newer analyzers may identify cleanup opportunities such as:
- version-appropriate simplifications
- outdated idioms
- benchmark modernization
- context and lifecycle footguns

Use these suggestions as prompts, not commands.

## Upgrade decision rules

Recommend a version-gated refactor only when at least one is true:
- it removes a real bug class
- it materially improves test reliability
- it reduces security risk at a boundary
- it substantially lowers maintenance cost

When suggesting it, always state:
- minimum supported Go version
- whether the change is optional or strategic
- fallback guidance for older toolchains
