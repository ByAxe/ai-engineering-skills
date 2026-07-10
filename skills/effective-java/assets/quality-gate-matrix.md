# Quality Gate Matrix

Choose gates from the changed contract, not from a universal “run everything” ritual.

| Change surface | Minimum gate | Widen when | Typical additional proof |
|---|---|---|---|
| pure Java algorithm/value object | compile + focused unit tests | public API or numeric/time edge | parameterized/property tests, module test |
| record/sealed/pattern modernization | compile + equality/serialization tests | public DTO/API | consumer/contract test |
| collections/streams | focused tests for order, duplicates, mutability, nulls | large data/performance | benchmark/profile |
| exception/I/O/resource | failure-path test + resource cleanup | external network/files | integration/fault injection |
| public library API | module build + API/consumer tests | published artifact | binary compatibility tool if configured |
| concurrency/virtual threads | deterministic tests | throughput/resource claim | JFR/load/pinning diagnostics |
| build/dependency/plugin | clean wrapper build | multi-module/runtime | effective POM/dependency insight, packaged run |
| JPA query/entity | DB-backed test | dialect/locking/query count | production-dialect container, SQL plan |
| transaction boundary | rollback/commit integration tests | external side effect/reactive | failure matrix/outbox/idempotency test |
| REST contract | HTTP contract tests | filters/security/proxy | packaged integration |
| Quarkus CDI/interceptor | component or `@QuarkusTest` | build profile/native | packaged/native test |
| Quarkus config phase | packaged-mode override test | native/build-time init | native executable test |
| messaging | ack/nack/duplicate tests | broker semantics | real broker/Dev Service integration |
| scheduler | overlap/time-zone/idempotency tests | multi-instance | distributed lock/cluster test |
| security | authn/authz/hostile input tests | critical exposure | threat review/DAST/policy test |
| native-sensitive code | JVM + packaged test | native production target | native integration build/run |

## Suggested order

1. syntax/compile or test-compile
2. focused test for changed contract
3. framework/component integration
4. formatter and configured analyzers
5. module/reactor `test`/`check`/`verify`
6. packaged JVM
7. native/load/security/migration gate only when risk requires it

Record command, exit status, tests discovered, and relevant output. A green process with zero discovered tests is not a green test gate.
