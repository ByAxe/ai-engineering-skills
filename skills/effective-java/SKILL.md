---
name: effective-java
description: Engineers, reviews, debugs, refactors, and modernizes production Java and Quarkus code with evidence-first safeguards. Use for Java 21 or JVM backend work; Maven or Gradle builds; API, modeling, collections, concurrency, persistence, testing, security, or performance changes; and Quarkus CDI, Jakarta REST, REST Client, Panache or Hibernate, Mutiny, messaging, configuration, virtual threads, native images, and Spring-to-Quarkus migrations. Not for Kotlin-only, Android, or non-Java projects.
license: MIT
metadata:
  author: ByAxe
  version: "1.0.0"
  category: software-development
  baseline: "Java 21; the project-configured release wins"
  frameworks: "Java SE, Quarkus"
---

# Effective Java Engineering

Engineer Java as a repository-aware maintainer, not as a snippet generator. Preserve behavior unless the requested change says otherwise, make the smallest defensible patch, and prove claims with code, build output, tests, or documented contracts.

## Non-negotiable rules

1. **Inspect before prescribing.** Read the wrapper, root build, module build, Java release or toolchain, dependency management, Quarkus BOM and extensions, source layout, generated-source rules, test conventions, and nearby code before editing.
2. **The repository is the version source of truth.** Never import an API, annotation, plugin, JDK feature, or Quarkus convention merely because it is current elsewhere. Confirm it exists in the configured JDK and dependency graph.
3. **Do not hide behavior changes inside cleanup.** Treat equality, hashing, ordering, mutability, nullability, serialization, HTTP payloads, exception types, transaction scope, thread selection, persistence timing, time zones, and logging as contracts.
4. **Do not edit generated output.** Find and change the generator, schema, annotation processor input, OpenAPI definition, migration source, or template. Verify regeneration when relevant.
5. **Avoid drive-by churn.** No unrelated formatting, dependency upgrades, package moves, framework migrations, public API changes, or abstraction layers without a demonstrated need.
6. **Use existing project tools first.** Prefer the checked-in Maven or Gradle wrapper, configured formatter, static analyzers, test fixtures, and Quarkus plugins. Do not silently install or replace them.
7. **Never claim an unrun gate passed.** State the exact command, result, and any environmental limitation.
8. **Heuristic scanner findings are candidates, not proof.** Inspect the semantic context before changing code.

## Workflow

### 1. Classify the task and risk

Choose the lightest mode that fits:

- **Implement:** add or change behavior.
- **Fix:** reproduce or characterize a defect, then patch the root cause narrowly.
- **Refactor:** preserve externally observable behavior while improving structure.
- **Assess or review:** produce evidence-backed findings without changing code unless asked.
- **Modernize:** adopt a newer Java or Quarkus capability only after compatibility checks.
- **Optimize:** measure first; preserve correctness and operational contracts.

Raise scrutiny for security, authorization, money, data loss, concurrency, transactions, public APIs, schema migrations, native images, or cross-module changes.

### 2. Establish the project profile

Run when repository access is available:

```bash
python3 scripts/profile_java_project.py . --format markdown
```

Confirm manually:

- wrapper and build system; multi-module boundaries
- configured Java release, toolchain, preview flags, and CI JDK
- Quarkus platform/BOM version and installed extensions
- blocking, reactive, coroutine, or virtual-thread execution model per entry point
- test layers, formatter, static analysis, coverage, and native target
- generated directories, migrations, API schemas, and public contracts

Do not force Java 21 onto a project that targets another release. Java 21 guidance in this skill is a capability reference, not an upgrade mandate. Read `references/version-policy.md` for version-sensitive work.

### 3. Capture contracts before editing

Write down the relevant invariants:

- current and requested behavior
- inputs, outputs, failure modes, and side effects
- null, empty, duplicate, ordering, locale, time-zone, and numeric rules
- transaction, retry, idempotency, cancellation, timeout, and concurrency behavior
- HTTP, event, database, serialization, and public API compatibility
- unchanged behavior that must remain protected

For a risky refactor, use `assets/refactor-plan-template.md`. For an assessment, use `assets/assessment-template.md`.

### 4. Read only the references the task needs

Start with `references/00-reference-router.md`. Load focused references when their trigger is present; do not ingest the entire pack by default.

High-value routes:

| Trigger | Read |
|---|---|
| agent-generated or suspiciously broad patch | `references/agent-failure-modes.md`, `references/evidence-first-workflow.md` |
| records, sealed types, patterns, `var`, language modernization | `references/modern-java-language-and-modeling.md` |
| nullness, `Optional`, generics, API shape | `references/api-design-nullness-and-generics.md` |
| collections, streams, mutability, ordering | `references/collections-streams-and-mutability.md` |
| equality, `BigDecimal`, arrays, time, locale | `references/equality-ordering-numerics-and-time.md` |
| exceptions, resources, files, HTTP, serialization | `references/exceptions-resources-io-and-serialization.md` |
| threads, futures, reactive code, virtual threads | `references/concurrency-virtual-threads-and-async.md` |
| Maven, Gradle, annotation processing, generated code | `references/build-maven-gradle-and-generated-code.md` |
| tests, mocks, debugging | `references/testing-debugging-and-test-doubles.md` |
| auth, validation, secrets, injection, unsafe input | `references/security-input-boundaries-and-secrets.md` |
| JPA, Hibernate, transactions, migrations | `references/persistence-jpa-and-transactions.md` |
| Quarkus work | the Quarkus entry point plus the area-specific file selected by `references/00-reference-router.md` |
| Spring-shaped code in Quarkus | `references/spring-to-quarkus-migration.md` |
| broad cleanup or review | `references/smell-and-refactoring-catalog.md`, `references/review-checklists.md` |

### 5. Form an evidence-backed plan

For each proposed change, record:

- evidence: file, symbol, failing test, trace, metric, or contract
- risk removed or behavior introduced
- smallest change surface
- tests or checks that prove the change
- compatibility and rollback implications

Prefer vertical, independently verifiable batches. Resolve correctness and security before readability; readability before speculative optimization.

### 6. Implement with Java-specific discipline

Apply these defaults unless repository conventions or measured constraints justify otherwise:

- model domain concepts with explicit types; do not replace a clear type with `Map<String, Object>` or strings
- use records only for transparent data carriers whose generated equality and component exposure are correct
- use sealed hierarchies only when the variant set is intentionally closed
- make mutability and ownership explicit; return defensive or immutable copies when that is the contract
- use `Optional` mainly for possibly absent return values, not as a universal field or parameter type
- keep stream pipelines side-effect-free and readable; use loops when state, early exits, checked failures, or debugging are clearer
- preserve causes and interruption; do not swallow, log-and-rethrow, or catch `Throwable` casually
- set charsets, timeouts, locale, zone, rounding, and resource lifetime explicitly at boundaries
- do not introduce parallel streams, executors, virtual threads, reactive types, or caches without an execution and lifecycle model
- prefer composition and focused concrete classes over one-interface-per-class, generic base services, builders for trivial objects, or ceremonial layers
- do not add a dependency for functionality the JDK or existing stack already provides adequately

Read the focused reference before applying a rule mechanically; each has legitimate exceptions.

### 7. Apply Quarkus semantics when present

First identify the actual Quarkus version and extensions. Then:

- use `jakarta.*` APIs and Quarkus-native facilities supported by that project
- keep REST resources transport-focused and place business transaction boundaries deliberately
- distinguish event-loop, worker-thread, reactive, and virtual-thread execution; never hide blocking work on an event loop
- use constructor injection for required dependencies where proxy and framework constraints allow it
- treat CDI discovery, scopes, qualifiers, interception, bean removal, and build-time augmentation as semantic behavior
- distinguish build-time-fixed configuration from runtime-overridable configuration
- keep ORM and Hibernate Reactive models consistent; do not mix blocking and reactive persistence casually
- keep entities out of public transport contracts unless that coupling is an explicit accepted design
- validate JVM behavior and native behavior separately when native is a production target

Use `references/quarkus-project-model-and-build-time.md` as the Quarkus entry point.

### 8. Validate in widening circles

Use the narrowest useful gate after each batch, then widen:

1. compile or test-compile the touched module
2. focused unit or component tests
3. affected integration or contract tests
4. formatter and configured static analysis
5. module or repository `test`/`check`/`verify`
6. Quarkus integration/native build only when the changed surface or production target requires it

The helper is non-destructive and wrapper-first:

```bash
scripts/run_quality_gates.sh --root . --mode compile
scripts/run_quality_gates.sh --root . --mode test
scripts/run_quality_gates.sh --root . --mode verify
```

Before finalizing, inspect patch scope:

```bash
python3 scripts/check_diff_scope.py .
python3 scripts/scan_java_risks.py . --format markdown
```

Fix confirmed regressions, re-run the failed gate, and stop only when the relevant evidence is green or the limitation is explicitly reported.

## Agent failure traps to reject immediately

- invented imports, annotations, Maven coordinates, Gradle DSL, or Quarkus properties
- replacing working imperative code with nested streams merely to appear modern
- converting mutable entities or identity-bearing objects to records
- adding `default` to a sealed-type switch and thereby hiding future exhaustiveness checks
- changing `Collectors.toList()` to `Stream.toList()` without checking mutability
- using record components that are mutable arrays or collections without handling equality and ownership
- using `BigDecimal(double)`, comparing monetary values with `equals` unintentionally, or omitting rounding policy
- using system-default charset, locale, or time zone in a contract
- adding `parallelStream()`, `CompletableFuture.supplyAsync`, or a new executor without ownership, bounds, cancellation, and context analysis
- pooling virtual threads or assuming they make CPU-bound work faster
- adding retries to non-idempotent work
- moving a transaction boundary without checking lazy loading, flush timing, locks, events, and error translation
- field-injecting every Quarkus bean, using `@Named` as a qualifier by habit, or assuming every class is discoverable by CDI
- returning JPA entities from REST because it is convenient
- fixing native-image reflection by registering whole packages before identifying the exact reflective access
- deleting code that appears unused without checking reflection, service loading, CDI, serialization, configuration, or generated references
- tests that mock the subject under test, assert implementation details, sleep for timing, or pass while the real boundary is untested

Read `references/agent-failure-modes.md` for the full taxonomy and countermeasures.

## Output contracts

### Assessment or review

Use `assets/assessment-template.md`. Every finding must include severity, confidence, evidence, violated contract or risk, smallest remedy, and verification. Separate confirmed defects from design trade-offs and heuristic candidates.

### Refactor or implementation

Use `assets/implementation-report-template.md`. Report changed behavior, preserved behavior, files changed, key decisions, exact gates run and results, and residual risk. Do not narrate every edit.

### Plan only

Use `assets/refactor-plan-template.md`. Make batches dependency-aware and attach a verification command or observable proof to every batch.

## Completion definition

A Java task is complete only when:

- the patch matches the requested scope
- relevant behavior and compatibility contracts are explicit
- no generated artifact or unrelated file was edited accidentally
- imports and APIs exist in the configured project versions
- relevant tests and build gates passed, or the exact blocker is disclosed
- concurrency, transaction, security, and Quarkus execution implications were checked where applicable
- the final report distinguishes facts, inferences, and unverified candidates
