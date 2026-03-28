# Assessment Checklists

Use these checklists during the final review pass.

## Repository-Level Checklist

- Skill scope matches Kotlin + Quarkus server code only
- Build tool, Quarkus version, Kotlin version, and JDK understood
- Key extensions identified
- Native target status known
- Package organization understood
- Execution model mapped for major entry points

## Architecture Checklist

- Package-by-feature preferred where practical
- No fake clean-architecture layers
- Resources are thin
- Services own orchestration
- Repositories or adapters own integration details
- Dead abstractions removed

## Kotlin Checklist

- `!!` minimized or removed
- `lateinit` only where justified
- data classes used for DTOs, not entities
- public APIs typed clearly
- scope functions not overused
- file names meaningful

## CDI Checklist

- Constructor injection by default
- Scopes sensible
- Qualifiers explicit
- No mutable singleton hazards
- No lifecycle surprises

## REST Checklist

- Quarkus REST used where appropriate
- HTTP DTOs separate from entities
- typed responses preferred
- validation at boundaries
- exception mapping consistent
- no blocking work on event loop

## Persistence Checklist

- ORM vs reactive choice intentional
- transaction boundaries explicit
- repositories own queries
- migrations present for real environments
- Panache style appropriate to app size

## Async Checklist

- one execution model per path
- no `runBlocking` in request handling
- no `GlobalScope`
- cancellation preserved
- virtual threads used only where appropriate

## Testing Checklist

- plenty of plain unit tests where possible
- component tests used for CDI slices
- `@QuarkusTest` focused on integration
- persistence rollback strategy clear
- native verification present if production needs it

## Security and Ops Checklist

- auth and authorization explicit
- dev-only auth not leaking to prod
- logs meaningful and safe
- health checks meaningful
- telemetry strategy coherent

## Final Output Checklist

- top risks prioritized
- target shape recommended
- staged plan defined
- verification commands exact
- deferred items named
