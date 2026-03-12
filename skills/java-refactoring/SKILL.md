---
name: java-refactoring
description: Review Java code for maintainability issues, code smells, and SOLID violations.
  Use when the user asks to "refactor this Java code", "find code smells", "review for
  SOLID violations", "improve testability", "reduce coupling", or "create a refactoring plan".
  Do not use for TypeScript, Python, or non-Java languages.
license: MIT
compatibility: Java projects (8+). Works best with repository access and ability to run
  build/test commands (Maven, Gradle). Framework-aware for Spring, Jakarta EE, Quarkus,
  Micronaut.
metadata:
  author: ByAxe
  version: 2.0.0
  category: software-development
  tags: [java, refactoring, code-smells, solid, maintainability, testability]
---

# Java Refactoring: Code Smells + SOLID

Diagnose Java code smells and SOLID violations, then refactor safely while preserving behavior.

## Important

- Preserve behavior: refactoring != rewriting. Keep functionality identical unless explicitly told otherwise.
- Small reversible steps: one smell per commit, compilation green after each.
- Add characterization tests before deep changes to capture current behavior.
- Prefer IDE refactorings (move/rename/extract) to avoid missed references.
- Don't mix style changes and logic changes in the same diff.
- Prioritize hotspots: code that changes most or causes most bugs.

## Instructions

### Step 1: Gather Context

Before refactoring, gather:

1. **Java version** (8/11/17/21+) and constraints (Android? server?).
2. **Frameworks** involved (Spring, Jakarta EE, Quarkus, Micronaut, etc.).
3. **Non-functional constraints**: performance, memory, latency, concurrency.
4. **Testing situation**: existing unit/integration tests? golden files? snapshots?
5. **API stability**: which public methods/classes are "public contract" and can't change?
6. **Ownership**: can you rename public methods? move packages? change serialization?

If any of these are unknown, refactor more conservatively (internal-only changes, add tests first).

### Step 2: Detect Smells

Scan target code against the smell catalog.

- Full catalog: `references/code-smells-catalog.md`
- Augment with IDE inspections and static analysis (SonarLint, Checkstyle, PMD, SpotBugs)

Name each smell, cite evidence, note risk level.

### Step 3: Map Smells to SOLID Violations

| Principle | Signal | Primary Tactic |
|---|---|---|
| **SRP** | God classes, many unrelated methods, constant churn | Split by use case; extract collaborators |
| **OCP** | switch/if ladders on type, repeated conditionals | Polymorphism (Strategy/State/Command) |
| **LSP** | Subclasses throw UnsupportedOperationException | Composition over inheritance |
| **ISP** | Fat interfaces, no-op implementations, testing pain | Role-based interfaces |
| **DIP** | `new` everywhere, hard-to-test code, deep framework coupling | Depend on interfaces; constructor injection |

Full SOLID with Java code examples: `references/solid-principles.md`

### Step 4: Plan Micro-Steps

- Pick the refactoring target: prefer code that changes often, breaks often, or blocks new features.
- Stabilize with tests: add characterization tests if needed.
- Choose the smallest sequence of safe refactorings.

### Step 5: Apply Refactorings

- Keep compilation green; run tests frequently.
- Re-evaluate SOLID after each change: responsibilities, extension points, substitutability, interface size, dependency direction.

### Step 6: Verify and Report

- Remove dead code, simplify names, update docs where they explain *why*.
- Confirm no behavior change unless requested; tests cover main flows.
- Check: reduced complexity in hotspots, clearer responsibilities, no new "god objects", public API changes justified, dependencies flow inward, naming communicates intent.

## Output Contract

1. **Smells found** — name, evidence, risk, SOLID mapping
2. **Refactor plan** — ordered micro-steps with verification checkpoints
3. **Changes** — code with explanation of why each change improves design
4. **Verification** — exact commands and what success looks like
5. **Follow-ups** — deferred improvements (optional)

## Smell Navigation

- Code smells catalog (all categories): `references/code-smells-catalog.md`
- SOLID principles with Java examples: `references/solid-principles.md`

## Examples

### Example 1: Full code review
User: "Review this Java service for code smells."
Action: Gather context, scan catalog, map to SOLID, produce ordered refactoring plan
with before/after code.

### Example 2: Targeted smell fix
User: "This OrderService is 800 lines. Help me break it up."
Action: Diagnose Large Class / SRP violation, identify seams, extract collaborators
in small commits, verify tests after each.

### Example 3: Testability improvement
User: "I can't unit test this PaymentProcessor."
Action: Diagnose DIP violation, introduce interfaces at boundaries, constructor injection,
demonstrate test with mock.

## Troubleshooting

### "This class is too big"
Identify seams: validation, persistence, notification, mapping, domain logic.
Extract SRP order: value objects, then collaborators, then orchestrator.

### "Adding a feature requires changes everywhere"
Diagnose Shotgun Surgery / tight coupling. Consolidate behavior near data/policy.

### "I can't test this code"
Identify concrete dependencies. Apply DIP: interfaces at boundaries, constructor injection.

## Trigger Test Suite

Should trigger:
- "Review this Java code for code smells"
- "Refactor this Java class, it's too large"
- "Find SOLID violations in my Java code"
- "Create a refactoring plan"

Should NOT trigger:
- "Write a SQL migration"
- "Refactor this TypeScript component"
- "Help me with Python code"
