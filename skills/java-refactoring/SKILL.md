---
name: java-refactoring
description: Review Java code for maintainability issues, code smells, and SOLID violations. Use when refactoring Java code, reviewing for code smells, improving testability, reducing coupling, or creating a behavior-preserving refactoring plan.
---

# Java Refactoring Skill: Code Smells + SOLID

A practical, Java-focused reference and operating procedure for:
- Recognizing **all code smells** listed in Refactoring.Guru's *Code Smells* catalog (Bloaters, Object-Orientation Abusers, Change Preventers, Dispensables, Couplers, plus Incomplete Library Class).
- Applying **SOLID** principles (SRP, OCP, LSP, ISP, DIP) to refactor safely.
- Turning "smelly" legacy Java into code that is easier to extend, test, and maintain.

> **Important:** This is a condensed, paraphrased "field guide." It is not a copy of the original Refactoring.Guru text.

---

## When to use this skill

Use this skill when you need to:
- Review Java code for maintainability issues and refactoring opportunities.
- Turn a "works but messy" implementation into a design that is easier to evolve.
- Reduce risk/cost of change by addressing high-impact smells first.
- Improve testability (usually by reducing coupling and clarifying responsibilities).
- Create a refactoring plan that stays behavior-preserving.

---

## Inputs you should gather first (to avoid wrong refactors)

1. **Java version** (8/11/17/21+) and constraints (Android? server?).
2. **Frameworks** involved (Spring, Jakarta EE, Quarkus, Micronaut, etc.).
3. **Non-functional constraints**: performance, memory, latency, concurrency.
4. **Testing situation**: existing unit/integration tests? golden files? snapshots?
5. **API stability**: which public methods/classes are "public contract" and can't change?
6. **Ownership**: can you rename public methods? move packages? change serialization?

If any of these are unknown, refactor more conservatively (internal-only changes, add tests first).

---

## Refactoring safety rules (Java)

1. **Preserve behavior**: refactoring != rewriting. Keep functionality identical unless explicitly told otherwise.
2. **Make changes in small, reversible steps**:
   - One smell/one concept per commit.
   - Keep compilation green after each step.
3. **Add characterization tests** before deep changes:
   - Capture current behavior (even if it's weird).
4. **Prefer IDE refactorings** (move/rename/extract) to avoid missed references.
5. **Avoid mixed concerns during refactor**:
   - Don't "improve style" and "change logic" in the same diff.
6. **Measure impact** in hotspots:
   - Improve the areas that change most often (or cause most bugs) first.

---

## SOLID principles in Java (what to do, what to avoid)

SOLID is not a checklist to "implement." It's a set of heuristics for minimizing the cost of change.

### S — Single Responsibility Principle (SRP)

**Idea:** A class/module should have one primary reason to change.
**Signals of SRP violations:** "God classes", many unrelated methods, lots of feature flags, constant churn.

**Java tactics**
- Split responsibilities by **use case** / **feature** rather than by "technical layer only".
- Extract cohesive collaborators (e.g., `Validator`, `Mapper`, `Policy`, `Calculator`, `Repository`).
- Prefer immutable data where possible (records/value objects) to simplify reasoning.

```java
// BEFORE: OrderService does everything.
class OrderService {
  void placeOrder(OrderRequest req) { /* validate + price + persist + notify */ }
}

// AFTER: Responsibilities split.
class OrderPlacer {
  private final OrderValidator validator;
  private final PricingService pricing;
  private final OrderRepository repo;
  private final NotificationService notifications;

  void placeOrder(OrderRequest req) { /* orchestration only */ }
}
```

### O — Open/Closed Principle (OCP)

**Idea:** You can add new behavior by extension (new classes/strategies), without editing lots of existing logic.

**Signals:** `switch/if` ladders on "type", repeated conditionals, frequent edits in central dispatcher classes.

**Java tactics**
- Replace type switches with **polymorphism** (Strategy/State/Command).
- Use **enums with behavior** or **sealed hierarchies** for controlled extension.
- Prefer composition over inheritance for variation points.

```java
interface DiscountPolicy { BigDecimal discount(Order o); }

final class VipDiscount implements DiscountPolicy { /* ... */ }
final class RegularDiscount implements DiscountPolicy { /* ... */ }
```

### L — Liskov Substitution Principle (LSP)

**Idea:** If `B` is a subtype of `A`, you can use `B` anywhere you use `A` without breaking correctness.

**Signals:** subclasses that throw `UnsupportedOperationException`, violate invariants, or require special casing.

**Java tactics**
- Don't use inheritance just for code reuse; use it for **true substitutability**.
- Use smaller interfaces, composition, and delegation when behavior diverges.
- Document behavioral contracts (pre/postconditions) and keep them consistent.

### I — Interface Segregation Principle (ISP)

**Idea:** Clients shouldn't depend on methods they don't use.

**Signals:** "fat" interfaces, many no-op methods in implementations, testing pain, frequent breaking changes.

**Java tactics**
- Split interfaces into **role-based** interfaces.
- Avoid "one interface for all use cases"; create focused ports.
- Prefer `default` methods only when they truly reduce duplication without bloating clients.

```java
interface Reader { String read(); }
interface Writer { void write(String s); }
// instead of one huge ReadWriteManageEverything interface
```

### D — Dependency Inversion Principle (DIP)

**Idea:** High-level policy depends on abstractions, not details. Details depend on abstractions.

**Signals:** business logic instantiates concrete implementations (`new` everywhere), hard-to-test code, deep framework coupling.

**Java tactics**
- Depend on interfaces (ports) and inject implementations (adapters).
- Use constructor injection for mandatory dependencies.
- Keep infrastructure (HTTP, DB, filesystem) at the edges.

```java
interface PaymentGateway { Receipt charge(Money amount); }

class CheckoutService {
  private final PaymentGateway gateway;
  CheckoutService(PaymentGateway gateway) { this.gateway = gateway; }
}
```

---

## Smell → SOLID "common links" (quick mapping)

| Smell | Often relates to |
|---|---|
| Long Method, Large Class, Divergent Change | **SRP** |
| Switch Statements, Duplicate Code (case logic), Type Codes | **OCP** |
| Refused Bequest, "special-cased" subclasses | **LSP** |
| Fat APIs, Alternative Classes w/ Different Interfaces | **ISP** |
| Message Chains, Inappropriate Intimacy, Shotgun Surgery | **DIP/decoupling** |
| Primitive Obsession, Data Clumps | SRP + design clarity (better domain model) |

---

## Code smells catalog

For the complete catalog of all code smells (Bloaters, Object-Orientation Abusers, Change Preventers, Dispensables, Couplers, and other smells) with detection signals, costs, fix strategies, and ignore-when guidance, see [reference.md](reference.md).

---

## Refactoring workflow (recommended)

1. **Pick the refactoring target**
   - Prefer code that changes often, breaks often, or blocks new features.
2. **Stabilize with tests**
   - Add characterization tests if needed.
3. **Detect smells**
   - Use IDE inspections + static analysis (SonarLint/SonarQube, Checkstyle, PMD, SpotBugs).
4. **Plan micro-steps**
   - Choose the smallest sequence of safe refactorings.
5. **Apply refactorings**
   - Keep compilation green; run tests frequently.
6. **Re-check design**
   - Re-evaluate SOLID: responsibilities, extension points, substitutability, interface size, dependency direction.
7. **Finalize**
   - Remove dead code, simplify names, update docs where they explain *why*.

---

## Code review checklist (Java)

- [ ] No behavior change unless requested; tests cover main flows.
- [ ] Reduced cyclomatic complexity in hotspot methods.
- [ ] Responsibilities are clearer and boundaries are explicit.
- [ ] No new "god objects" created in the process.
- [ ] Public API changes are justified and documented.
- [ ] Dependencies flow inward (domain/policy doesn't import infrastructure).
- [ ] Naming communicates intent; comments explain *why*, not *what*.

---

## Prompt template (if you use an LLM with this skill)

When asking for help, include:
- Java version + framework + constraints
- A code snippet or file(s)
- What you want: "refactor only" vs "refactor + behavior change"
- Any API that must remain stable

Example request:

> Analyze this Java code for Refactoring.Guru code smells and SOLID violations.
> List smells with evidence (methods/classes), propose a step-by-step refactor plan (small commits), and show the final refactored code with notes on why each change improves SRP/OCP/LSP/ISP/DIP.
