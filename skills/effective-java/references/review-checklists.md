# Java and Quarkus Review Checklists

Use these as final passes, not as substitutes for understanding the change. Mark an item not applicable rather than forcing a change.

## 1. Change intent and evidence

- [ ] The requested behavior or refactoring goal is stated in one sentence.
- [ ] Current behavior was reproduced or characterized where uncertainty matters.
- [ ] Unchanged behavior is listed for risky work.
- [ ] Findings distinguish defect, risk, candidate, and preference.
- [ ] Every strong claim has code, test, build, trace, metric, or documented-contract evidence.
- [ ] The patch is the smallest defensible surface.
- [ ] Unrelated upgrades, formatting, package moves, or abstractions are absent.
- [ ] Generated files were not edited directly.
- [ ] Limitations and unrun gates are explicit.

## 2. Repository and version profile

- [ ] Checked-in Maven/Gradle wrapper is used.
- [ ] Java release/toolchain and CI/runtime JDK are known.
- [ ] Preview flags are consistent across compile/test/run/deploy or not introduced.
- [ ] Multi-module dependents are identified.
- [ ] Dependency/BOM/plugin versions come from the project.
- [ ] Added APIs/imports/config keys exist in those versions.
- [ ] Annotation processors and generated-source owners are known.
- [ ] Existing formatter/static-analysis/test conventions are followed.

## 3. Java language and modeling

- [ ] Record use matches transparent value/data-carrier semantics.
- [ ] Record components do not expose mutable arrays/collections unintentionally.
- [ ] Generated record equality/toString/serialization are acceptable.
- [ ] Sealed hierarchy is intentionally closed.
- [ ] Pattern switch is exhaustive; `default` does not hide future variants.
- [ ] `var` does not obscure important type/units.
- [ ] Value objects improve a real invariant rather than add ceremony.
- [ ] Entity/identity objects were not converted into records.
- [ ] No dynamic map/string schema replaced a clear type.

## 4. API, nullness, and generics

- [ ] Public API compatibility was assessed: source, binary, behavioral, serialization.
- [ ] Null/empty/absent semantics are explicit.
- [ ] `Optional` is used where absence is a return contract, not universally.
- [ ] Input ownership and defensive copying are clear.
- [ ] Returned collection mutability is documented/tested.
- [ ] No raw generics or unchecked casts were introduced without a localized proof.
- [ ] Wildcards follow caller needs rather than maximal generic cleverness.
- [ ] Overloads are unambiguous for null/lambda/varargs call sites.
- [ ] Exceptions exposed by the API are stable and meaningful.

## 5. Collections and streams

- [ ] Collection type preserves required order, duplicates, nulls, and mutability.
- [ ] `Stream.toList()`/`List.copyOf()` mutability and null behavior were checked.
- [ ] `toMap` has a deliberate duplicate-key policy.
- [ ] Stream pipeline is side-effect-free or a loop is used instead.
- [ ] No hidden quadratic scans for expected data size.
- [ ] Mutable objects are not hash keys/elements under changing equality fields.
- [ ] No `parallelStream()` was introduced without measurement/execution isolation.
- [ ] Large data is not materialized unnecessarily.
- [ ] Concurrent collection use protects compound invariants, not only individual calls.

## 6. Equality, numbers, text, and time

- [ ] `equals` and `hashCode` remain consistent and stable.
- [ ] Entity equality handles transient/persisted/proxy states.
- [ ] Comparator is consistent with equality where sorted collections require it.
- [ ] `BigDecimal` construction, scale, comparison, and rounding are deliberate.
- [ ] Integer overflow is handled for sizes/money/counters where relevant.
- [ ] Floating-point comparison has the right tolerance/model.
- [ ] Charset is explicit at byte/text boundaries.
- [ ] Locale is explicit for machine versus user text.
- [ ] Instant, local time, and zone are not conflated.
- [ ] `Clock` or equivalent makes time-sensitive logic deterministic.
- [ ] DST and boundary dates are tested when business rules depend on them.

## 7. Exceptions, resources, and I/O

- [ ] Exceptions are caught only where they can be handled or translated.
- [ ] Causes and interrupted status are preserved.
- [ ] Failures are not both logged and rethrown at multiple layers.
- [ ] Closeable resources have clear ownership and try-with-resources/lifecycle cleanup.
- [ ] Executors and clients are not created per call without ownership.
- [ ] Network operations have connect/read/request/total timeout policy.
- [ ] Paths are normalized and constrained for untrusted input.
- [ ] Archive/parser/body size and complexity are bounded.
- [ ] Serialization contract and unknown-field policy are protected.
- [ ] Sensitive data is not logged or returned.

## 8. Concurrency and async

- [ ] Workload is classified as CPU, blocking I/O, or reactive.
- [ ] Shared mutable state and publication are safe.
- [ ] Executor owner, bounds, queue, rejection, and shutdown are explicit.
- [ ] Common pool/parallel stream was not used accidentally.
- [ ] Cancellation and interruption propagate.
- [ ] Timeout stops or safely abandons underlying work.
- [ ] Retry is bounded and operation is idempotent.
- [ ] Virtual threads are not pooled and scarce resources remain bounded.
- [ ] Thread-local use is safe at projected virtual-thread scale.
- [ ] Pinning advice matches the actual JDK.
- [ ] Reactive chain has no detached subscription/blocking wait.
- [ ] Context propagation is framework-supported and cleaned up.
- [ ] Concurrency tests use deterministic synchronization and deadlines.

## 9. Architecture and dependency design

- [ ] Responsibility/change axes are cohesive.
- [ ] An added abstraction isolates a demonstrated variation or external boundary.
- [ ] There is no interface-per-class or generic base layer by default.
- [ ] Package/module dependencies do not become cyclic.
- [ ] Utility code belongs to a focused owner.
- [ ] Framework types do not invade core logic without a justified trade-off.
- [ ] Visibility is no broader than needed.
- [ ] New dependency is necessary, maintained, aligned, and approved by project policy.
- [ ] No overlapping library was added for an existing capability.

## 10. Persistence and transactions

- [ ] ORM/reactive stack is identified and consistent per path.
- [ ] Transaction start, completion, rollback, and flush timing are explicit.
- [ ] Interception actually applies to the invocation path.
- [ ] External calls inside transactions are justified and bounded.
- [ ] Database constraints enforce persisted invariants.
- [ ] Entity equality, IDs, cascades, and orphan removal are correct.
- [ ] Lazy loading does not escape into serialization unexpectedly.
- [ ] Query count/cardinality/pagination were checked where relevant.
- [ ] Streams/cursors close within transaction/resource lifetime.
- [ ] Locking and retry avoid lost updates and duplicate side effects.
- [ ] Applied migrations are not rewritten; rollout compatibility is staged.

## 11. Testing

- [ ] Test proves a named contract, not only method calls.
- [ ] Bugfix has defect proof, fix proof, and unchanged-behavior proof.
- [ ] Pure logic uses plain tests where possible.
- [ ] Framework behavior is tested through the framework.
- [ ] Mocks do not replace the boundary under test.
- [ ] Test data and mutable state are isolated.
- [ ] Time/randomness/concurrency are deterministic.
- [ ] Test discovery/count is confirmed.
- [ ] Production dialect/broker/runtime is represented where semantics differ.
- [ ] Golden/snapshot changes were reviewed semantically.
- [ ] Native-sensitive behavior has a native test when native is shipped.

## 12. Security

- [ ] Trust boundaries and protected assets are identified.
- [ ] Authentication and authorization are separate and both tested.
- [ ] Tenant/resource ownership is server-derived and enforced.
- [ ] SQL/query/path/URL inputs are parameterized, canonicalized, and constrained.
- [ ] Redirects and DNS are considered for outbound URL checks.
- [ ] Secrets/tokens/PII are not exposed in logs, metrics, traces, errors, or fixtures.
- [ ] Parsers/uploads/archives/queries have resource limits.
- [ ] Crypto/token validation uses established providers/frameworks.
- [ ] Non-idempotent actions are protected against retries/replay.
- [ ] Security dependency/config changes were validated against current guidance.

## 13. Quarkus project/build-time

- [ ] Quarkus platform/BOM/plugin/extension versions are known.
- [ ] Build-time versus runtime property phase is known.
- [ ] Bean/index/generated metadata effects were considered.
- [ ] Dev Services assumptions do not leak into production.
- [ ] Dev-mode success is not the only packaged-mode proof.
- [ ] Native is treated as a separate target where applicable.
- [ ] Broad reflection/resource registration was avoided.
- [ ] Static initialization does not freeze time/random/config/secrets unintentionally.

## 14. Quarkus CDI/ArC

- [ ] Bean has a documented discovery path/index.
- [ ] Scope matches lifecycle and concurrent access.
- [ ] Constructor injection is used for mandatory dependencies where safe.
- [ ] Qualifiers are type-safe and unambiguous; `@Named` is not abused.
- [ ] Producer-created resources have disposal/shutdown ownership.
- [ ] Transaction/security/retry/metrics interceptors apply to actual calls.
- [ ] Startup work is bounded, observable, and restart-safe.
- [ ] Programmatic lookup and unused-bean removal interact safely.
- [ ] Normal-scope proxyability/private-member/native implications are checked.

## 15. Quarkus REST/client execution

- [ ] Resource return type and annotations imply the intended dispatch for this version.
- [ ] No blocking work runs on event loop, including filters and serialization.
- [ ] Virtual-thread route is I/O-bound and downstream resources are bounded.
- [ ] Reactive route has no blocking ORM/client/wait.
- [ ] Request/response models protect wire contracts and entities remain internal.
- [ ] Validation, exception mapping, status, headers, and media types are tested.
- [ ] REST clients have lifecycle, timeouts, response mapping, TLS/SSRF controls.
- [ ] Retry is safe and idempotent.
- [ ] Security/trace/MDC context survives async boundaries correctly.

## 16. Quarkus messaging/scheduling

- [ ] Acknowledgment timing and failure behavior are explicit.
- [ ] Duplicate delivery is safe/deduplicated durably.
- [ ] Ordering/partition/concurrency assumptions are protected.
- [ ] DB and message atomicity is not overstated.
- [ ] Retry/dead-letter/replay behavior is defined.
- [ ] Scheduler overlap, misfire, time zone, and cluster ownership are defined.
- [ ] Fault-tolerance policy has a total deadline and honest fallback.
- [ ] Telemetry counts logical operation outcomes, not attempts as successes.

## 17. Quarkus config/security/observability

- [ ] Config keys, defaults, types, profiles, and phases are verified.
- [ ] Missing secrets/endpoints fail safely rather than use unsafe fallbacks.
- [ ] Route and method security precedence is tested.
- [ ] OIDC issuer/audience/tenant/token propagation are deliberate.
- [ ] Logs reflect terminal outcome and redact sensitive data.
- [ ] Metrics labels are bounded.
- [ ] Trace context crosses async work without leaks.
- [ ] Liveness/readiness semantics avoid restart storms and overload.

## 18. Final diff and evidence

Run or adapt:

```bash
python3 scripts/check_diff_scope.py .
python3 scripts/scan_java_risks.py . --format markdown
scripts/run_quality_gates.sh --root . --mode verify
```

Then verify:

- [ ] Diff contains only intended files and generated output policy is respected.
- [ ] Scanner candidates were inspected, not blindly fixed.
- [ ] Exact commands and results are recorded.
- [ ] No untracked artifact, debug output, secret, or temporary file remains.
- [ ] Residual risk and intentionally deferred work are named.
