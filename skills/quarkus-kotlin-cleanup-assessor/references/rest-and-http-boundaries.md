# REST and HTTP Boundaries in Quarkus

Use this guide when resources, HTTP contracts, or REST clients need cleanup.

## Prefer Quarkus REST for New Quarkus Code

In modern Quarkus code, prefer `quarkus-rest` and related Quarkus REST extensions over RESTEasy Classic.

This gives a cleaner fit with Quarkus’ unified execution model and current recommendations.

## Keep Resources Thin

Resource responsibilities:

- transport validation
- calling the service
- response mapping
- HTTP-specific headers or status
- exception translation coordination

Resource anti-pattern:

```kotlin
@Path("/orders")
class OrderResource(
    private val repository: OrderRepository,
    private val paymentClient: PaymentClient,
) {
    @POST
    @Transactional
    fun create(request: CreateOrderRequest): Response {
        validateBusinessRules(request)
        val customer = paymentClient.fetchCustomer(request.customerId)
        val entity = OrderEntity(...)
        repository.persist(entity)
        audit("created", entity.id)
        return Response.status(201).entity(entity).build()
    }
}
```

Better:

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

## Prefer Typed Returns

Prefer:

- domain-safe DTOs
- `RestResponse<T>` when status and body both matter
- response annotations for simple static metadata

Avoid raw `Response` everywhere unless you truly need low-level control.

## Do Not Leak Entities Across HTTP

Avoid returning JPA entities directly.

Why:

- persistence shape becomes API shape
- lazy loading problems leak to HTTP
- native and serialization behavior gets harder to reason about
- refactoring persistence becomes harder

Map entities to transport-safe response models.

## Validate at the Boundary

Use Bean Validation or clear request validation close to the resource boundary.

Distinguish:

- malformed request
- invalid request
- business conflict
- missing resource
- infrastructure failure

## Exception Mapping

Use central exception mapping rather than ad-hoc `try/catch` in each resource.

Prefer `@ServerExceptionMapper` from Quarkus REST over the legacy `@Provider` + `ExceptionMapper<T>` pattern. It supports `RestResponse<T>` returns, CDI injection, and cleaner per-class or global scoping.

Pattern:

```kotlin
data class ApiError(
    val code: String,
    val message: String,
)
```

Global mapper (place in a standalone class outside any REST resource):

```kotlin
class ExceptionMappers {
    @ServerExceptionMapper
    fun mapCustomerAlreadyExists(
        exception: CustomerAlreadyExistsException,
    ): RestResponse<ApiError> =
        RestResponse.status(
            Response.Status.CONFLICT,
            ApiError(
                code = "CUSTOMER_EXISTS",
                message = exception.message ?: "Customer already exists",
            ),
        )
}
```

Per-resource mapper (place inside a specific resource class to scope it):

```kotlin
@Path("/customers")
class CustomerResource(private val service: CustomerService) {

    @ServerExceptionMapper
    fun mapNotFound(
        exception: CustomerNotFoundException,
    ): RestResponse<ApiError> =
        RestResponse.status(
            Response.Status.NOT_FOUND,
            ApiError(code = "CUSTOMER_NOT_FOUND", message = exception.message ?: "Not found"),
        )
}
```

Use a consistent error body contract across the service.

## Content Types

If you are not intentionally relying on JSON defaults, be explicit with `@Produces` and `@Consumes`.

This improves clarity and can reduce provider surface in native builds.

## Resource Method Size

A resource method should usually fit on one screen.

Smells:

- more than one remote dependency call
- transaction management
- retries
- mapping between multiple layers
- more than light branching

Move orchestration into a service.

## REST Clients

Prefer Quarkus REST Client for HTTP integrations.

Cleanup goals:

- one client interface per remote API or bounded slice
- typed request and response DTOs
- central config for base URL and timeouts
- explicit error mapping
- retries or fault tolerance only where justified

Avoid:

- `java.net.HttpURLConnection`
- copy-pasted low-level client code
- scattered remote URLs in services

## Pagination and Filters

Model query parameters explicitly:

```kotlin
data class OrdersQuery(
    val page: Int,
    val size: Int,
    val status: OrderStatus?,
)
```

Avoid large numbers of loose scalar parameters in service APIs when they belong together.

## OpenAPI and Dev Discoverability

When present, OpenAPI and Swagger UI should help document the contract during cleanup and regression review.

Use them to spot:

- odd status code patterns
- inconsistent DTO names
- hidden entity leakage
- overly broad request or response models

## REST Review Questions

- Are resources thin?
- Are status codes intentional?
- Are transport DTOs separate from entities?
- Are exceptions mapped consistently?
- Is blocking work kept off the event loop?
- Are remote clients centralized and typed?
