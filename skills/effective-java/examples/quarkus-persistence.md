# Quarkus Persistence Boundaries

## Blocking ORM use case

```java
@ApplicationScoped
class RegisterCustomer {
    @Transactional
    CustomerId register(RegisterCustomerCommand command) {
        CustomerEntity entity = CustomerEntity.from(command);
        entity.persist();
        return new CustomerId(entity.id);
    }
}
```

The transaction encloses one state transition. A database uniqueness constraint must protect unique email/identifier rules; a prior `count()` check alone is racy.

## Reactive Panache shape

```java
@ApplicationScoped
class RegisterCustomerReactive {
    @WithTransaction
    Uni<CustomerId> register(RegisterCustomerCommand command) {
        CustomerEntity entity = CustomerEntity.from(command);
        return entity.persist()
            .replaceWith(() -> new CustomerId(entity.id));
    }
}
```

Use only with the project’s Hibernate Reactive/Panache API and supported transaction annotation. Do not add `.await().indefinitely()` to make it resemble blocking ORM.

## Entity versus response

```java
@Entity
class CustomerEntity extends PanacheEntity {
    String email;
    String internalRiskCode;
    @Version long version;
}

record CustomerResponse(long id, String email) {
    static CustomerResponse from(CustomerEntity entity) {
        return new CustomerResponse(entity.id, entity.email);
    }
}
```

A dedicated response protects internal fields, optimistic-lock metadata, lazy relationships, and future persistence refactors. Keep mapping small; a mapper framework is not mandatory.

## External side effect

Avoid charging a card or publishing a message inside a long database transaction without an atomicity/idempotency design. Consider a transactional outbox, persisted intent plus idempotent processor, or saga. A Java transaction annotation cannot make an HTTP call and database commit atomic.

## Tests

- uniqueness constraint under concurrent attempts
- rollback on domain failure
- commit before emitted success/outbox consumption
- lazy relationship not traversed by serialization
- query count for list endpoint
- reactive failure/cancellation rolls back
- production dialect behavior where it differs
