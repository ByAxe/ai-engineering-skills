# Collections, Streams, and Mutability

## Trap: `Stream.toList()` mutability

Before:

```java
List<String> names = source.stream()
    .map(User::name)
    .collect(java.util.stream.Collectors.toList());

names.sort(String.CASE_INSENSITIVE_ORDER);
```

A mechanical replacement can break at runtime:

```java
List<String> names = source.stream()
    .map(User::name)
    .toList();

names.sort(String.CASE_INSENSITIVE_ORDER); // UnsupportedOperationException
```

Choose the contract explicitly.

Mutable result:

```java
List<String> names = source.stream()
    .map(User::name)
    .collect(java.util.stream.Collectors.toCollection(java.util.ArrayList::new));

names.sort(String.CASE_INSENSITIVE_ORDER);
```

Unmodifiable result with sorting inside the pipeline:

```java
List<String> names = source.stream()
    .map(User::name)
    .sorted(String.CASE_INSENSITIVE_ORDER)
    .toList();
```

## Trap: duplicate keys

```java
Map<String, User> byEmail = users.stream()
    .collect(java.util.stream.Collectors.toMap(User::email, java.util.function.Function.identity()));
```

If duplicates are invalid, keep the failure but add a named validation/test. If “latest wins” is the business rule:

```java
Map<String, User> byEmail = users.stream()
    .collect(java.util.stream.Collectors.toMap(
        User::email,
        java.util.function.Function.identity(),
        (earlier, later) -> later,
        java.util.LinkedHashMap::new));
```

The merge and map supplier encode duplicate and encounter-order policies.

## When a loop is clearer

```java
List<Invoice> accepted = new ArrayList<>();
for (Invoice invoice : invoices) {
    if (!validator.isValid(invoice)) {
        audit.rejected(invoice.id());
        continue;
    }
    accepted.add(normalize(invoice));
}
```

A stream version would mix validation, audit side effects, filtering, and mapping. The loop exposes control flow and a breakpoint-friendly failure path.

## Tests

Protect:

- encounter order
- duplicate behavior
- null element/key policy
- result mutability
- aliasing/defensive copies
- large-input behavior when materialization matters
