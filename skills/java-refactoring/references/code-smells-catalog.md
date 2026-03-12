# Code Smells Catalog (Refactoring.Guru list)

All smells from the Refactoring.Guru *Code Smells* list, with Java-oriented detection tips and common refactoring moves.

## Contents

- [Bloaters](#bloaters): Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps
- [Object-Orientation Abusers](#object-orientation-abusers): Alternative Classes with Different Interfaces, Refused Bequest, Switch Statements, Temporary Field
- [Change Preventers](#change-preventers): Divergent Change, Shotgun Surgery, Parallel Inheritance Hierarchies
- [Dispensables](#dispensables): Comments, Duplicate Code, Lazy Class, Data Class, Dead Code, Speculative Generality
- [Couplers](#couplers): Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man
- [Other smells](#other-smells): Incomplete Library Class

## How to read each smell entry

- **Signals**: how to notice it quickly.
- **Costs**: why it matters (risk/cost of change).
- **Fix**: refactoring moves (named after common refactoring patterns).
- **Ignore when**: cases where the "smell" may be acceptable.

> Refactoring move names match standard refactoring vocabulary (e.g., *Extract Method*, *Move Method*, etc.).

---

## Bloaters

### Long Method

**Signals**
- Method does "setup + logic + formatting + IO".
- Many comments separating "sections".
- Deep nesting / lots of temporary variables.

**Costs**
- Hard to test, hard to reuse, high bug density.

**Fix (typical moves)**
- **Extract Method**: carve out cohesive chunks (validation, mapping, calculation).
- **Replace Temp with Query**: turn temporary variables into query methods when safe.
- **Introduce Explaining Variable / Extract Variable**: name complex expressions.
- **Replace Method with Method Object**: when the method needs many local vars.

**Ignore when**
- Tiny performance-critical loops with proven need for inlining (rare).

---

### Large Class

**Signals**
- Too many fields; "utility drawer" class.
- Many methods touch disjoint sets of fields.
- One class does multiple jobs (persistence + domain logic + formatting).

**Costs**
- Low cohesion, frequent merge conflicts, painful changes.

**Fix**
- **Extract Class**: split responsibilities into collaborators.
- **Extract Subclass / Extract Interface**: separate optional/variant behavior.
- For UI-heavy code: isolate view state (e.g., *Duplicate Observed Data* pattern).

**Ignore when**
- A deliberate facade with minimal logic (but keep it thin).

---

### Primitive Obsession

**Signals**
- Magic strings, ints, raw maps, `String` used for money/IDs/dates.
- Lots of validation scattered everywhere.
- `Map<String, Object>` or "code" fields with implicit meaning.

**Costs**
- Bugs from invalid states, duplicated validation, unclear intent.

**Fix**
- **Replace Data Value with Object**: introduce value objects (e.g., `Email`, `Money`).
- **Replace Type Code with Class / Subclasses / State/Strategy**.
- **Replace Array with Object**: convert positional data to named fields.
- Use Java types: `UUID`, `Instant`, `Duration`, `BigDecimal` (where appropriate).

**Ignore when**
- Truly throwaway scripts or boundary DTOs (but keep validation at boundaries).

---

### Long Parameter List

**Signals**
- Methods with many parameters, especially booleans/flags.
- Repeated parameter groups across methods.

**Costs**
- Call sites become unreadable, hard to evolve signature, bugs from wrong ordering.

**Fix**
- **Introduce Parameter Object** (often a record): `new ShippingRequest(...)`.
- **Preserve Whole Object**: pass domain objects rather than extracting fields.
- **Replace Parameter with Method Call**: compute inside when appropriate.

**Ignore when**
- Low-level performance hot paths where allocations are proven problematic.

---

### Data Clumps

**Signals**
- Same 3-5 parameters passed around together (e.g., `street, city, zip`).
- Same fields duplicated across classes.

**Costs**
- Duplicated change points, inconsistent validation.

**Fix**
- **Extract Class** / **Introduce Parameter Object**: group data (e.g., `Address`).
- **Preserve Whole Object** when the clump belongs to an existing entity.

**Ignore when**
- Temporary glue code you're about to delete (verify it's truly temporary).

---

## Object-Orientation Abusers

### Alternative Classes with Different Interfaces

**Signals**
- Two classes do similar things but APIs don't match (forces adapters everywhere).
- Conditional logic chooses which API to call.

**Costs**
- Hard to interchange, inconsistent usage across codebase.

**Fix**
- **Rename Method** to align concepts.
- **Move Method / Add Parameter / Parameterize Method** to unify capabilities.
- **Extract Superclass / Extract Interface** for common contract.
- Consider **Adapter** when you can't change one side (third-party).

**Ignore when**
- Intentional separation of concepts (verify they truly differ).

---

### Refused Bequest

**Signals**
- Subclass inherits methods/fields it doesn't use.
- Overridden methods throw exceptions or become no-ops.
- Subclass breaks assumptions of base class.

**Costs**
- Violates LSP; forces defensive coding and special cases.

**Fix**
- **Replace Inheritance with Delegation** (prefer composition).
- **Extract Superclass** to keep only shared, substitutable behavior.

**Ignore when**
- Rare: framework-mandated inheritance with small surface area (wrap instead if possible).

---

### Switch Statements

**Signals**
- Big `switch`/`if-else` chains on type codes, enums, strings.
- Same switch duplicated across methods/classes.

**Costs**
- OCP violation: adding a new case requires edits in many places.

**Fix**
- **Extract Method** for each branch, then **Move Method** to the right class.
- **Replace Type Code with Subclasses / State / Strategy**.
- **Replace Conditional with Polymorphism** (preferred).
- **Replace Parameter with Explicit Methods** when appropriate.
- **Introduce Null Object** to remove repeated null/absence branches.

**Java patterns**
- Enum strategy:

```java
enum PaymentType {
  CARD { Receipt pay(PaymentContext c) { /*...*/ } },
  CASH { Receipt pay(PaymentContext c) { /*...*/ } };
  abstract Receipt pay(PaymentContext c);
}
```

**Ignore when**
- Very small, stable switches that are unlikely to change (e.g., parsing fixed protocol).

---

### Temporary Field

**Signals**
- Fields are only set in certain scenarios and otherwise null/empty.
- Many null checks around a subset of fields.

**Costs**
- Object state becomes confusing; class tries to support multiple modes.

**Fix**
- **Extract Class**: move mode-specific data+logic into a helper (method object).
- **Replace Method with Method Object** for complex multi-step algorithms.
- **Introduce Null Object** to eliminate "is present" checks.

**Ignore when**
- Truly optional cached values (but keep them clearly named and documented).

---

## Change Preventers

### Divergent Change

**Signals**
- One class changes for many unrelated reasons (feature A change touches validation + formatting + persistence in same class).
- Adding one feature requires modifying multiple unrelated methods in that same class.

**Costs**
- SRP violation; class becomes a "change magnet".

**Fix**
- **Extract Class** by responsibility.
- When similar behavior exists across multiple classes, consider **Extract Superclass/Subclass** (careful with LSP).

**Ignore when**
- Short-lived prototypes (but plan a cleanup phase).

---

### Shotgun Surgery

**Signals**
- A single change request forces tiny edits across many classes.
- Features are split too thinly across the codebase.

**Costs**
- High coordination cost, fragile changes, merge conflicts.

**Fix**
- **Move Method / Move Field** to concentrate behavior near the data/policy.
- If classes become near-empty after moving behavior, **Inline Class**.

**Ignore when**
- Some cross-cutting changes are expected (logging/tracing via AOP), but keep them systematic.

---

### Parallel Inheritance Hierarchies

**Signals**
- Adding a subclass in one hierarchy forces adding a matching subclass in another.
- "Twin" hierarchies evolve together.

**Costs**
- Duplication and combinatorial complexity.

**Fix**
- Link one hierarchy to the other by composition, then:
  - **Move Method / Move Field** to eliminate one of the hierarchies.
- Consider Strategy/State to collapse parallel trees into composition.

**Ignore when**
- Attempts to collapse make the design worse; sometimes parallel trees are the lesser evil.

---

## Dispensables

### Comments

**Signals**
- Lots of comments that explain *what* the code does (not *why*).
- Comments used to compensate for unclear naming/structure.

**Costs**
- Comments get stale; they add noise and false confidence.

**Fix**
- **Extract Variable** to name complex expressions.
- **Extract Method** and name the method from the comment intent.
- **Rename Method/Class/Variable** to make code self-describing.
- **Introduce Assertion** for important invariants and assumptions.

**Ignore when**
- Explaining *why* a surprising decision exists, or documenting non-obvious constraints.
- Complex algorithms where clearer code isn't feasible.

---

### Duplicate Code

**Signals**
- Copy/paste blocks; similar branches; repeated mapping/validation logic.

**Costs**
- Bugs fixed in one place but not the other; higher maintenance.

**Fix**
- Same class: **Extract Method**.
- Sibling subclasses: **Extract Method** + **Pull Up Field/Method**, **Pull Up Constructor Body**.
- Similar but not identical: **Form Template Method**.
- Different algorithms same goal: **Substitute Algorithm**.
- Different classes: **Extract Superclass** or **Extract Class** (shared component).
- Repeated conditionals: **Consolidate Conditional Expression** / **Consolidate Duplicate Conditional Fragments**.

**Ignore when**
- Merging would make the result less readable than duplication (rare; justify in review).

---

### Lazy Class

**Signals**
- Class does too little; mainly exists for indirection.
- "Future placeholder" that never became real.

**Costs**
- Increases cognitive load; more files to navigate.

**Fix**
- **Inline Class**.
- For tiny subclasses: **Collapse Hierarchy**.

**Ignore when**
- A deliberate placeholder for imminent work (keep it time-boxed).

---

### Data Class

**Signals**
- Class is basically fields + getters/setters; behavior lives elsewhere.
- Anemic domain model where services do all the work.

**Costs**
- Feature Envy spreads; duplication in service code; low cohesion.

**Fix**
- **Encapsulate Field**; prefer controlled updates.
- **Encapsulate Collection** for list/set fields.
- **Move Method** (and **Extract Method**) from client code into the data class where it belongs.
- After adding real behavior, reduce over-permissive access: **Remove Setting Method**, **Hide Method**.

**Java note**
- DTOs are fine at boundaries. Domain objects should usually own business rules.

**Ignore when**
- The class is intentionally a DTO/record at system boundaries (serialization/mapping layer).

---

### Dead Code

**Signals**
- Unused methods/fields/params/classes; unreachable branches.
- "Old feature" remnants.

**Costs**
- Confuses readers; increases attack surface; can hide bugs.

**Fix**
- Delete it (use IDE "find usages" / safe delete).
- If it's an unnecessary class in a hierarchy: **Inline Class** or **Collapse Hierarchy**.
- Remove unused params: **Remove Parameter**.

**Ignore when**
- Code is used reflectively or via framework configuration (verify before deleting).

---

### Speculative Generality

**Signals**
- Hooks/abstractions "just in case", unused parameters, unused extension points.
- Abstract classes/interfaces with only one implementation and no clear need.

**Costs**
- Complexity without value; harder onboarding and change.

**Fix**
- Unused abstract classes: **Collapse Hierarchy**.
- Unneeded delegation: **Inline Class**.
- Unused methods: **Inline Method**.
- Unused params: **Remove Parameter**.
- Unused fields: delete.

**Ignore when**
- You're building a framework/library for external users (extensions may be the point).
- Tests may rely on hooks (verify first).

---

## Couplers

### Feature Envy

**Signals**
- A method reads more fields from another object than from `this`.
- Lots of getters: `a.getB().getC()...` inside a method.

**Costs**
- Misplaced behavior; changes require bouncing between classes.

**Fix**
- If the whole method belongs elsewhere: **Move Method**.
- If only part belongs: **Extract Method** and move that piece.
- If it touches multiple objects: split into focused methods placed near the data.

**Ignore when**
- Behavior is intentionally separated (Strategy/Visitor, functional-style pipelines).

---

### Inappropriate Intimacy

**Signals**
- One class reaches into another's internals (private fields via package access, too many friend-like helpers).
- Bidirectional references everywhere; tight knot.

**Costs**
- High coupling; changes ripple; reuse is hard.

**Fix**
- **Move Method / Move Field** to where it's actually needed.
- Or make relationship explicit with **Extract Class** + **Hide Delegate**.
- Break cycles: **Change Bidirectional Association to Unidirectional**.
- If the issue is between subclass & superclass, reconsider the relationship (inheritance vs delegation).

**Ignore when**
- Performance-critical, well-encapsulated modules (rare; document why).

---

### Message Chains

**Signals**
- Long call chains: `order.getCustomer().getAccount().getPlan().getRate()`.
- Code navigates object graphs instead of asking for results.

**Costs**
- Client depends on internal structure; small model changes break many callers.

**Fix**
- **Hide Delegate** (introduce forwarding method at the right place).
- Or extract the actual intent: **Extract Method** and **Move Method** to the start of the chain.

**Ignore when**
- Over-hiding delegates would create a *Middle Man* problem.

---

### Middle Man

**Signals**
- Class does little besides forwarding calls.
- Many methods are one-liners delegating to another object.

**Costs**
- Extra indirection; harder navigation and debugging.

**Fix**
- **Remove Middle Man**: let clients talk to the real collaborator.
- If delegation exists for a true purpose (Proxy/Decorator), keep it.

**Ignore when**
- The middle layer enforces invariants, security, caching, transactions, or is a deliberate pattern.

---

## Other smells

### Incomplete Library Class

**Signals**
- A third-party class is almost what you need, but missing a few methods.
- You can't modify it (read-only dependency).

**Costs**
- Workarounds spread; duplicated helper logic; awkward call sites.

**Fix**
- Small additions: **Introduce Foreign Method** (helper that "acts like" it belongs).
- Bigger adaptation: **Introduce Local Extension** (wrap/extend with your own type).
- In Java, **prefer composition** (wrappers/adapters) over subclassing if the library isn't designed for inheritance.

**Ignore when**
- Extending/wrapping introduces too much maintenance overhead; consider alternative libraries.
