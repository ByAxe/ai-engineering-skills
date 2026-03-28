# Idiomatic Quarkus + Kotlin Examples

Use these examples when the user wants concrete before-and-after guidance.

## Example 1: Constructor Injection Instead of Field Injection

### Before

```kotlin
@Path("/customers")
class CustomerResource {

    @Inject
    @field: Default
    lateinit var service: CustomerService

    @GET
    fun list(): List<CustomerResponse> {
        return service.list()
    }
}
```

### After

```kotlin
@Path("/customers")
class CustomerResource(
    private val service: CustomerService,
) {
    @GET
    fun list(): List<CustomerResponse> = service.list()
}
```

## Example 2: Thin Resource, Service Owns Workflow

### Before

```kotlin
@Path("/orders")
class OrderResource(
    private val repository: OrderRepository,
    private val paymentClient: PaymentClient,
) {
    @POST
    @Transactional
    fun create(request: CreateOrderRequest): Response {
        if (request.items.isEmpty()) {
            return Response.status(400).build()
        }

        val customer = paymentClient.fetchCustomer(request.customerId)
        val entity = OrderEntity().apply {
            customerId = customer.id
            total = request.items.sumOf { it.price }
        }

        repository.persist(entity)

        return Response.status(201).entity(entity).build()
    }
}
```

### After

```kotlin
@Path("/orders")
class OrderResource(
    private val service: CreateOrderService,
) {
    @POST
    fun create(request: CreateOrderRequest): RestResponse<OrderResponse> {
        val created = service.create(request.toCommand())
        return RestResponse.status(
            Response.Status.CREATED,
            created.toResponse(),
        )
    }
}
```

```kotlin
@ApplicationScoped
class CreateOrderService(
    private val repository: OrderRepository,
    private val paymentClient: PaymentClient,
) {
    @Transactional
    fun create(command: CreateOrderCommand): Order {
        require(command.items.isNotEmpty()) { "order must contain items" }

        val customer = paymentClient.fetchCustomer(command.customerId)
        val saved = repository.create(customer.id, command.items)
        return saved
    }
}
```

## Example 3: Config Mapping Instead of Scattered Properties

### Before

```kotlin
@ApplicationScoped
class CatalogClient {

    @ConfigProperty(name = "catalog.base-url")
    lateinit var baseUrl: String

    @ConfigProperty(name = "catalog.timeout-ms")
    var timeoutMs: Long = 0
}
```

### After

```kotlin
@ConfigMapping(prefix = "catalog")
interface CatalogConfig {
    fun baseUrl(): URI
    fun timeoutMs(): Long
}
```

```kotlin
@ApplicationScoped
class CatalogClient(
    private val config: CatalogConfig,
) {
    fun baseUrl(): URI = config.baseUrl()
}
```

## Example 4: Replace `!!` with Explicit Invariants

### Before

```kotlin
fun toCommand(request: CreateCustomerRequest): CreateCustomerCommand {
    return CreateCustomerCommand(
        id = UUID.fromString(request.id!!),
        email = request.email!!,
    )
}
```

### After

```kotlin
fun toCommand(request: CreateCustomerRequest): CreateCustomerCommand {
    val id = requireNotNull(request.id) { "id is required" }
    val email = requireNotNull(request.email) { "email is required" }

    return CreateCustomerCommand(
        id = CustomerId(UUID.fromString(id)),
        email = EmailAddress(email),
    )
}
```

## Example 5: Value Classes for Safer APIs

```kotlin
@JvmInline
value class CustomerId(val value: UUID)

@JvmInline
value class EmailAddress(val value: String)

data class CreateCustomerCommand(
    val id: CustomerId,
    val email: EmailAddress,
)
```

This prevents accidental swapping of raw strings and UUIDs.

## Example 6: Sealed Business Outcome

```kotlin
sealed interface RegisterCustomerResult {
    data class Success(val customerId: CustomerId) : RegisterCustomerResult
    data object EmailTaken : RegisterCustomerResult
}
```

```kotlin
@ApplicationScoped
class RegisterCustomerService(
    private val repository: CustomerRepository,
) {
    @Transactional
    fun register(command: RegisterCustomerCommand): RegisterCustomerResult {
        if (repository.findByEmail(command.email.value) != null) {
            return RegisterCustomerResult.EmailTaken
        }

        val customer = repository.create(command)
        return RegisterCustomerResult.Success(CustomerId(requireNotNull(customer.id)))
    }
}
```

## Example 7: Repository Over Entity Companion Sprawl

### Before

```kotlin
@Entity
class CustomerEntity : PanacheEntity() {
    companion object : PanacheCompanion<CustomerEntity> {
        fun findByEmail(email: String) = find("email", email).firstResult()
        fun create(email: String, name: String): CustomerEntity {
            val entity = CustomerEntity()
            entity.email = email
            entity.name = name
            entity.persist()
            return entity
        }
    }

    lateinit var email: String
    lateinit var name: String
}
```

### After

```kotlin
@Entity
class CustomerEntity {
    @Id
    @GeneratedValue
    var id: Long? = null
    lateinit var email: String
    lateinit var name: String
}
```

```kotlin
@ApplicationScoped
class CustomerRepository : PanacheRepository<CustomerEntity> {
    fun findByEmail(email: String): CustomerEntity? =
        find("email", email).firstResult()

    fun create(command: RegisterCustomerCommand): CustomerEntity =
        CustomerEntity().apply {
            email = command.email.value
            name = command.displayName
        }.also(::persist)
}
```

## Example 8: Make Blocking Intent Explicit with Virtual Threads

### Before

```kotlin
@Path("/reports")
class ReportResource(
    private val service: ReportService,
) {
    @GET
    fun generate(): ReportResponse = service.generateBlocking()
}
```

The method looks harmless, but it can run with the wrong execution assumptions.

### After

```kotlin
@Path("/reports")
class ReportResource(
    private val service: ReportService,
) {
    @GET
    @RunOnVirtualThread
    fun generate(): ReportResponse = service.generateBlocking()
}
```

Use this only when the path is I/O-bound and virtual-thread pinning concerns are understood.

## Example 9: Coroutine Service with Cancellation Safety

### Before

```kotlin
suspend fun sync() {
    runCatching {
        client.fetch()
    }.onFailure {
        log.error("sync failed", it)
    }
}
```

### After

```kotlin
suspend fun sync() {
    try {
        client.fetch()
    } catch (e: CancellationException) {
        throw e
    } catch (e: Exception) {
        log.error("sync failed", e)
        throw e
    }
}
```

## Example 10: Roll Back Database Changes in a Test

```kotlin
@QuarkusTest
class CustomerRepositoryTest {

    @Inject
    lateinit var repository: CustomerRepository

    @Test
    @TestTransaction
    fun `persists customer`() {
        repository.create(
            RegisterCustomerCommand(
                email = EmailAddress("a@acme.test"),
                displayName = "Aleksei",
            ),
        )

        assertNotNull(repository.findByEmail("a@acme.test"))
    }
}
```

## Example 11: Resource-Level Validation, Service-Level Meaning

```kotlin
data class CreateBookRequest(
    @field:NotBlank
    val title: String,

    @field:Min(1)
    val pages: Int,
)
```

```kotlin
@Path("/books")
class BookResource(
    private val service: CreateBookService,
) {
    @POST
    fun create(request: @Valid CreateBookRequest): RestResponse<BookResponse> =
        RestResponse.status(
            Response.Status.CREATED,
            service.create(request.toCommand()).toResponse(),
        )
}
```
