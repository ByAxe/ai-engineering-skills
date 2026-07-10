# Collections, Streams, and Mutability

Collection choice is part of the contract. Preserve order, duplicates, null policy, mutability, view/copy behavior, and element ownership.

## Mutability and ownership matrix

| Construction | Important behavior |
|---|---|
| `List.of(...)` | unmodifiable; rejects null elements |
| `List.copyOf(source)` | unmodifiable snapshot; rejects nulls; may reuse an already unmodifiable list |
| `stream.toList()` | unmodifiable list; encounter order when present; no implementation/serializability guarantee |
| `Collectors.toList()` | no guarantee of implementation, mutability, serializability, or thread-safety |
| `Collectors.toCollection(ArrayList::new)` | explicit mutable implementation |
| `Collections.unmodifiableList(list)` | unmodifiable view; underlying list changes remain visible |
| `new ArrayList<>(source)` | shallow mutable copy |
| `Arrays.asList(array)` | fixed-size list backed by the array |
| `subList(...)` | view backed by the original list; structural changes can invalidate behavior |

Never replace one with another without checking callers.

## Defensive copying

A shallow copy protects the collection structure, not mutable elements. Decide whether the API owns:

- only the container
- the elements too
- neither (documented borrowed view)

Copy on ingress and/or egress according to ownership. Records need the same analysis; final components can still point to mutable state.

## Type communicates semantics

- `List`: ordered, duplicates allowed
- `Set`: unique, order not promised
- `LinkedHashSet`: unique with encounter order
- `SortedSet`/`NavigableSet`: comparator-defined ordering
- `Map`: key uniqueness, order implementation-dependent
- `LinkedHashMap`: encounter order
- `SortedMap`/`NavigableMap`: comparator-defined ordering
- Java 21 sequenced interfaces: explicit first/last/reverse semantics

Do not rely on `HashMap`/`HashSet` iteration order, even when tests appear stable.

## Equality and mutable elements

A collection’s equality/hash behavior delegates to elements/entries. Mutable keys or set elements can become unreachable after fields used by `equals`/`hashCode` change. Do not use mutable identity state as a hash key.

## Streams: use when the data flow is clearer

Good fits:

- map/filter/reduce pipelines with small stateless steps
- declarative aggregation
- bounded transformations where encounter order is understood

Prefer a loop when:

- there are multiple mutable accumulators
- early exits or complex control flow matter
- checked failure handling dominates
- debugging/stepwise state is clearer
- the pipeline requires side effects to work

## Stream correctness rules

- behavioral functions should be non-interfering and usually stateless
- do not modify the source during traversal unless the source explicitly supports it
- a stream is single-use
- close streams backed by I/O, such as `Files.lines`, with try-with-resources
- do not rely on `peek` for required side effects; stages may be optimized/elided in permitted cases
- preserve encounter order when business output depends on it
- distinguish `findFirst` from `findAny`

## Collectors

### Duplicate keys

`Collectors.toMap` without a merge function throws on duplicate keys. Choose deliberately:

- reject duplicates
- first wins
- last wins
- combine values
- group values

A silent last-wins merge can hide data defects.

### Grouping and ordering

Default collector map types may not preserve desired order. Supply an explicit map factory when order matters. Downstream collectors can produce mutable collections; document or copy before exposure.

### Numeric reductions

Avoid lossy floating arithmetic for money. Check integer overflow and empty-input semantics. Ensure reduction functions are associative before parallel execution.

## Parallel streams

Do not introduce `parallelStream()` as a generic performance fix. Evaluate:

- data size and operation cost
- common-pool contention in a server
- blocking operations
- ordering cost
- thread-local/context propagation
- thread-safety and associativity
- benchmark evidence

Use an explicitly managed execution strategy when concurrency is a product requirement.

## Concurrent collections

Thread-safe collection operations do not make multi-step invariants atomic. Prefer atomic methods such as `compute`, `merge`, or purpose-built synchronization, but keep mapping functions short and side-effect-light. Understand weakly consistent iterators and callback reentrancy.

## Nulls

JDK immutable factories reject null. Many mutable collections permit it, but null keys/elements often blur “missing” with “present null.” Preserve existing behavior during refactors or migrate with an explicit contract.

## Java 21 sequenced views

`reversed()` returns a reverse-ordered view. If mutation is supported, writes can reflect into the original. `getFirst`/`getLast` throw on empty collections. Sorted collections may reject explicit positioning operations. Test these semantics before replacing copy-based code.

## Review checklist

- Is order required and represented by the type?
- Are duplicates accepted, merged, or rejected explicitly?
- Is the returned collection mutable, copied, or a live view?
- Are null elements legal?
- Can mutable keys/elements invalidate hashing?
- Are stream lambdas stateless and side-effect-free?
- Are I/O streams closed?
- Is any parallelism justified and isolated?
