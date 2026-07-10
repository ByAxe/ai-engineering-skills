# Task

A Quarkus application works on the JVM but fails as a native executable. It loads a serializer with `Class.forName(config.serializerClass())`, reads `/templates/invoice.html` from the classpath, and has this static initialization:

```java
static final Instant STARTED = Instant.now();
static final String NONCE = UUID.randomUUID().toString();
static final String API_TOKEN = System.getenv("API_TOKEN");
```

A proposed fix registers the entire company package for reflection and embeds all resources. Production needs runtime-specific tokens and a fresh nonce per process.

Create `native-readiness-plan.md` with exact hypotheses, targeted remedies, JVM/native contract checks, and a native test plan. Avoid broad reflection/resource registration.
