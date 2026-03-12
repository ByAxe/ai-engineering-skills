---
name: java-21-refactor-assessor
description: Assesses and refactors Java 21 codebases into idiomatic, maintainable Java.
  Use when the user asks to "review this Java 21 code", "modernize Java codebase",
  "refactor Python-to-Java port", "remove Pythonic anti-patterns", or "improve Java
  architecture". Do not use for pure Python-only repositories or projects not written in Java.
license: MIT
compatibility: Java 21 projects using Maven or Gradle. Works best with repository access
  and ability to run build/test commands.
metadata:
  author: ByAxe
  version: 2.0.0
  category: software-development
  tags: [java, java-21, refactoring, assessment, python-to-java, virtual-threads,
         concurrency, architecture]
---

# Java 21 Refactor Assessor

Turn a Java 21 codebase into clean, idiomatic Java with strong typing, clear boundaries,
safe concurrency, and verifiable behavior.

## Important

- Preserve behavior first. Favor refactors that keep external behavior identical, backed by tests.
- Prefer clarity over cleverness. Avoid overusing streams, reflection, metaprogramming patterns, or "framework magic" when a simple, explicit approach is clearer.
- Make illegal states unrepresentable. Use types, immutability, and sealed hierarchies to prevent bugs.
- Keep changes incremental. Refactor in small batches; compile and run tests after each batch.
- Optimize last. Make performance changes only after correctness and clarity are established, and back them with measurements.

## Instructions

### Step 1: Establish a Baseline

- Identify the build tool and entry points:
  - Maven: pom.xml
  - Gradle: build.gradle or build.gradle.kts
- Run a clean build and the full test suite.
- Capture current behavior:
  - Record API contracts, CLI output, and key workflows.
  - Note runtime flags (especially for any preview features).

### Step 2: Inventory Architecture and Dependencies

- Map modules and packages:
  - Identify "core domain" code vs frameworks/adapters (web, DB, messaging).
  - Detect cycles between packages/modules.
- Identify external dependencies and versions:
  - Highlight Python-era libraries or patterns that no longer fit (dynamic maps, "duck-typing" wrappers, runtime type switching).

### Step 3: Detect Port Smells

Look for these high-signal Python-to-Java patterns:

- Dynamic data everywhere:
  - Map<String, Object>, Map<String, Any>, raw Object fields, JSON-as-Map without schemas.
  - "payload" blobs passed through many layers.
- Overloaded "utility" modules/classes:
  - Large static helper classes replacing cohesive services.
  - God classes that centralize unrelated responsibilities.
- Pythonic control flow:
  - Deep if/elif chains for type dispatch instead of polymorphism or sealed + switch.
  - Sentinel values and None-like patterns instead of explicit types or Optional.
- Weak error modeling:
  - Catch-all Exception, silent failures, logging without propagation, "return null" on failure.
- Concurrency translated literally:
  - Shared mutable state, ad-hoc thread creation, executor misuse, or "async-style" code without need.

### Step 4: Propose a Refactor Plan

- Prioritize by risk and leverage:
  1. Correctness and data integrity
  2. API and domain modeling
  3. Boundaries and layering
  4. Concurrency and scalability
  5. Performance and allocation hot spots
- Define phases with acceptance criteria:
  - Build still passes
  - Tests still pass (or are improved)
  - Public interfaces unchanged unless explicitly approved

### Step 5: Execute Refactors

Apply idiomatic Java 21 patterns. Key areas:

- **Data modeling**: records for value types, sealed interfaces for closed hierarchies
- **Pattern matching**: switch expressions with record patterns for type dispatch (finalized in Java 21, JEP 441/440)
- **Collections**: immutable factories (List.of, Set.of, Map.of), sequenced collection APIs (JEP 431)
- **Null/Optional**: no null returns from public APIs, validate at boundaries
- **Concurrency**: virtual threads for I/O-bound work (JEP 444), avoid synchronized pinning; structured concurrency for fork-join patterns (preview, JEP 453)
- **Testing**: JUnit 5, characterization tests before refactoring

For detailed guidance with code examples: `references/java-21-best-practices.md`

When a specific symptom is identified, use the playbook below.

### Step 6: Validate and Harden

- Run formatters and static analysis.
- Add or strengthen tests around previously implicit behavior.
- Re-run the suite and key workflows.
- Provide a concise change log: what changed, why, and how to validate.

## Refactoring Playbook by Symptom

### Symptom: "Everything is a Map"

- Introduce typed records/classes for payloads.
- Centralize parsing/validation at the boundary (JSON in, typed object out).
- Replace Map lookups with field access.
- Add validation and tests for parsing.

### Symptom: "Huge if/else chains for types or states"

- Model states with sealed types or enums + dedicated data.
- Replace chains with pattern switch and exhaustive handling.
- Enforce no default branch unless explicitly needed.

### Symptom: "God classes and static helpers"

- Split by responsibility:
  - Extract cohesive services and inject dependencies.
  - Move pure functions to small utility classes only when genuinely cross-cutting.
- Reduce static state; prefer instance composition.

### Symptom: "Concurrency feels unsafe or inconsistent"

- Identify shared mutable state and race risks.
- Prefer confinement:
  - Make state immutable, or
  - Confine mutation to a single thread/component.
- For I/O-heavy parallelism, prefer virtual threads + bounded lifetimes.
- For multi-step parallel workflows, prefer structured concurrency.

### Symptom: "Errors are swallowed or unclear"

- Replace catch-all with specific handling.
- Add context to errors and propagate causes.
- Introduce typed results for expected failures.

## Output Contract

When asked to assess a codebase, produce:

1. **Findings summary** — top 5 risks and their impact
2. **Refactor plan** — phases, expected effort, and safety checks
3. **Concrete changes** — specific files/classes to touch and why
4. **Verification steps** — exact commands to build/test/run key workflows

When asked to refactor code, implement changes in small batches and include:

- What changed
- Why it is more idiomatic Java 21
- How to verify (build + tests)

## Smell Navigation

- Full Java 21 best practices with code examples: `references/java-21-best-practices.md`

## Examples

### Example 1: Full codebase assessment
User: "Assess this Java 21 repository that was ported from Python."
Action: Run Steps 1-6. Produce findings summary, refactor plan, concrete changes,
and verification steps.

### Example 2: Targeted symptom fix
User: "This service uses Map<String, Object> everywhere."
Action: Apply "Everything is a Map" playbook — introduce typed records, centralize
parsing at boundaries, add tests.

### Example 3: Concurrency modernization
User: "Replace our thread pool with virtual threads."
Action: Audit current patterns, identify I/O-bound vs compute-bound, apply virtual
thread executor, verify no pinning from synchronized.

## Troubleshooting

### Project uses preview features
Confirm --enable-preview in compile + runtime. Document the preview dependency.
Structured concurrency (JEP 453) and scoped values (JEP 446) are preview in Java 21.

### Tests fail after refactor
Revert to last passing state. Narrow scope. Add characterization tests. Re-apply smaller.

### Unclear if port smell or intentional design
Check for explicit documentation. If absent, propose change with justification.
Preserve revert option.

## Trigger Test Suite

Should trigger:
- "Assess this Java 21 codebase"
- "Modernize this Java repository"
- "This was ported from Python, clean it up"
- "Refactor for idiomatic Java 21"

Should NOT trigger:
- "Write Python code"
- "Refactor this TypeScript"
- "Help me with Java 8 code" (borderline — may trigger for general assessment)
