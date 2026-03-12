# Frontend Security Smells in TypeScript

This is a practical catalog of common security smells in frontend TypeScript codebases. Fixes should align with the project's security policies.

## Contents
- SEC-01 Unsafe HTML injection (XSS risk)
- SEC-02 Building URLs and redirects unsafely
- SEC-03 Trusting external data without validation
- SEC-04 Storing sensitive tokens in risky places
- SEC-05 Exposing secrets in client bundles
- SEC-06 Loading third-party scripts unsafely
- SEC-07 Unsafe postMessage usage
- SEC-08 Eval and dynamic code execution
- Refactor checklist

---

## SEC-01 Unsafe HTML injection (XSS risk)

### Symptoms
- Setting innerHTML with user-controlled content.
- Using dangerouslySetInnerHTML without sanitization.

### Refactor strategy
- Prefer rendering text nodes.
- If HTML rendering is required, sanitize using a project-approved sanitizer and apply a strict allowlist.

---

## SEC-02 Building URLs and redirects unsafely

### Symptoms
- Concatenating user-controlled strings into URLs.
- Redirect targets taken from query params without validation.

### Refactor strategy
- Use URL and URLSearchParams APIs.
- Validate redirect targets against an allowlist of paths.

---

## SEC-03 Trusting external data without validation

### Symptoms
- API response assumed correct and cast with assertions.
- localStorage data parsed and used directly.

### Refactor strategy
- Validate data at boundaries.
- Convert unknown data to trusted domain models via mappers.

---

## SEC-04 Storing sensitive tokens in risky places

### Symptoms
- Long-lived auth tokens stored in localStorage or sessionStorage by default.
- Tokens accessible to JavaScript in environments where XSS is a concern.

### Refactor strategy
- Follow the project's auth strategy.
- Prefer safer storage patterns when possible (for example, httpOnly cookies managed by the server) if aligned with backend and security requirements.

---

## SEC-05 Exposing secrets in client bundles

### Symptoms
- API keys or secrets hard-coded.
- Environment variables exposed without understanding which are public.

### Refactor strategy
- Treat frontend code as public.
- Move secrets to the server.
- Ensure build-time env vars are safe to expose.

---

## SEC-06 Loading third-party scripts unsafely

### Symptoms
- Injecting script tags with dynamic URLs.
- No integrity or allowlist.

### Refactor strategy
- Avoid dynamic script injection unless necessary.
- Use a strict allowlist and integrity attributes when supported.
- Prefer bundling dependencies instead of runtime injection.

---

## SEC-07 Unsafe postMessage usage

### Symptoms
- Accepting messages from any origin.
- No schema validation of message payload.

### Refactor strategy
- Validate origin.
- Validate message schema before acting.
- Avoid executing commands based on untrusted messages.

---

## SEC-08 Eval and dynamic code execution

### Symptoms
- eval, new Function, or dynamic code execution.
- Rendering untrusted templates.

### Refactor strategy
- Remove eval usage.
- Use safe parsers or declarative config formats.

---

## Refactor checklist

- [ ] Identify trust boundaries (user input, network, storage, postMessage).
- [ ] Avoid unsafe HTML injection; sanitize only when necessary.
- [ ] Validate external data before it enters core logic.
- [ ] Ensure tokens and secrets follow security policy.
- [ ] Reduce dynamic script loading and dynamic code execution.
