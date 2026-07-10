# Version Policy

This skill has a Java 21 baseline because the replaced assessor targeted Java 21, but it is deliberately project-version-aware.

## Source of truth order

1. repository toolchain/release configuration
2. CI and production runtime definitions
3. dependency/BOM/plugin versions
4. repository documentation and tests
5. official documentation for that exact version
6. this skill’s general guidance

When sources conflict, do not silently choose the newest.

## Java features

Classify a proposed feature as:

- available and final in project release
- preview in project release
- unavailable until a later release
- supported by JDK but incompatible with framework/tooling

Preview use requires compiler and runtime flags across build, tests, IDE, CI, and deployment. Never enable preview as a side effect of a refactor.

Java 21 final highlights covered here include records (final since 16), record patterns, pattern matching for switch, sequenced collections, and virtual threads. Structured concurrency and scoped values are preview in Java 21 and changed later.

JDK behavior can change after 21. Example: synchronized-related virtual-thread pinning is addressed by JEP 491 in JDK 24, so diagnostics/remedies must be runtime-specific.

## Quarkus

Read the project’s platform/BOM version. Use versioned Quarkus docs when available. Do not treat the main/SNAPSHOT guide as proof an API exists in the project.

Confirm:

- extension artifact names
- REST stack generation
- test annotation availability
- config key and phase
- supported JDK/GraalVM/Mandrel versions
- deprecated/removed APIs

Keep Quarkus extension versions aligned through the platform unless project policy says otherwise.

## Build plugins and libraries

Check effective Maven/Gradle configuration and dependency graph. Documentation for a latest plugin may not match the wrapper/plugin version. Never add a version merely to make a guessed DSL compile.

## Updating this skill

At least quarterly or before a major release:

1. review `source-index.md`
2. check Agent Skills and Tessl specification changes
3. review supported JDK/Quarkus release guidance
4. run script tests and bundle validator
5. run activation/output evals and Tessl scenarios
6. compare against the previous skill version
7. bump `tile.json`, metadata, and changelog semantically

Prefer removing stale advice to accumulating version tables indefinitely.
