# Persistence, Transactions, and Migrations

Use this guide when database access, transaction scope, or schema management needs cleanup.

## Choose ORM vs Reactive Deliberately

Most Quarkus services do **not** need Hibernate Reactive just because it exists.

Use classic Hibernate ORM when:

- the code is primarily synchronous
- JDBC access is fine
- transaction semantics are straightforward
- the team wants simpler code

Consider reactive persistence only when:

- the full request path is reactive
- concurrency profile justifies it
- the team can maintain reactive semantics end-to-end

Do not mix models casually.

## Put Transaction Boundaries in the Right Place

Prefer transaction boundaries in application services for non-trivial workflows.

Example:

```kotlin
@ApplicationScoped
class CreateInvoiceService(
    private val repository: InvoiceRepository,
    private val eventPublisher: InvoiceEventPublisher,
) {
    @Transactional
    fun create(command: CreateInvoiceCommand): Invoice {
        val invoice = repository.create(command)
        eventPublisher.invoiceCreated(invoice)
        return invoice
    }
}
```

Avoid:

- transaction annotations scattered randomly
- resources owning large transactions by default
- helper methods starting hidden transactions

## Keep Entities Persistence-Oriented

Entities should model persistence concerns, not public transport contracts.

Good practices:

- separate request and response DTOs
- map entities to domain or API-safe models
- keep entity lifecycle concerns local to persistence

Avoid:

- returning entities directly
- serializing lazy graphs by accident
- putting remote-call orchestration inside entity methods

## Migrations Over Hope

In real environments, prefer versioned migrations with Flyway or Liquibase.

Smells:

- relying on schema auto-generation in production
- schema drift between environments
- no reliable upgrade history

Cleanup task:

- ensure one migration strategy is the source of truth

## Query Ownership

Repositories should own query logic.

Avoid:

- query strings in resources
- persistence logic in services
- different services each writing their own variant of the same query

## Entity vs DTO Example

Avoid:

```kotlin
@Entity
class CustomerEntity {
    @Id
    var id: UUID? = null
    lateinit var email: String
}

@Path("/customers")
class CustomerResource(
    private val repository: CustomerRepository,
) {
    @GET
    fun list(): List<CustomerEntity> = repository.listAll()
}
```

Prefer:

```kotlin
data class CustomerResponse(
    val id: UUID,
    val email: String,
)

@Path("/customers")
class CustomerResource(
    private val service: CustomerQueryService,
) {
    @GET
    fun list(): List<CustomerResponse> = service.list()
}
```

## Testing Transactions

In persistence-heavy tests, use `@TestTransaction` when you want rollback after the test.

Avoid assuming `@Transactional` tests will automatically revert database changes.

## Datasource Hygiene

Check:

- datasource config is centralized
- timeouts and pool settings are intentional
- test and prod settings are separated
- Dev Services are not confused with production provisioning

## Persistence Review Questions

- Is the chosen persistence model intentional?
- Are transaction boundaries obvious?
- Are entities kept out of transport contracts?
- Is schema evolution managed with real migrations?
- Are repositories the only place where queries live?
