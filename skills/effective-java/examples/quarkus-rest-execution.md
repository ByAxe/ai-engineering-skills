# Quarkus REST Execution and DTO Boundary

Confirm the exact dispatch rules for the project’s Quarkus version. The examples show intent, not a version-independent guarantee.

## Blocking ORM path

```java
@Path("/orders")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class OrderResource {
    private final PlaceOrder service;

    OrderResource(PlaceOrder service) {
        this.service = service;
    }

    @POST
    @Transactional
    public Response place(@Valid PlaceOrderRequest request) {
        OrderReceipt receipt = service.place(request.toCommand());
        return Response.status(Response.Status.CREATED)
            .entity(OrderResponse.from(receipt))
            .build();
    }
}
```

The synchronous/transactional path is intended for blocking ORM on an appropriate worker thread. Test actual dispatch in the project generation; do not infer only from this snippet.

## Reactive path

```java
@Path("/catalog")
public class CatalogResource {
    private final CatalogClient client;

    CatalogResource(CatalogClient client) {
        this.client = client;
    }

    @GET
    public Uni<List<ItemResponse>> list() {
        return client.fetchItems()
            .map(items -> items.stream().map(ItemResponse::from).toList());
    }
}
```

Every call inside the chain must remain non-blocking. Adding blocking JPA, filesystem I/O, `.await()`, `join()`, or a synchronous client would require a deliberate dispatch/model change.

## Virtual-thread path

```java
@GET
@Path("/legacy/{id}")
@RunOnVirtualThread
public LegacyResponse legacy(@PathParam("id") String id) {
    return mapper.map(blockingLegacyClient.fetch(id));
}
```

Use only when supported and the work is primarily blocking I/O. Bound the legacy client’s connections and configure timeouts. Do not mark CPU-heavy routes universally.

## Boundary rules

- request DTO validates transport shape
- service/domain enforces business invariants and authorization context
- response DTO prevents entity/lazy/internal-field leakage
- exception mapping owns stable status/error envelopes
- success telemetry occurs after transaction/reactive completion
- tests assert status, headers, body, failure mapping, and authz
