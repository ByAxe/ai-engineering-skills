# Task

A user says they run agents both locally and in a cloud workspace. The current task happened in a cloud workspace with repo write access through a branch/PR. The repository has `openspec/config.yaml`, `openspec/specs/`, `openspec/changes/`, `.github/workflows/`, and project docs, but no writable local agent memory directory and no proof that git hooks are installed in the cloud runner. Future cloud runs may be read-only/proposal-only.

The session learning is: OpenSpec verification for this repo must include an independent reviewer pass before sync/archive, and repeated missed verification commands should become an enforceable gate when possible.

Create `cloud-openspec-reflection.md` with the reflection routing recommendation. The grading expects that file as the solution artifact.
