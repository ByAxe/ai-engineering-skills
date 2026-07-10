# Legacy Skill Coverage Map

This bundle supersedes `java-21-refactor-assessor` and `java-refactoring`; it is not a textual concatenation.

| Legacy capability | Replacement location | Expansion |
|---|---|---|
| behavior-preserving refactoring | `SKILL.md`, `references/evidence-first-workflow.md` | contract matrix, evidence ledger, widening gates, rollback |
| Java 21 records/sealed/patterns | `references/modern-java-language-and-modeling.md` | equality, arrays/collections, exhaustive switches, version policy |
| virtual threads | `references/concurrency-virtual-threads-and-async.md` | workload, lifecycle, bounds, ThreadLocal, JDK 21–23 versus 24 pinning |
| dynamic maps/Python-shaped Java | modeling/API/collections references | boundary typing without cargo-cult layers |
| code smells | `references/smell-and-refactoring-catalog.md` | agent, semantic, build, security, persistence, and Quarkus smells |
| SOLID | architecture and smell references | heuristics tied to change axes; rejects interface/layer inflation |
| characterization tests | workflow/testing references | defect/fix/unchanged proof and test-layer fidelity |
| Maven/Gradle verification | build reference and scripts | wrapper-first profiler, gates, diff review, bundle validator |
| generic framework awareness | Quarkus reference suite | augmentation, ArC, execution model, transactions, config, messaging, native |
| output contract | assets and JSON schemas | assessment, plan, implementation report, machine-readable finding model |
| trigger examples | `SKILL.md`, `agents/openai.yaml`, evals | positive/negative activation and scenario grading |

## Intentionally changed guidance

- The project-configured Java release wins; Java 21 is a baseline, not a forced upgrade.
- Structured concurrency and scoped values are not prescribed as stable Java 21 production defaults.
- `synchronized` is not globally replaced for virtual threads; pinning advice is JDK-specific.
- SOLID is not treated as a requirement to introduce interfaces or layers.
- Quarkus is not treated as Spring with different annotations.
- Scanner matches are candidates, never confirmed findings.
- JVM tests are not claimed to prove native behavior.
