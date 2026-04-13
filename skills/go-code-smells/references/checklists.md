# Go Review Checklists

## Contents
- General review checklist
- Public API checklist
- Concurrency checklist
- Persistence and I/O checklist
- Performance checklist
- Release checklist

## General review checklist

- Is the package name clear and non-stuttering?
- Are exports justified and minimal?
- Is the simplest adequate abstraction being used?
- Are errors handled once and semantically?
- Is ownership of cleanup explicit?
- Are tests clear, stable, and behavior-oriented?
- Is the verification plan strong enough for the risk?

## Public API checklist

- Are interfaces owned by consumers unless the interface is the product?
- Are concrete types returned by default?
- Are zero values, nil semantics, and cleanup contracts documented or obvious?
- Does the API force callers into globals, registries, or hidden lifecycle coupling?
- Would adding a method later break callers because the API returned an interface too early?

## Concurrency checklist

- Who owns each goroutine?
- How does it stop?
- Can it block forever?
- Is channel close responsibility clear?
- Does cancellation propagate from the request or process boundary?
- Has the code been run with the race detector?

## Persistence and I/O checklist

- Are response bodies, rows, statements, files, and cancel functions cleaned up?
- Are queries parameterized?
- Are transactions explicitly committed or rolled back?
- Are timeouts or deadlines applied where needed?
- Are trust boundaries around paths, JSON, and external processes explicit?

## Performance checklist

- Is there a benchmark or profile for the claimed hotspot?
- Are allocation-heavy patterns visible in the evidence?
- Is the fix simpler than the problem?
- Did the team re-measure after the change?
- Did observability improve enough to keep future regressions visible?

## Release checklist

- Any exported API changes?
- Any behavior change visible to callers?
- Any migration notes needed?
- Any version-gated advice or features used?
- Any deferred work that should become a follow-up ticket?
