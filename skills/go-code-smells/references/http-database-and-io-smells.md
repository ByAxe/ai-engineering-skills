# HTTP, Database, Filesystem, JSON, and I/O Smells

## Contents
- HTTP client and server smells
- Database access smells
- Filesystem and path handling smells
- JSON and serialization boundary smells
- Randomness and security-sensitive I/O
- Cleanup rules to enforce

## HTTP client and server smells

### Response body not closed
One of the most common Go resource smells.
If an HTTP client call returns a response, close the body when done.

### No timeout or deadline strategy
Smell when outbound HTTP or downstream calls can hang indefinitely.
Use request contexts and appropriate client timeout configuration.

### Request not bound to context
Prefer `http.NewRequestWithContext` or request-scoped context propagation so cancellation and trace metadata flow correctly.

### Transport hidden behind unnecessary abstraction
Sometimes the smell is not HTTP itself but a package wrapping `http.Client` with a giant custom interface that adds no semantics.
Prefer a clear seam over a fake one.

## Database access smells

### Missing `rows.Close()` or `stmt.Close()`
Always close resources obtained from `database/sql` when done.

### Transaction not clearly committed or rolled back
A transaction must have a visible success path and a visible rollback path.
A common safe shape is:
- begin transaction
- `defer tx.Rollback()`
- perform work
- `return tx.Commit()` on success

### Mixing `sql.DB` calls inside a transaction flow
Smell when some operations use `tx` and others accidentally use `db`, producing inconsistent behavior or deadlocks.

### SQL built with string formatting
Use parameterized queries, not `fmt.Sprintf`, for values.

### Context-less database operations
Use `QueryContext`, `ExecContext`, and friends so request cancellation and timeouts propagate.

## Filesystem and path handling smells

### Treating user-controlled path pieces as trusted
Smell when `filepath.Join(base, userInput)` is assumed safe without considering traversal.

### Filesystem trust boundary not explicit
If the code must stay inside a directory boundary, use a traversal-resistant approach appropriate to the toolchain and platform, and document the boundary clearly.

For repositories on newer toolchains, review whether the standard library now offers a better root-bound filesystem API for this boundary. See `references/version-gated-modernization.md`.

### Hidden cleanup ownership
When a helper opens a file or stream, the API must make the cleanup contract obvious.

## JSON and serialization boundary smells

### Unknown fields silently accepted where the boundary should be strict
For security-sensitive or schema-controlled inputs, consider strict decoding instead of silently ignoring unknown keys.

### Comparing JSON strings in tests
Usually brittle. Decode and compare semantic structures instead.

### Using generic maps far past the boundary
Decode into typed structures as early as possible. Keep `map[string]any` near untyped edges.

## Randomness and security-sensitive I/O

### `math/rand` used for secrets, tokens, or keys
Use cryptographically secure randomness for security-sensitive values.

### Dangerous shelling out or unvalidated paths
Surface the trust boundary. Separate lexical validation from execution. Prefer argument arrays over shell command strings.

## Cleanup rules to enforce

Look for and make explicit ownership of:
- `resp.Body.Close()`
- `rows.Close()`
- `stmt.Close()`
- transaction rollback/commit
- opened files and directories
- cancel functions from derived contexts

If a function acquires a resource, the API should make it obvious who releases it.
