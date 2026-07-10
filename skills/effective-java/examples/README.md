# Effective Java Examples

These examples illustrate decision rules, not copy-paste framework templates. Confirm the target repository’s Java release, Quarkus version, extensions, serialization stack, and conventions before applying them.

| Concern | Example |
|---|---|
| record ownership/equality | `records-and-value-semantics.md` |
| collection order/mutability/duplicates | `collections-and-streams.md` |
| exceptions/resources/HTTP boundaries | `exceptions-and-boundaries.md` |
| virtual-thread workload and limits | `virtual-threads.md` |
| Quarkus REST dispatch and DTO boundary | `quarkus-rest-execution.md` |
| ArC constructor injection and config mapping | `quarkus-cdi-config.md` |
| ORM/reactive persistence and transactions | `quarkus-persistence.md` |

Every “after” example should be accompanied by a contract test in a real repository. The examples intentionally avoid asserting that one architecture fits all services.
