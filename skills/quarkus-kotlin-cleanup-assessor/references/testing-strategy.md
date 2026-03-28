# Testing Strategy for Quarkus + Kotlin

The goal is not “more tests everywhere.” The goal is fast, trustworthy feedback at the right level.

## Preferred Test Pyramid

### 1. Pure Kotlin Unit Tests

Use for:

- business rules
- mapping logic
- validation logic
- small orchestration with mocked collaborators

These should be the bulk of the suite where possible.

If coroutine code is involved, prefer coroutine test utilities like `runTest`.

### 2. `@QuarkusComponentTest`

Use for:

- CDI wiring of a focused slice
- service + repository mapper combinations
- bean interaction without booting the full app

This is a strong default for medium-complexity service tests.

### 3. `@QuarkusTest`

Use for:

- full application wiring
- resource behavior
- security integration
- config-driven behavior
- transaction behavior
- HTTP-level tests, often with REST Assured

Avoid using `@QuarkusTest` for everything if plain unit tests or component tests would do.

### 4. Native Verification

Use when the service actually ships native or the touched area is native-sensitive.

Native tests are slower and should be selective.

## Mocks and Fakes

Prefer:

- plain constructor-injected fakes for unit tests
- `@InjectMock`
- `QuarkusMock`

Avoid huge custom test harnesses when the framework already gives a simpler path.

## Persistence Tests

For tests that touch the database:

- keep fixture setup obvious
- avoid fragile test ordering
- use `@TestTransaction` when you want rollback after the test

Smell:

- `@Transactional` used on a test with the assumption that data will not persist afterward

## Dev Services

Dev Services can make local and test setup dramatically simpler.

Still verify:

- container startup cost is acceptable
- production assumptions are not hidden
- data setup is deterministic

## Security Tests

Security should be testable without standing up the whole identity platform for every test.

Use Quarkus security testing tools where appropriate to simulate users, roles, or disabled security for focused cases.

## Example: Component Test

```kotlin
@QuarkusComponentTest
class CustomerServiceTest {

    @Inject
    lateinit var service: CustomerService

    @InjectMock
    lateinit var repository: CustomerRepository

    @Test
    fun `returns customer when found`() {
        whenever(repository.findByEmail("a@acme.test")).thenReturn(
            CustomerEntity().apply { email = "a@acme.test"; displayName = "A" }
        )

        val result = service.findByEmail("a@acme.test")

        assertEquals("A", result?.displayName)
    }
}
```

## Example: Coroutine Unit Test

```kotlin
class SyncCatalogServiceTest {

    @Test
    fun `sync returns imported count`() = runTest {
        val client = FakeCatalogClient(items = listOf("a", "b"))
        val repository = FakeCatalogRepository()
        val service = SyncCatalogService(client, repository)

        val result = service.sync()

        assertEquals(2, result.imported)
    }
}
```

## Test Review Questions

- Can business rules be tested without Quarkus boot?
- Are CDI slices covered with component tests?
- Are app-level concerns covered with `@QuarkusTest`?
- Are persistence tests rolled back when appropriate?
- Are native-sensitive paths verified if native is a real target?
