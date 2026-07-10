# Build, Maven, Gradle, and Generated Code

The build is executable architecture. Agents must read it before choosing APIs or verification commands.

## Wrapper first

Prefer checked-in `./mvnw` or `./gradlew`. A system Maven/Gradle may resolve a different plugin/tool version. Check wrapper files are complete and executable; do not regenerate or upgrade them during unrelated work.

## Java release and toolchains

Find the effective setting, not just one property:

- Maven compiler `release`, `source`/`target`, parent/plugin management, profiles, and toolchains
- Gradle Java toolchain/language version, `options.release`, convention plugins, and subproject overrides
- CI matrix and runtime image
- test/native toolchain

`--release` constrains language/API targeting more reliably than source/target alone. Do not use host-JDK APIs that are absent from the configured release.

## Maven workflow

Inspect:

- parent and dependency management/BOM imports
- reactor modules and profiles
- plugin management versus actual plugin executions
- annotation processors
- Surefire versus Failsafe test phases/patterns
- generated-source plugins
- enforcer, formatter, static analysis, coverage

Useful diagnostics, when appropriate:

```bash
./mvnw help:effective-pom
./mvnw dependency:tree
./mvnw -pl :module -am test
./mvnw -DskipTests compile
./mvnw verify
```

`-DskipTests` normally skips execution but still permits test compilation in many Maven setups; `-Dmaven.test.skip=true` is stronger. Use the repository’s documented commands and inspect custom profiles.

## Gradle workflow

Inspect:

- `settings.gradle(.kts)` and included builds
- convention plugins/build logic
- version catalogs/platforms
- task graph and source sets
- toolchains
- annotation processors (`annotationProcessor`)
- dependency locking/verification
- test suites and custom integration tasks

Useful diagnostics:

```bash
./gradlew projects
./gradlew tasks
./gradlew dependencies
./gradlew test
./gradlew check
```

Do not assume `build` and `check` include every custom integration/native task. Use `--dry-run` or task reports to understand the graph when needed.

## Dependency management

- keep Quarkus extensions aligned through the project’s Quarkus platform/BOM
- do not pin an extension version independently without a documented reason
- distinguish compile/runtime/test scopes/configurations
- inspect conflicts before forcing versions
- update lockfiles/catalogs using the owning tool, not manual guesses
- avoid dynamic/range versions in reproducible production builds unless policy explicitly uses them

A compile error after an import is not proof that a new dependency should be added; first verify the intended API and version.

## Annotation processing and code generation

Identify generators such as:

- Lombok
- MapStruct
- JPA metamodel
- OpenAPI/client generation
- protobuf/Avro
- jOOQ
- Immutables/AutoValue
- Quarkus augmentation

Edit the source schema/template/annotations/configuration. Generated directories often include `target/generated-sources`, `build/generated`, or custom paths. Do not hand-edit them unless the repository explicitly treats generated code as vendored source.

When changing generator inputs:

1. record generator/plugin version
2. regenerate with the repository command
3. review generated diff for unintended churn
4. compile consumers
5. preserve deterministic output

## Lombok and generated semantics

A small annotation change can alter constructors, null checks, equality, builders, logging fields, and framework access. Inspect delomboked/generated behavior or compile tests; do not reason from annotation names alone.

## Multi-module changes

Determine:

- upstream and downstream modules
- published API boundaries
- test fixtures
- dependency convergence
- module-specific Java releases
- Quarkus application module versus plain library modules

Compile affected dependents. A leaf module’s green test does not prove a changed shared API is compatible.

## Profiles and environments

Profiles can change dependencies, plugins, generated sources, tests, and Quarkus build-time configuration. Do not activate a profile by habit. State which profile was used and why.

## Build-file edit discipline

A build edit deserves the same review as production code:

- minimal location
- property/version source respected
- no duplicate dependency/plugin declaration
- scope correct
- repository policy and formatting preserved
- dependency tree checked
- offline/CI/native implications considered

Separate upgrades from feature/refactor work when possible.

## Quality tools

Use configured tools before adding new ones. Common categories:

- formatting: Spotless, google-java-format, Checkstyle
- bug finding: Error Prone, SpotBugs, PMD
- nullness: NullAway, Checker Framework, JSpecify-aware tools
- architecture/dependencies: ArchUnit, Maven Enforcer, dependency analysis
- coverage/mutation: JaCoCo, PIT

A tool warning is evidence to investigate, not permission for a behavior-changing rewrite.

## Reproducibility checklist

- wrapper used
- JDK/toolchain recorded
- no unreviewed network/version drift
- generated sources deterministic
- relevant profile named
- test discovery confirmed
- build cache/stale-output concerns handled deliberately
- exact command and exit result reported
