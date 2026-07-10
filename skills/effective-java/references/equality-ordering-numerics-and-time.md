# Equality, Ordering, Numerics, and Time

These concerns create subtle Java bugs because code compiles and ordinary happy-path tests pass.

## `equals` and `hashCode`

Maintain the contracts: reflexive, symmetric, transitive, consistent, null-safe, and equal objects have equal hashes.

Common failures:

- subclass equality breaks symmetry
- mutable fields participate in a hash while an object is in a map/set
- arrays compare by identity through `Object.equals`
- records containing arrays inherit array identity equality
- cached hash is retained after mutable state changes
- entity equality changes before/after persistence assigns an identifier
- proxy subclasses make `getClass()` equality surprising

Use composition for value types when inheritance makes equality ambiguous. For arrays, use `Arrays.equals`/`deepEquals` and corresponding hash methods when content equality is intended.

## Records and equality

Generated record equality compares components using their normal equality. It is excellent for immutable value components and dangerous for mutable/identity components. Converting a class to a record is a behavior change unless the old equality already matched the record contract.

## Ordering

A comparator should usually be consistent with equality when used in sorted sets/maps; otherwise distinct objects may collapse into one sorted key. Always add a stable tie-breaker for pagination or deterministic output when the primary sort key is non-unique.

Avoid subtraction comparators such as `a.id() - b.id()` because of overflow. Use `Comparator.comparingInt` or `Integer.compare`.

## `BigDecimal`

Rules for financial/decimal domains:

- construct from decimal text or `BigDecimal.valueOf(double)`, not `new BigDecimal(double)` unless the exact binary value is intended
- define scale and rounding at the domain boundary
- `equals` is scale-sensitive (`2.0` differs from `2.00`); `compareTo` is numerical
- division may throw for non-terminating results without a rounding mode/MathContext
- do not silently normalize scale if serialization/database contracts preserve it
- be cautious using `BigDecimal` in sorted versus hashed collections because natural ordering is inconsistent with `equals`

Money also needs currency; a bare decimal is not a complete monetary value.

## Floating point

Review NaN, infinities, signed zero, comparison tolerance, accumulation error, and serialization. Do not use an arbitrary epsilon independent of value scale/domain. Use decimal arithmetic when exact decimal rules are required.

## Integer overflow

Overflow wraps silently for primitive integers. Check:

- multiplication before widening (`long x = intA * intB` still multiplies as int)
- size/count conversions
- timestamps/durations
- money in minor units
- comparator subtraction

Use `Math.addExact`, `multiplyExact`, range checks, or larger/domain types where overflow is unacceptable.

## Time type selection

- `Instant`: a point on the UTC timeline; good for persisted events and inter-service contracts
- `OffsetDateTime`: timestamp plus offset; useful when offset must be preserved
- `ZonedDateTime`: timeline point plus regional zone rules
- `LocalDate`: calendar date without time/zone
- `LocalDateTime`: wall-clock date-time with no unique timeline meaning
- `Duration`: time-based amount
- `Period`: date-based amount

Do not convert a local date-time to an instant without an explicit zone and DST policy.

## Clocks and determinism

Inject or pass a `Clock` at testable boundaries. Avoid scattered `Instant.now()`, `LocalDateTime.now()`, and `System.currentTimeMillis()` in domain logic. One operation should generally capture “now” once so comparisons are coherent.

Use monotonic elapsed-time sources (`System.nanoTime`) for duration measurement, not wall-clock time.

## DST and zone rules

Local times can be missing or duplicated during transitions. Define how scheduling, expiry, and daily aggregation handle gaps/overlaps. Store an instant for events and a zone identifier when future local scheduling must track regional rules.

## Locale and text

Use `Locale.ROOT` for protocol/config identifiers and case normalization that must not vary by user locale. Use the intended user locale for display. String case conversion is not a universal identifier canonicalization scheme; Unicode and security rules may require a domain-specific policy.

Specify charset at byte/text boundaries. Charset is covered further in `exceptions-resources-io-and-serialization.md`.

## Randomness and identifiers

Use `SecureRandom` or a vetted security API for secrets/tokens. Do not substitute UUID or `ThreadLocalRandom` automatically for cryptographic requirements. Inject deterministic randomness in tests where the algorithm allows it.

## Review checklist

- Can equality change while an object is keyed?
- Do arrays or proxies make equality surprising?
- Is comparator equality consistent and ordering deterministic?
- Are decimal construction, currency, scale, and rounding explicit?
- Can arithmetic overflow before widening?
- Does every local time have an explicit zone policy?
- Is “now” testable and captured consistently?
- Are locale and charset explicit at contracts?
