# Exceptions, Resources, and Boundaries

## Preserve causes and own logging

Avoid:

```java
try {
    return client.fetch(id);
} catch (Exception failure) {
    log.error("Fetch failed: " + failure.getMessage());
    throw new CustomerLookupException("Fetch failed");
}
```

Problems include broad recovery, eager/string logging, duplicate logs, and lost cause.

A boundary translation can be explicit:

```java
try {
    return client.fetch(id);
} catch (RemoteNotFound failure) {
    throw new CustomerNotFound(id, failure);
} catch (RemoteTimeout failure) {
    throw new CustomerDependencyUnavailable(id, failure);
}
```

Log once at the layer that owns the final operation outcome, including the exception object and safe correlation fields.

## Preserve interruption

```java
try {
    queue.put(command);
} catch (InterruptedException interrupted) {
    Thread.currentThread().interrupt();
    throw new CommandSubmissionInterrupted(interrupted);
}
```

The right API may instead declare `InterruptedException`. Do not restore and continue as if submission succeeded.

## Resource ownership

```java
HttpRequest request = HttpRequest.newBuilder(uri)
    .timeout(Duration.ofSeconds(3))
    .GET()
    .build();

HttpResponse<InputStream> response = client.send(
    request,
    HttpResponse.BodyHandlers.ofInputStream());

try (InputStream body = response.body()) {
    return parser.parse(body);
}
```

Also configure connection behavior at the client level and bound the body/parser according to the trust boundary.

## Files and charset

```java
String text = Files.readString(path, StandardCharsets.UTF_8);
Files.writeString(output, text, StandardCharsets.UTF_8);
```

For untrusted paths, charset is not enough: normalize/resolve against a trusted root and enforce containment, symlink policy, size, and permissions.
