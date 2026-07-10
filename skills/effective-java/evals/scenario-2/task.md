# Task

A modernization patch changed this code:

```java
List<Job> jobs = source.stream()
    .filter(Job::ready)
    .collect(Collectors.toList());
jobs.sort(comparing(Job::priority));
jobs.add(fallbackJob);
return jobs;
```

to:

```java
List<Job> jobs = source.stream()
    .filter(Job::ready)
    .toList();
jobs.sort(comparing(Job::priority));
jobs.add(fallbackJob);
return jobs;
```

Production now fails on the sort. The public method historically returns a mutable list, preserves encounter order before sorting, preserves duplicates, and accepts any null elements that the old collector accepted. The project targets Java 21.

Create `stream-mutability-fix-plan.md` with the root cause, smallest patch, contract analysis, focused regression tests, and exact verification gates. Avoid a broad stream rewrite.
