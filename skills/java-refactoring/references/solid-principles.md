# SOLID Principles in Java

Detailed SOLID principle explanations with Java code examples. Referenced from the main skill during Step 3 (Map Smells to SOLID Violations).

## Overview

SOLID is not a checklist to "implement." It's a set of heuristics for minimizing the cost of change.

## S — Single Responsibility Principle (SRP)

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

## O — Open/Closed Principle (OCP)

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

## L — Liskov Substitution Principle (LSP)

**Idea:** If `B` is a subtype of `A`, you can use `B` anywhere you use `A` without breaking correctness.

**Signals:** subclasses that throw `UnsupportedOperationException`, violate invariants, or require special casing.

**Java tactics**
- Don't use inheritance just for code reuse; use it for **true substitutability**.
- Use smaller interfaces, composition, and delegation when behavior diverges.
- Document behavioral contracts (pre/postconditions) and keep them consistent.

## I — Interface Segregation Principle (ISP)

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

## D — Dependency Inversion Principle (DIP)

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

## Smell-to-SOLID Quick Mapping

| Smell | Often relates to |
|---|---|
| Long Method, Large Class, Divergent Change | **SRP** |
| Switch Statements, Duplicate Code (case logic), Type Codes | **OCP** |
| Refused Bequest, "special-cased" subclasses | **LSP** |
| Fat APIs, Alternative Classes w/ Different Interfaces | **ISP** |
| Message Chains, Inappropriate Intimacy, Shotgun Surgery | **DIP/decoupling** |
| Primitive Obsession, Data Clumps | SRP + design clarity (better domain model) |
