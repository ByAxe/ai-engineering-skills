# Records and Value Semantics

## Trap: array components

```java
record Digest(byte[] bytes) {}
```

This is only shallowly immutable:

- callers can mutate `bytes`
- the accessor returns the same array
- generated record equality compares arrays by reference

A class can make ownership and deep equality explicit:

```java
import java.util.Arrays;
import java.util.HexFormat;
import java.util.Objects;

public final class Digest {
    private final byte[] bytes;

    public Digest(byte[] bytes) {
        Objects.requireNonNull(bytes, "bytes");
        this.bytes = bytes.clone();
    }

    public byte[] bytes() {
        return bytes.clone();
    }

    public String hex() {
        return HexFormat.of().formatHex(bytes);
    }

    @Override
    public boolean equals(Object other) {
        return this == other
            || other instanceof Digest digest && Arrays.equals(bytes, digest.bytes);
    }

    @Override
    public int hashCode() {
        return Arrays.hashCode(bytes);
    }
}
```

A record is appropriate when components already have the intended value/ownership semantics:

```java
import java.util.Objects;
import java.util.UUID;

public record CustomerId(UUID value) {
    public CustomerId {
        Objects.requireNonNull(value, "value");
    }

    public static CustomerId parse(String text) {
        return new CustomerId(UUID.fromString(text));
    }
}
```

## Trap: mutable collection component

```java
record Order(String id, java.util.List<String> lines) {}
```

If immutable ownership is the contract:

```java
public record Order(String id, java.util.List<String> lines) {
    public Order {
        java.util.Objects.requireNonNull(id, "id");
        lines = java.util.List.copyOf(lines);
    }
}
```

`List.copyOf` rejects null elements and returns an unmodifiable list. That is a behavior decision, not only defensive syntax.

## Characterization tests to add

- equal values compare equal after construction from distinct inputs
- caller mutation after construction does not change the object
- accessor mutation is impossible or isolated
- null component/element policy
- JSON/message representation if the type crosses a wire boundary
- public constructor/accessor compatibility if replacing an existing class

Do not convert a JPA entity to a record. Persistence identity, enhancement/proxies, lifecycle mutation, and equality need a different model.
