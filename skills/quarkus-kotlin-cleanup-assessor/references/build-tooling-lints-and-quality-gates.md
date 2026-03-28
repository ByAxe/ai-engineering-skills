# Build Tooling, Linters, and Quality Gates

This guide defines the cleanup validation surface.

## Minimum Useful Validation

For a typical repository, try to keep these green:

- format
- tests
- static analysis
- service build
- native build when applicable

## Common Commands

### Maven

- `./mvnw -q test`
- `./mvnw verify`
- `./mvnw quarkus:dev`
- `./mvnw install -Dnative` when native verification is required

### Gradle

- `./gradlew test`
- `./gradlew build`
- `./gradlew --console=plain quarkusDev`
- `./gradlew build -Dquarkus.native.enabled=true` when native verification is required

## Kotlin Quality Gates

Good additions when present:

- `detekt`
- `ktlint` or formatter workflow driven by `.editorconfig`
- warnings elevated appropriately in CI
- no permanent “ignore everything” baselines unless there is a phased cleanup plan

## Detekt

Detekt is strong for catching:

- long methods
- too many functions per file or class
- magic numbers
- exception handling smells
- complexity growth
- Kotlin-specific code smells

Use `assets/detekt.quarkus-kotlin-cleanup.sample.yml` as a starter, then adapt it to the repository’s version and tolerance.

## `.editorconfig`

Keep Kotlin formatting rules centralized in `.editorconfig` where the chosen formatter supports it.

Use `assets/editorconfig.kotlin-quarkus-cleanup.sample` as a starter.

## CI Order

A practical order:

1. dependency resolution
2. format or formatting verification
3. static analysis
4. unit tests
5. component and integration tests
6. build artifact
7. native build or native tests if required

## Quality Gate Review Questions

- Is formatting automatic and predictable?
- Is static analysis catching real cleanup risks?
- Are warnings and failures aligned with team goals?
- Is native validation included only when meaningful?
