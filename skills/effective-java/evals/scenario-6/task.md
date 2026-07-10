# Task

A Quarkus endpoint uses Hibernate Reactive Panache but was copied from a blocking service:

```java
@Transactional
public Uni<Order> create(CreateOrder request) {
    Order order = map(request);
    order.persistAndFlush().await().indefinitely();
    eventBus.publish(new OrderCreated(order.id));
    return Uni.createFrom().item(order);
}
```

The event must not be observed as committed when the database transaction later fails. Retries may occur at the HTTP gateway. The team wants the smallest safe repair, not a move back to blocking ORM.

Create `reactive-transaction-review.md` with the execution/transaction diagnosis, a correctly composed approach supported by the project version, commit-consistency options, idempotency strategy, failure/cancellation tests, and exact verification gates.
