# Spring-Shaped Code in a Quarkus Kotlin Service

Use this guide when the codebase “works” but still looks mentally modeled after Spring Boot.

## Principle

Quarkus provides Spring compatibility extensions, but a cleanup pass for a Quarkus-native codebase should usually converge toward Quarkus and Jakarta APIs.

Keep compatibility layers when:

- the codebase is mid-migration
- a large untouched surface still depends on them
- changing them now would create unnecessary risk

Prefer native Quarkus style in new or heavily touched code.

## Common Spring-to-Quarkus Mismatches

### Controllers vs Resources

Spring habit:

- `@RestController`
- `@RequestMapping`
- `ResponseEntity`

Quarkus-native target:

- `@Path`
- Jakarta REST method annotations
- typed DTO returns or `RestResponse<T>`

### `@Autowired` and Field Injection

Spring habit:

- `@Autowired`
- field injection everywhere

Quarkus-native target:

- constructor injection
- CDI scopes and qualifiers

### `@ConfigurationProperties`

Spring habit:

- config classes modeled after Spring Boot configuration

Quarkus-native target:

- `@ConfigMapping`
- grouped config interfaces

### Spring Data as Default House Style

Spring habit:

- repository methods inferred from method names
- Spring Data patterns used everywhere

Quarkus-native target:

- Panache repositories or explicit repositories
- queries where they are owned and reviewable

### `@ComponentScan`, `@Import`

Spring habit:

- manual component scanning narratives

Quarkus-native target:

- Quarkus bean discovery and build-time indexing
- explicit CDI composition

### Response Wrapping

Spring habit:

- `ResponseEntity<?>` everywhere

Quarkus-native target:

- typed resource returns
- `RestResponse<T>` only where status or headers need explicit control

### Scheduling

Spring habit:

- Spring scheduling defaults

Quarkus-native target:

- `quarkus-scheduler`
- `quarkus-quartz` only for advanced persistent or clustered scheduling

## Migration Heuristics

Good cleanup policy:

- keep compatibility layers at untouched boundaries
- convert actively refactored features to Quarkus-native style
- do not mix two house styles inside the same feature package

## Signs the App Is Still Mentally Spring

- new code uses Spring annotations first and Quarkus docs second
- every response is wrapped the Spring way
- configuration modeled around Spring compatibility even where Quarkus-native config is cleaner
- data access patterns copied from Spring Data instead of chosen deliberately

## Cleanup Questions

- Is this compatibility layer still buying migration safety?
- Would Quarkus-native style be clearer for this touched area?
- Are two framework vocabularies coexisting inside one feature?
