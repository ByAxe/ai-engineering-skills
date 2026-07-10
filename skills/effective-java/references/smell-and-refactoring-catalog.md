# Java and Quarkus Smell and Refactoring Catalog

This catalog is a hypothesis generator. A smell is not automatically a defect. Confirm repository context, contract, frequency, and cost before changing code.

## Finding format

For every reported item, include:

- **ID and name**
- **classification:** confirmed defect, high-confidence risk, candidate, or preference
- **severity:** critical, high, medium, low
- **confidence:** high, medium, low
- **evidence:** file, symbol, line, test, trace, metric, or config
- **contract/risk:** what can break or what cost is imposed
- **smallest remedy:** not an aspirational rewrite
- **verification:** exact proof
- **exception/trade-off:** why the current shape may be legitimate

Prioritize correctness, security, data integrity, concurrency, and compatibility before style or theoretical purity.

## A. Agent-specific patch smells

| ID | Signal | Risk | Verify | Smallest response |
|---|---|---|---|---|
| AG-01 | import/annotation/property looks plausible but has no local precedent | version/API confabulation | dependency graph, source/Javadoc, compile | use the project-supported API; do not add a random dependency |
| AG-02 | patch touches build, dependencies, formatting, packages, and behavior | scope explosion | diff stats and requirement trace | split unrelated changes; restore untouched files |
| AG-03 | “modernized” code is longer or more nested | cargo-cult modernization | compare control flow and contracts | retain loop/concrete type unless a specific benefit exists |
| AG-04 | several interfaces/builders/factories added for one implementation | abstraction inflation | identify real variation/test boundary | inline or keep concrete until volatility exists |
| AG-05 | comments/assertions claim a gate passed without output | false verification | command history/CI evidence | run the gate or disclose it was not run |
| AG-06 | heuristic scanner output copied as definitive findings | false-positive laundering | inspect each match semantically | downgrade to candidate or remove |
| AG-07 | behavior fallback/retry/sort/normalization added “helpfully” | invented semantics | contract and before/after tests | remove or make explicit requirement |
| AG-08 | generated file edited directly | overwritten change | generator/source mapping | edit source of truth and regenerate |
| AG-09 | dead code deleted based only on text search | framework/reflection break | CDI, service loader, config, serialization, generated refs | delete only after usage proof |
| AG-10 | dependency added for trivial JDK/existing-stack behavior | attack surface/version drift | existing APIs/dependencies | use existing capability or justify dependency |

## B. Naming, methods, and local control flow

| ID | Smell | Signals | Cost | Typical refactoring | Ignore when |
|---|---|---|---|---|---|
| LOC-01 | Long method | multiple phases, deep nesting, many locals | hard reasoning/testing | extract named pure steps; keep orchestration visible | linear algorithm is clearer together |
| LOC-02 | Boolean blindness | calls like `send(x, true, false)` | call-site ambiguity | enum/options/explicit methods | private obvious helper with one flag |
| LOC-03 | Flag argument | one method contains separate behaviors | divergent change | split commands or policy object | one stable minor rendering option |
| LOC-04 | Deep nesting | nested conditionals/loops/try | hidden paths | guard clauses, extract decision | nesting mirrors a clear tree/protocol |
| LOC-05 | Temporal coupling | methods must be called in undocumented order | invalid states | constructor/factory/state type | framework lifecycle is explicit and tested |
| LOC-06 | Mystery side effect | getter/mapper logs, persists, or mutates | surprise and duplicate work | command name and explicit boundary | lazy cache with documented thread safety |
| LOC-07 | Magic literal | repeated code/status/string/time | drift and weak meaning | named constant/value type/config | protocol literal appears once at boundary |
| LOC-08 | Comment as deodorant | comments explain what unclear code does | staleness | rename/extract; retain why/constraint | algorithm or workaround needs rationale |
| LOC-09 | Clever one-liner | nested ternary/stream/regex | review/debug cost | expand into named steps | established idiom remains obvious |
| LOC-10 | Copy-paste branch | near-identical blocks drift | inconsistent fixes | extract shared stable behavior | abstraction would obscure meaningful differences |

## C. Type and domain-model smells

| ID | Smell | Signals | Risk | Verify/refactor |
|---|---|---|---|---|
| MOD-01 | Primitive obsession | IDs/money/email/state as strings/numbers everywhere | invalid states/scattered validation | introduce focused value type at high-value boundary |
| MOD-02 | Dynamic map schema | `Map<String,Object>` passed across layers | runtime casts/typos/no evolution | typed DTO/record and boundary parser |
| MOD-03 | String type code | repeated comparisons on status/type | non-exhaustive behavior | enum or sealed hierarchy if set is truly closed |
| MOD-04 | Record misuse | entity, mutable identity, hidden invariants, array component | equality/ownership/proxy errors | retain class or defensive canonical constructor/accessor |
| MOD-05 | Anemic aggregate | rules live in many services over data-only domain objects | duplicated invariant | move behavior to cohesive owner where domain model merits it |
| MOD-06 | God object | disjoint fields/method clusters | low cohesion/conflicts | split by responsibility/change axis |
| MOD-07 | Data clump | same fields/parameters travel together | inconsistent validation | value object/parameter record |
| MOD-08 | Parallel hierarchy | adding variant requires matching classes elsewhere | combinatorial change | composition or collapse one hierarchy |
| MOD-09 | Refused inheritance | unsupported/no-op overrides | LSP violation | composition, smaller interface, split hierarchy |
| MOD-10 | Closed hierarchy with default switch | sealed variants plus broad `default` | new variant silently ignored | exhaustive cases; default only for external/open values |
| MOD-11 | Mutable collection exposed | getter returns owned mutable list/map | invariant corruption | immutable/defensive view or explicit mutation API |
| MOD-12 | Array as value component | record/equality/API owns array directly | reference equality and mutation | immutable collection or clone + explicit deep equality |
| MOD-13 | Sentinel value | `-1`, empty string, epoch means absent/error | ambiguous state | Optional/result/variant/domain type |
| MOD-14 | Generic “data/result/context” | unrelated fields accumulate | weak boundary | name by use case and split payloads |

## D. API, nullness, and generics smells

| ID | Smell | Signal | Risk | Smallest remedy |
|---|---|---|---|---|
| API-01 | Null return without contract | callers scatter checks/NPEs | ambiguity | document/annotate and use Optional or explicit nullable policy |
| API-02 | Optional field/parameter everywhere | serialization/framework friction | awkward double absence | nullable/internal field or overload/parameter object as appropriate |
| API-03 | `Optional.get()` | absence not handled | exception at edge | `orElseThrow`, mapping, pattern based on contract |
| API-04 | Raw generic type | `List`, `Map`, raw `Class` | heap pollution/casts | parameterize; localize unavoidable legacy bridge |
| API-05 | Unbounded wildcard misuse | unreadable `? extends/super` chains | caller pain | PECS only at genuine variance boundary |
| API-06 | Unsafe generic array/varargs | heap pollution warning | runtime type corruption | collection, safe copy, `@SafeVarargs` only with proof |
| API-07 | Long parameter list | same clusters/booleans | call-site mistakes | request/parameter object; preserve source compatibility if public |
| API-08 | Overload ambiguity | null/lambda/varargs choose surprising overload | source breaks | distinct names or narrower overload set |
| API-09 | Concrete collection in public API | implementation leakage | evolution cost | interface type unless concrete semantics matter |
| API-10 | Mutable input retained | caller later mutates state | action at distance | defensive copy or documented ownership transfer |
| API-11 | Checked exception leakage | low-level detail in public use case | coupling | translate at boundary while preserving cause |
| API-12 | Interface-per-class | no alternate implementation/role | navigation/ceremony | keep concrete until external boundary or variation exists |

## E. Collections, streams, and ordering smells

| ID | Smell | Signal | Risk | Verify/refactor |
|---|---|---|---|---|
| COL-01 | Mutability drift | `Collectors.toList()` changed to `Stream.toList()` | later mutation fails | test ownership/mutation; choose collector/copy deliberately |
| COL-02 | Order drift | `List`/`LinkedHashMap` replaced with unordered type | output/test/selection changes | state order contract; use ordered collection |
| COL-03 | Duplicate-key crash | `toMap` without merge | production exception | define duplicate policy explicitly |
| COL-04 | Side effects in stream | mutation/logging/IO in `map`/`peek` | order/parallel/debug surprises | loop or pure pipeline + terminal side effect |
| COL-05 | Nested stream maze | complex joins/state/checked errors | unreadable behavior | named loop/helper/query |
| COL-06 | `parallelStream()` in server code | common-pool contention/context loss | latency instability | remove unless benchmarked and isolated executor/design |
| COL-07 | Repeated linear lookup | list scanned inside loop | quadratic cost | pre-index map/set after measuring/cardinality check |
| COL-08 | Mutable key in hash map/set | hash fields change | unreachable entries | immutable key/equality policy |
| COL-09 | Wrong equality in distinct/set | entity/BigDecimal/array semantics | lost/duplicate data | define equality or comparator/normalization intentionally |
| COL-10 | Null-hostile factory surprise | `List.of/copyOf` with nulls | runtime NPE | validate/transform or retain nullable collection policy |
| COL-11 | Unbounded collection | cache/accumulator never evicts | memory leak | bound/expire/persist/stream |
| COL-12 | Concurrent collection as blanket fix | compound operation still racy | lost updates | atomic APIs/lock/confinement and invariant test |
| COL-13 | Accidental sequenced-view mutation | reversed/view operations affect backing data | aliasing surprise | copy when independent ownership is required |
| COL-14 | Materialize all | `.toList()` before filtering/pagination | memory/latency | filter/page at source or process incrementally |

## F. Equality, numeric, text, and time smells

| ID | Smell | Signal | Risk | Remedy |
|---|---|---|---|---|
| VAL-01 | Entity all-field equality | generated Lombok/IDE equality includes relations | recursion/hash instability | stable identity policy documented/tested |
| VAL-02 | `BigDecimal(double)` | binary artifact in decimal value | money/rounding error | string/valueOf or integer minor units per contract |
| VAL-03 | Scale-sensitive equality surprise | `1.0.equals(1.00)` assumption | set/assert/business mismatch | use `compareTo` only when numeric equality is intended |
| VAL-04 | Missing rounding policy | divide/setScale implicit | `ArithmeticException` or inconsistent money | explicit scale/rounding at domain boundary |
| VAL-05 | Integer overflow | multiply/add counters/sizes | security/correctness | exact methods, wider type, bounds |
| VAL-06 | Floating point exact compare | `double ==` for calculations | unstable tests/logic | tolerance/domain decimal representation |
| VAL-07 | System default charset | `new String(bytes)`, `getBytes()` | host-dependent data | `StandardCharsets.UTF_8` or contract charset |
| VAL-08 | System default locale | case/format/parsing | Turkish-I and host drift | `Locale.ROOT` or business locale |
| VAL-09 | System default zone | `LocalDateTime.now()` for instant | host/DST drift | `Clock`, `Instant`, explicit `ZoneId` |
| VAL-10 | Wall-clock duration | current time subtraction | clock adjustment errors | monotonic source for elapsed duration |
| VAL-11 | Regex denial/backtracking | untrusted large input/complex regex | CPU DoS | limits, safer parser/pattern, timeout architecture |
| VAL-12 | Platform line/path assumptions | hardcoded separators/case | portability | `Path`, line APIs, explicit normalization |

## G. Exceptions, resources, and I/O smells

| ID | Smell | Signal | Risk | Remedy |
|---|---|---|---|---|
| ERR-01 | Empty catch | ignored failure | corrupt/unknown state | handle, compensate, or propagate |
| ERR-02 | Catch `Exception`/`Throwable` broadly | masks bugs/cancellation | wrong recovery | narrow exception boundary; never catch fatal errors casually |
| ERR-03 | Log and rethrow | duplicate noisy logs | poor ownership | log once at owning boundary |
| ERR-04 | Cause discarded | `throw new X(message)` | lost diagnosis | wrap with cause |
| ERR-05 | Interrupted status lost | catch `InterruptedException` and continue | shutdown/cancellation failure | restore interrupt or propagate according to API |
| ERR-06 | Exception as loop/control flow | expected absence throws repeatedly | cost/noise | explicit result/Optional/query API |
| ERR-07 | Resource not closed | stream/client/executor/response | leak/exhaustion | try-with-resources or lifecycle owner |
| ERR-08 | New HTTP client per call | no pooling/lifecycle | latency/socket use | shared managed client |
| ERR-09 | Missing timeout | network/file/process wait forever | thread/resource exhaustion | connect/read/request/total deadlines |
| ERR-10 | Path traversal | resolve user path without containment | data exposure | normalize then enforce trusted-root containment |
| ERR-11 | Zip bomb/slip | archive extraction unbounded | overwrite/DoS | entry path and size/count limits |
| ERR-12 | Java native serialization | untrusted deserialization | RCE/compatibility | safer format/filter only if legacy unavoidable |
| ERR-13 | Full body buffering | untrusted response/request read all | memory DoS | size limits/streaming |
| ERR-14 | `printStackTrace`/`System.out` | unmanaged output/secrets | poor operations | structured project logger |

## H. Concurrency and asynchronous smells

| ID | Smell | Signal | Risk | Remedy/evidence |
|---|---|---|---|---|
| CON-01 | Executor without owner | `newFixedThreadPool` in method/bean | leaks/shutdown loss | framework-managed or explicit lifecycle |
| CON-02 | Common-pool async | bare `supplyAsync` | contention/context loss | explicit managed executor or synchronous path |
| CON-03 | Unbounded submission | task per item/request | memory/downstream collapse | semaphore/bulkhead/queue policy |
| CON-04 | Virtual-thread pool | fixed pool of virtual threads | defeats model | thread-per-task plus resource bounds |
| CON-05 | CPU work moved to virtual threads | no throughput benefit/carrier saturation | regressions | profile; bounded platform/ForkJoin strategy |
| CON-06 | ThreadLocal per virtual thread | memory/context leakage | scale failure | scoped/context propagation or explicit data |
| CON-07 | Runtime-insensitive pinning advice | blanket replace synchronized | needless churn | check JDK; JDK 24 changes synchronized pinning |
| CON-08 | Shared mutable app state | unsynchronized maps/counters | races/cross-request leak | immutability, confinement, atomic/lock design |
| CON-09 | Check-then-act | separate read and write | race | atomic compute/DB constraint/lock |
| CON-10 | Future `.get/join` in event loop | blocking/deadlock | latency outage | compose async or dispatch blocking work |
| CON-11 | Lost cancellation | detached tasks/recovery swallows | wasted work/inconsistent state | structured ownership and propagate cancellation |
| CON-12 | Timeout leaves work running | wrapper only times caller | resource leak/duplicate action | cancel underlying operation; idempotency |
| CON-13 | Retry without idempotency | duplicate payment/write/message | data corruption | idempotency key/state machine |
| CON-14 | Sleep-based synchronization | flaky/slow tests | false confidence | latch/barrier/eventual assertion with deadline |
| CON-15 | Lock around blocking remote call | contention/deadlock | outage amplification | reduce critical section/redesign state |
| CON-16 | Double-checked locking wrong | unsafe publication | rare corruption | correct volatile or holder/DI initialization |
| CON-17 | Reactive side subscription | detached lifecycle | lost errors/transaction | return composed pipeline |
| CON-18 | Context copied manually | stale/security leakage | cross-request contamination | supported context propagation |

## I. Architecture and dependency smells

| ID | Smell | Signal | Cost | Refactoring |
|---|---|---|---|---|
| ARC-01 | Large class | unrelated responsibilities/field clusters | churn/conflicts | extract by change axis/use case |
| ARC-02 | Shotgun surgery | one feature edits many tiny layers | fragile change | co-locate behavior/vertical slice |
| ARC-03 | Divergent change | one class changes for unrelated features | low cohesion | split responsibilities |
| ARC-04 | Feature envy | method mostly manipulates another object | misplaced behavior | move method or expose focused behavior |
| ARC-05 | Message chain | `a.getB().getC().getD()` | coupling/null fragility | tell-don’t-ask/focused facade where useful |
| ARC-06 | Middle man | class only delegates | navigation burden | inline unless boundary/policy is valuable |
| ARC-07 | Cyclic package/module dependency | mutual imports/build cycles | impossible layering | extract stable contract or reassign responsibility |
| ARC-08 | Package-by-layer mega-structure | feature spans many packages | discovery/ownership cost | package by feature/hybrid incrementally |
| ARC-09 | Utility dumping ground | `Common`, `Utils`, many unrelated statics | hidden cohesion | move to owner or focused helper |
| ARC-10 | Static service locator | global lookups/state | tests/lifecycle | DI or explicit composition at boundary |
| ARC-11 | Framework in domain core | annotations/types everywhere | migration and test coupling | isolate only where cost justifies it |
| ARC-12 | Ceremonial clean architecture | identical DTO copies/pass-through use cases | code volume | collapse no-value layers |
| ARC-13 | Dependency inversion theater | internal interface with one impl but no boundary | ceremony | concrete class; interface at external/volatile seam |
| ARC-14 | Dependency sprawl | many overlapping libraries | CVE/version/size | standardize and remove unused with proof |
| ARC-15 | Public internals | packages/classes exported accidentally | compatibility burden | narrow visibility/modules after usage analysis |

## J. Build and repository smells

| ID | Smell | Signal | Risk | Remedy |
|---|---|---|---|---|
| BLD-01 | System Maven/Gradle used despite wrapper | version drift | non-reproducible build | wrapper-first |
| BLD-02 | `source/target` without `release`/toolchain clarity | wrong bootstrap APIs | runtime failure | configure release/toolchain consistently |
| BLD-03 | Preview flag only in compiler | tests/runtime fail | environment mismatch | compiler, test, run, CI flags or avoid preview |
| BLD-04 | Dependency version bypasses BOM/catalog | convergence drift | runtime incompatibility | central management |
| BLD-05 | Annotation processor silently disabled | missing generated code | compile/runtime errors | inspect compiler/AP config |
| BLD-06 | Generated directories committed/edited inconsistently | stale artifacts | merge/build divergence | source-of-truth policy |
| BLD-07 | Multi-module partial build hides dependents | downstream break | false green | build affected reactor/dependents |
| BLD-08 | Test skipped/profile-dependent silently | false green | regressions | inspect effective tasks/profiles and discovery |
| BLD-09 | Formatter applied repository-wide in feature | review noise | hidden semantic diff | format touched scope/project policy |
| BLD-10 | Plugin/dependency upgrade bundled with fix | unbounded risk | hard rollback | separate change |
| BLD-11 | Dynamic/latest dependency version | irreproducible build | supply-chain drift | pin via project policy |
| BLD-12 | Secret in build log/config | credential exposure | compromise | secret provider/redaction/rotation |

## K. Persistence smells

| ID | Smell | Signal | Risk | Remedy |
|---|---|---|---|---|
| DB-01 | Entity as REST/message DTO | lazy/cycle/API coupling | data leak | boundary model |
| DB-02 | Mutable entity all-field equality | hash/recursion/proxy issue | collection corruption | stable identity strategy |
| DB-03 | Global eager loading | huge joins/N+1 elsewhere | performance | query-specific fetch/projection |
| DB-04 | N+1 mapping/serialization | query per row | latency/load | measure query count, fetch plan/projection |
| DB-05 | Hidden transaction in resource/repository | unclear atomicity | partial updates | use-case transaction boundary |
| DB-06 | External call inside transaction | long locks/connections | outage cascade | outbox/saga/stage carefully |
| DB-07 | Count-then-insert invariant | race | duplicates | database constraint + conflict handling |
| DB-08 | Cascade added as test fix | unintended updates/deletes | data loss | explicit lifecycle test |
| DB-09 | Stream escapes transaction | closed session/leak | runtime failure | consume/close inside boundary |
| DB-10 | Deployed migration edited | environment divergence | rollout failure | new forward migration |
| DB-11 | Schema auto-generation in production | uncontrolled drift | data loss | managed migrations |
| DB-12 | Blocking ORM on event loop | throughput collapse | outage | worker/virtual thread or reactive stack |
| DB-13 | Reactive transaction converted to blocking wait | deadlock/context loss | failure | compose reactive transaction |
| DB-14 | Retry whole transaction blindly | duplicate side effects | corruption | classify/idempotency/optimistic retry only |

## L. Testing and debugging smells

| ID | Smell | Signal | Risk | Remedy |
|---|---|---|---|---|
| TST-01 | Mock subject under test | test proves mock | no coverage | instantiate real subject |
| TST-02 | Interaction-only assertion | verifies calls, not outcome | brittle/false proof | assert observable contract |
| TST-03 | Expected value reimplements algorithm | same bug both sides | false confidence | examples, properties, or an independent oracle |
| TST-04 | Happy path only | no boundaries/failures | production gaps | table/parameterized edge matrix |
| TST-05 | `assertDoesNotThrow` only | no correctness assertion | weak test | assert result/state/side effect |
| TST-06 | Sleep/poll without deadline | flakes/hangs | unreliable CI | deterministic signal/eventual assertion |
| TST-07 | Everything `@QuarkusTest` | slow feedback | low test density | plain unit/component tests for pure logic |
| TST-08 | Everything mocked in integration test | framework boots but boundary absent | false integration | real test resource/container at target boundary |
| TST-09 | Shared mutable fixture | order dependence | flakes | per-test state/cleanup |
| TST-10 | System clock/zone/random | nondeterminism | flakes | injected clock/seed |
| TST-11 | Test not discovered | naming/engine/profile issue | false green | verify count/report |
| TST-12 | Snapshot/golden updated blindly | approves regression | contract loss | inspect semantic diff and rationale |
| TST-13 | Only unit test for interceptor/config/ORM mapping | wrong layer | false proof | framework-level test |
| TST-14 | Native claim from JVM test | closed-world gap | deployment failure | native integration where required |

## M. Security smells

| ID | Smell | Signal | Risk | Remedy |
|---|---|---|---|---|
| SEC-01 | Validation without authorization | valid cross-user ID accepted | IDOR | ownership/permission check |
| SEC-02 | Raw SQL/string query construction | untrusted concatenation | injection | parameters and allowlisted identifiers |
| SEC-03 | Path resolve without root containment | `../` or symlink escape | file exposure | normalize/real-path policy/containment |
| SEC-04 | URL allowlist before redirect/DNS | SSRF bypass | internal access | validate every hop/resolution and egress controls |
| SEC-05 | Secret/token logged | credentials in logs/traces | compromise | redaction and rotation |
| SEC-06 | Parser/archive no limits | entity/zip/JSON bomb | DoS | bytes/depth/count/time limits |
| SEC-07 | Custom crypto/token validation | subtle vulnerability | auth compromise | standard provider/framework |
| SEC-08 | Internal exception returned | stack/schema/secret leak | reconnaissance | stable safe error envelope |
| SEC-09 | Retry non-idempotent operation | duplicate payment/action | financial/data loss | idempotency and bounded retry |
| SEC-10 | Unbounded regex/body/list query | CPU/memory exhaustion | DoS | limits/pagination/timeouts |
| SEC-11 | Dependency added without provenance | supply-chain risk | compromise | project-approved source/version/checks |
| SEC-12 | Client-controlled role/tenant header trusted | privilege escalation | authz bypass | verified identity claims/server lookup |

## N. Quarkus-specific smells

| ID | Smell | Signal | Risk | Verify/remedy |
|---|---|---|---|---|
| QUA-01 | Versionless “latest Quarkus” advice | API/property mismatch | build failure | project BOM/versioned docs |
| QUA-02 | Unindexed dependency assumed bean | injection failure | startup failure | Jandex/index-dependency/producer |
| QUA-03 | `@Named` as routine qualifier | default ambiguity/string coupling | augmentation failure | type-safe qualifier/identifier |
| QUA-04 | `@Singleton` everywhere | misunderstood scope/state | concurrency/lifecycle | choose scope intentionally |
| QUA-05 | mutable `@ApplicationScoped` fields | shared races/tenant leak | correctness/security | immutability/confinement/bounded state |
| QUA-06 | heavy startup callback | opaque readiness/dev restart | boot outage | bounded startup service/health |
| QUA-07 | broad `@Unremovable`/disable removal | hides dead beans/larger image | footprint | precise visible root |
| QUA-08 | interceptor annotation on ineffective path | transaction/security/retry bypass | data/auth issue | CDI integration test |
| QUA-09 | reactive signature with blocking call | event-loop starvation | outage | dispatch or consistent stack |
| QUA-10 | `.await/.join/get` in reactive request | blocking/deadlock | latency | composed pipeline |
| QUA-11 | `@RunOnVirtualThread` as universal speed flag | CPU/resource overload | regression | workload and downstream bounds |
| QUA-12 | ORM and Hibernate Reactive mixed | wrong session/thread | runtime failure | one model per path |
| QUA-13 | Jakarta `@Transactional` used on reactive Panache by habit | wrong transaction model | incomplete commit/rollback | supported reactive transaction API |
| QUA-14 | build-time property expected to change at runtime | ineffective config | deployment bug | phase check + packaged test |
| QUA-15 | Dev Services assumptions in prod | missing dependency/credentials | startup failure | explicit prod config |
| QUA-16 | JPA entity returned from REST | lazy/API leak | errors/data exposure | response model |
| QUA-17 | broad reflection/resource registration | image bloat/masked dynamic behavior | native regression | exact metadata and native test |
| QUA-18 | JVM test used as native proof | closed-world failure | prod outage | native integration for touched surface |
| QUA-19 | Spring annotation translation only | semantic mismatch | auth/tx/dispatch bugs | vertical-slice contract migration |
| QUA-20 | request filter blocks event loop | global latency | outage | filter execution/thread trace |
| QUA-21 | success telemetry before reactive/transaction completion | false signals | operations/data mismatch | record after terminal commit/outcome |
| QUA-22 | scheduler assumed cluster-singleton | duplicate jobs | repeated side effect | lock/leader/external scheduler |
| QUA-23 | message ack and DB commit misordered | loss/duplicate | data inconsistency | ack/transaction/idempotency design |
| QUA-24 | config mapping mocked/proxied casually | unsupported test behavior | fragile test | supply config/focused test implementation |

## Refactoring move selection

Prefer the move that directly removes the proven risk:

- **Rename / extract variable:** comprehension only
- **Extract method:** one cohesive local responsibility
- **Move method:** behavior belongs with data/policy
- **Introduce value object/record:** stable value semantics and validated boundary
- **Introduce parameter object:** coherent repeated parameter group
- **Replace conditional:** enum behavior, strategy, or sealed switch only when variation model warrants it
- **Replace inheritance with composition:** substitutability is false
- **Encapsulate collection:** ownership/invariants
- **Introduce adapter/port:** external dependency or volatile boundary
- **Split transaction/use case:** atomicity and orchestration boundary
- **Add database constraint:** persisted invariant and race safety
- **Add characterization test:** behavior unclear before structural change
- **Delete abstraction:** no independent change axis or policy

Do not combine several moves merely because they are adjacent in a catalog.

## Triage order

1. exploitable security, data corruption/loss, authorization, unsafe deserialization
2. transaction/concurrency correctness, idempotency, event-loop blocking
3. public/wire/schema compatibility
4. resource leaks, unbounded work, missing timeouts
5. build/version/generated/native correctness
6. test gaps for changed behavior
7. maintainability hotspots supported by churn/complexity evidence
8. style and preference
