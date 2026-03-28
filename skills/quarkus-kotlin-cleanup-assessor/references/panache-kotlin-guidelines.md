# Panache with Kotlin: Cleanup Guidance

Panache can be productive in Kotlin, but it is easy to overuse. This guide explains the clean target style.

## Repository Pattern vs Active Record

### Use Repository Pattern by Default in Medium and Large Apps

Prefer:

```kotlin
@ApplicationScoped
class CustomerRepository : PanacheRepository<CustomerEntity> {
    fun findByEmail(email: String): CustomerEntity? =
        find("email", email).firstResult()
}
```

Why:

- better separation between persistence and orchestration
- easier tests
- less domain logic trapped in entities
- better feature scaling as the codebase grows

### Active Record Is Fine for Tiny CRUD

Active record can be acceptable in small, simple services or quickstarts.

It becomes messy when:

- queries multiply
- workflows span several aggregates
- services need transactions across multiple repositories
- entity companion objects become persistence god-objects

## Companion Object Rules

In Kotlin Panache active record, static-like query helpers live in the `companion object`.

Keep those helpers:

- short
- persistence-specific
- close to one entity

Avoid putting:

- orchestration
- cross-entity workflows
- remote calls
- business policies

in entity companion objects.

## Entity Shape

Panache Kotlin entities are usually regular classes, not data classes.

Common patterns:

- nullable `id`
- `lateinit` fields for JPA-managed non-null properties

This is acceptable in the persistence layer when the ORM lifecycle truly requires it.

It is **not** a license to spread `lateinit` through the whole codebase.

## Do Not Use Entities as Your Domain Model by Default

For small CRUD, that may be tolerable.

For medium and larger systems, prefer:

- entity for persistence
- domain or service-facing model where invariants matter
- transport DTOs at the boundary

## Transactions and Panache

Keep transaction ownership in services for business workflows.

Avoid hiding important transaction semantics inside active-record helpers when the use case is bigger than one entity call.

## Streams Need Care

Panache stream operations typically require an active transaction or session context. Be careful not to stream lazily outside the correct lifecycle.

## Cleanup Heuristic

If the codebase contains:

- many entity companion methods
- services that call entity static helpers everywhere
- difficult mocking or testing
- entity leakage over HTTP

move toward repositories.

## Example: Good Medium-App Shape

```kotlin
@Entity
class CustomerEntity {
    @Id
    @GeneratedValue
    var id: Long? = null
    lateinit var email: String
    lateinit var displayName: String
}
```

```kotlin
@ApplicationScoped
class CustomerRepository : PanacheRepository<CustomerEntity> {
    fun findByEmail(email: String): CustomerEntity? =
        find("email", email).firstResult()
}
```

```kotlin
@ApplicationScoped
class RegisterCustomerService(
    private val repository: CustomerRepository,
) {
    @Transactional
    fun register(command: RegisterCustomerCommand): Customer {
        check(repository.findByEmail(command.email) == null) {
            "Customer already exists"
        }

        val entity = CustomerEntity().apply {
            email = command.email
            displayName = command.displayName
        }
        repository.persist(entity)
        return Customer(
            id = requireNotNull(entity.id),
            email = entity.email,
            displayName = entity.displayName,
        )
    }
}
```
