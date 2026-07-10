# Testing, Debugging, and Test Doubles

Tests are executable contracts. Optimize for signal, determinism, and the correct boundary.

## Choose the smallest faithful test

- **Pure unit test:** algorithms, policies, value types, mapping without framework behavior
- **Parameterized/property-style test:** parsers, validators, state machines, reducers, boundary matrices
- **Component/slice test:** dependency injection, interceptors, serialization components
- **Integration test:** database, messaging, HTTP clients, transactions, framework runtime
- **Artifact test:** packaged JAR/container/native executable
- **Contract test:** public HTTP/event/schema compatibility

Do not use a slow framework test for pure logic, and do not use a mocked unit test to claim a framework integration works.

## Regression structure for a fix

Prove three things:

1. the defect condition is represented
2. corrected behavior occurs
3. adjacent unchanged behavior remains protected

A test that would already pass before the change is not defect proof.

## Test design

- name the behavior and condition
- arrange only relevant state
- assert outcome, externally meaningful state, or contract
- include negative and boundary cases
- avoid duplicating implementation logic in expected calculations
- use explicit fixed data for time, locale, zone, randomness, and IDs
- keep failures diagnostic

## Mocks and fakes

Mock external collaboration or hard boundaries, not simple values or the subject under test. Prefer a fake/in-memory implementation when stateful behavior matters and it remains faithful enough.

Warning signs:

- many mocks to construct one class
- tests verify call order that is not contractual
- deep stubs
- mocking static/domain methods because architecture is hard to reach
- every dependency returns a canned happy path
- interaction assertions replace result assertions

A mock can prove orchestration but not SQL, serialization, CDI interception, REST client configuration, or transaction behavior.

## Time and concurrency

Inject `Clock` and controllable schedulers where practical. Avoid sleeps; use latches, barriers, eventually assertions with bounded deadlines, or test framework facilities. Always fail with a timeout rather than hang.

Test interruption/cancellation and saturation for async code where those are part of the contract.

## Database tests

- use the same database family when dialect/locking behavior matters
- isolate data and transactions
- test constraints and migrations, not only repository mocks
- avoid relying on unspecified row order
- make rollback semantics explicit
- verify optimistic/pessimistic locking under realistic transaction boundaries

## HTTP and serialization tests

Assert status, headers, body shape, null/absent fields, error mapping, authz, and media type. Avoid brittle full-string JSON comparison unless exact formatting is contractual; use structural assertions.

## Quarkus test selection

- plain JUnit for pure Java
- `@QuarkusComponentTest` for focused CDI components when supported by the project version
- `@QuarkusTest` for application runtime/HTTP integration
- `@QuarkusIntegrationTest` for the built artifact
- transaction test annotations only when their rollback/commit semantics match the claim
- native integration tests when production ships native and the changed feature is native-sensitive

Read `quarkus-testing-dev-services-and-native.md` before choosing annotations.

## Flaky test diagnosis

Classify the nondeterminism:

- time/zone/locale
- order or shared state
- concurrency/race
- port/network/resource lifecycle
- database isolation
- random data
- asynchronous completion
- dependency/environment drift

Do not “fix” flakiness by increasing sleeps or retries before identifying the class.

## Debugging loop

1. reduce to the smallest failing command/test
2. read the first causal failure, not only the final wrapper exception
3. inspect generated/effective configuration
4. compare expected thread/transaction/classloader/context with actual
5. add temporary targeted diagnostics without leaking secrets
6. verify competing hypotheses
7. remove temporary noise after adding a durable regression guard

For Quarkus dev mode, remember hot reload can differ from clean packaged startup; reproduce in the appropriate mode.

## Test quality review

- Would it fail for the known bad behavior?
- Does it assert a contract rather than implementation trivia?
- Is the real risky boundary exercised?
- Is it deterministic across locale, zone, order, and time?
- Are cleanup and resource ownership reliable?
- Does the chosen Quarkus test layer match the claim?
- Is test discovery proven by output?
