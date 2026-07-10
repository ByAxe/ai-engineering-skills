# Task

A Java 21 service contains these public transport/value types:

```java
public record Digest(byte[] bytes) {}

public record SearchResult(List<String> hits) {}
```

The documented contract says two digests with the same byte contents are equal, callers must not be able to mutate either value through constructor arguments or accessors, and the existing JSON field names must remain unchanged. `SearchResult` must preserve order and duplicates. The team wants to keep records where they are a good fit and does not want a broad model rewrite.

Create `record-value-semantics-review.md` with an evidence-led assessment, the smallest safe change, compatibility risks, and tests that prove value equality, hash consistency, defensive ownership, null behavior, JSON compatibility, order, and duplicate preservation. Do not claim the current declarations are safe merely because records are immutable-looking.
