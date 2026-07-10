# Task

A Quarkus REST endpoint is explicitly non-blocking and returns `Uni<Response>`:

```java
@GET
@NonBlocking
public Uni<Response> export() {
    return Uni.createFrom().item(() -> {
        List<OrderEntity> orders = OrderEntity.listAll();
        byte[] report = Files.readAllBytes(Path.of(config.reportTemplate()));
        return Response.ok(render(orders, report)).build();
    });
}
```

The project uses blocking Hibernate ORM with Panache, not Hibernate Reactive. The HTTP contract and transaction semantics must remain stable. A previous agent claimed wrapping the lambda in `Uni` made the code non-blocking.

Create `event-loop-fix-plan.md` with the execution-model diagnosis, compatible alternatives, smallest recommended patch, transaction considerations, focused tests, and thread/dispatch evidence to collect.
