# Go Code Review Template

## What is wrong
- Highest-risk smell:
- Why it matters:

## What should change
- Smallest safe refactor:
- Any API or migration note:

## What to verify
- formatting
- tests
- race detector if relevant
- vet/static analysis
- benchmark/profile if making performance claims

## Reviewer questions
- Is ownership of cleanup explicit?
- Is the interface in the right package?
- Are errors handled once and semantically?
- Can goroutines stop promptly?
- Did we simplify more than we added?
