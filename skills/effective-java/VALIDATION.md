# Validation Record

Validation date: **2026-07-10**

This record distinguishes checks actually run in the construction environment from external checks that remain the installer’s responsibility.

## Completed offline checks

The bundle was checked with:

```bash
PYTHONPYCACHEPREFIX=/tmp/effective-java-pyc python3 -m py_compile scripts/*.py tests/*.py
bash -n scripts/*.sh migration/*.sh
find . -type f -name '*.json' -print0 | xargs -0 -n1 jq empty
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skill.py . --strict-warnings
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/build_manifest.py . --check
```

Observed results for the release bundle:

- standalone bundle validator: zero errors and zero warnings
- Python and Bash syntax: passed
- all JSON files: parsed successfully
- executable offline test suite: passed
- Java value-contract fixture: compiled with `javac --release 21` and ran with assertions enabled
- Maven and Gradle wrapper command construction: passed in dry-run tests
- project profiler: passed Maven and Gradle Kotlin DSL fixtures
- risk scanner: passed Markdown, JSON, SARIF, severity, and evidence-location checks
- diff-scope checker: detected tracked and untracked scope/security candidates
- migration: dry-run and apply paths passed against a temporary Git repository
- manifest: every portable payload file is size- and SHA-256-verified

Construction environment:

- OpenJDK 21.0.10
- Python 3.13.5
- Git 2.47.3
- Bash, `jq`, Info-ZIP `zip`/`unzip`

The tests are offline. The Quarkus fixture is intentionally static and does not download framework dependencies.

## External checks not claimed

The following tools were unavailable in the construction environment and were **not** claimed as passed:

- `skills-ref validate`
- `tessl skill lint`
- `tessl skill review`
- `tessl eval run`
- Maven or Gradle dependency resolution
- a Quarkus JVM integration build
- a Quarkus native-image build
- ShellCheck

Run the relevant checks after installation with repository/network credentials and the project’s supported JDK, Maven/Gradle wrapper, Quarkus platform, container runtime, and native toolchain. A Tessl score must not be reported until Tessl has actually produced it.

## Installation verification

Installation into `ai-engineering-skills` on 2026-07-10 exposed a Bash 3.2 portability issue: expanding optional empty arrays under `set -u` made the wrapper-first quality gate fail before printing its dry-run command. The installed script now assembles optional arguments only when present.

The installed tree was then checked with:

- standalone strict validation: zero errors and zero warnings
- offline tests with OpenJDK 26 exercising `javac --release 21`: 13 of 13 passed
- Python and Bash syntax checks: passed
- JSON parsing with `jq`: passed
- ShellCheck: passed
- repository validation: all 10 installed skills passed
- Tessl 0.90.0 lint: valid, with a deprecation warning for the legacy `tile.json` plugin manifest

`skills-ref validate`, Tessl review/eval jobs, dependency-resolving Maven or Gradle builds, Quarkus integration, and native-image checks were not run during installation.

## Release procedure

1. Run the offline commands above.
2. Regenerate the manifest after the last content change:

   ```bash
   python3 scripts/build_manifest.py .
   python3 scripts/build_manifest.py . --check
   ```

3. Create the ZIP from the parent directory so the archive has one `effective-java/` root.
4. Extract into a clean temporary directory.
5. Re-run strict validation, manifest verification, and the offline tests from the extracted copy.
6. Run Agent Skills and Tessl validation/evals when their CLIs are available.
