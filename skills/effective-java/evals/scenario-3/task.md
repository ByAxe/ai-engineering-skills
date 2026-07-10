# Task

A Quarkus service targeting Java 21 proposes annotating every REST endpoint with `@RunOnVirtualThread`. One endpoint performs CPU-heavy password hashing; request context is stored in a `ThreadLocal` containing a roughly 2 MB object; a JDBC pool has 20 connections; a legacy library synchronizes around a socket call; and no load test or JFR capture exists. The team believes virtual threads remove the need for concurrency limits.

Create `virtual-thread-assessment.md`. Recommend a staged policy per workload, identify what must be measured, protect downstream capacity and cancellation behavior, and state Java 21-specific pinning implications without prescribing blanket lock rewrites. Include Quarkus/JDK version checks and verification steps.
