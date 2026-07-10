# Task

A Quarkus application has two payment gateway beans. Both are annotated with `@Named`, injection by type is ambiguous, and one gateway lives in a dependency JAR that has no Jandex index and no `beans.xml`. A different plugin bean is looked up only with `CDI.current().select(...)` using a class name from configuration and disappears in production after unused-bean removal. A prior patch disabled bean removal globally and added field injection everywhere.

Create `arc-diagnosis.md` with separate root causes, the smallest remedies, build-time discovery and qualifier checks, lifecycle/scope considerations, and JVM plus packaged/native verification. Do not solve every issue by disabling optimization globally.
