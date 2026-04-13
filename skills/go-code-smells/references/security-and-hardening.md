# Security and Hardening Smells in Go Code

## Contents
- Boundary-first mindset
- Input and decoding smells
- Database and query smells
- Filesystem and path smells
- Randomness and secret handling smells
- Network and transport smells
- Security review prompts

## Boundary-first mindset

Most security smells in Go are ordinary code-smell categories at trust boundaries:
- permissive decoding
- path handling assumptions
- shell or query construction shortcuts
- weak randomness for secrets
- missing deadlines or cancellation

Security review starts by finding user-controlled input and following where assumptions become implicit.

## Input and decoding smells

### Accepting unknown fields silently where the input should be schema-bound
Consider stricter decoding for admin, security-sensitive, or contract-driven APIs.

### Late validation
Smell when untyped or weakly typed data travels deep into the system before validation.
Decode and validate early.

### Stringly typed authorization or state transitions
Refactor toward domain types and validation close to the boundary.

## Database and query smells

### Query construction with string interpolation
Use query parameters for values.

### Hidden transaction boundaries
When authorization and mutation are not in one explicit transaction or request boundary, correctness and security assumptions drift.

## Filesystem and path smells

### Assuming `filepath.Join` alone enforces a security boundary
It does not by itself solve traversal attacks with attacker-controlled path components.
Treat directory boundaries explicitly and choose a traversal-resistant approach appropriate to the environment.

### Temporary file or directory cleanup unclear
Make lifecycle and permissions explicit.

## Randomness and secret handling smells

### `math/rand` for tokens or secrets
Use cryptographically secure randomness for anything security-sensitive.

### Secrets logged or embedded in error strings
Wrap with contextual meaning but avoid leaking secret values.

## Network and transport smells

### No timeout or deadline policy
A security and reliability smell for networked systems.

### TLS or transport configuration hidden in ad hoc wrappers
If wrappers exist, they should clarify security policy, not obscure it.

## Security review prompts

When reviewing Go code, ask:
- Where does untrusted input enter?
- Where are schema, auth, and transaction boundaries?
- Which path or file operations could escape their intended root?
- Are secrets or tokens generated securely?
- Could indefinite hangs amplify operational or abuse risk?
- Do errors reveal too much implementation detail?
