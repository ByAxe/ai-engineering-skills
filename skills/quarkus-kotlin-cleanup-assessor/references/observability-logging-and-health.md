# Observability, Logging, and Health

This guide covers logs, traces, metrics, and health checks from a cleanup perspective.

## Logging

Prefer:

- one logger per class
- stable logger names
- contextual structured fields
- one meaningful log at a boundary over repeated log spam in every layer

Avoid:

- dynamic logger names
- logging whole request bodies with secrets
- logging the same exception in every layer
- `println`

## Structured Logging

When logs are centralized, JSON logging can improve machine readability and correlation.

Use it deliberately, especially in containerized deployments.

## Correlation

Make sure important logs can be tied together via:

- request IDs
- trace IDs
- user or tenant identifiers where appropriate
- job or message keys for background flows

## OpenTelemetry and Metrics

Prefer a coherent telemetry strategy instead of mixing unrelated observability stacks.

Good target:

- tracing enabled intentionally
- metrics consistent
- logs and traces correlate
- exporters and protocols standardized

## Health Endpoints

Quarkus health support gives standard endpoints such as:

- liveness
- readiness
- startup
- aggregate health

Keep checks meaningful:

- liveness says “should restart?”
- readiness says “should receive traffic?”

Avoid fake health checks that always report healthy.

## Management Interface

Review whether health and management endpoints should share the main server or live on a separate management interface.

## Example: Good Logging Boundary

```kotlin
@ApplicationScoped
class SyncCatalogService(
    private val client: CatalogClient,
    private val repository: CatalogRepository,
) {
    private val log = Logger.getLogger(SyncCatalogService::class.java)

    fun sync(): SyncResult {
        val startedAt = Instant.now()
        return try {
            val items = client.fetchAll()
            val saved = repository.replaceAll(items)
            log.infof("catalog_sync_success saved=%d durationMs=%d", saved, Duration.between(startedAt, Instant.now()).toMillis())
            SyncResult(saved)
        } catch (e: Exception) {
            log.error("catalog_sync_failure", e)
            throw e
        }
    }
}
```

## Review Questions

- Are logs structured enough to operate the service?
- Is there one clear telemetry strategy?
- Are health checks meaningful?
- Are readiness and liveness distinct?
- Are sensitive values excluded from logs?
