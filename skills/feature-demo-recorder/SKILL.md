---
name: feature-demo-recorder
description: Record, trim, and publish a short demo of a completed feature, then attach it to the GitHub PR. Use when a feature is implemented and needs a reviewer-facing visual demo showing where the new functionality lives, how it is used, and what changes on screen. Trigger this skill for requests to capture feature videos, make PR demo GIFs/MP4s, trim simulator recordings, or update PR descriptions with demo media.
metadata:
  author: ByAxe
  environment: Requires ffmpeg, ffprobe, gh auth, and either simulator tooling or another reproducible screen-recording path.
  version: 1.0.0
---

# Feature Demo Recorder

Create a short, reviewer-friendly demo of the new functionality only. Prefer an iOS simulator recording when the feature is cross-platform and does not require Android-specific behavior.

## Outcome

- Record a focused demo that shows:
  - where the feature lives
  - every newly interactive control in the flow
  - the visible result after the action completes
- Publish a lightweight GIF preview plus an MP4 download to GitHub.
- Update the PR description with a `## Demo` section.
- Remove temporary repo files and local scratch artifacts when done.

## Typical Requests

- "Record a short demo of this new settings flow and attach it to the PR."
- "Trim this simulator capture into a GIF and MP4 for reviewers."
- "Show where the new feature lives, tap all new controls, and upload the result to GitHub."

## Demo Rules

- Keep the clip between 8 and 20 seconds unless the feature genuinely needs more.
- Show only the new behavior and the minimum navigation needed to reach it.
- Use realistic state and data, but avoid long setup, login, or unrelated screens.
- Click every interactive element that is part of the new feature.
- End on the final state long enough for a reviewer to understand the result.
- Exclude idle waiting, notification prompts, loading retries, debug overlays, and repeated navigation unless they are part of the feature itself.

## Workflow

### 1. Scope the demo

- Inspect the completed feature and identify the smallest path that proves it works.
- Decide which screen should be the first visible frame.
- Decide which controls must be tapped and which visible state proves success.
- If the feature depends on data or auth, prepare that state before the recording starts.

### 2. Drive the UI deterministically

- Prefer a scripted flow over manual tapping so the recording is reproducible.
- For Flutter apps, use integration tests or platform MCP tooling to navigate into the exact state.
- If simulator/device popups can interrupt the demo, clear or auto-approve them before the final recording pass.

### 3. Record

- Prefer the iOS simulator recording toolchain if available:
  - `mcp__ios_simulator__record_video`
  - `mcp__ios_simulator__stop_recording`
- Keep recording broader than needed, then trim afterward.
- Do at least one dry run before the final capture.

### 4. Trim and generate assets

- Use `scripts/make_demo_assets.sh` to turn the raw recording into:
  - a trimmed MP4
  - a GIF preview suitable for embedding in a PR
- Choose start/end timestamps so the first frame already shows the feature entry point.
- Prefer 6 fps GIF output and moderate width scaling for small files.

### 5. Publish to GitHub

- Use `scripts/publish_pr_demo.py` with the PR number and generated assets.
- Publish assets to a prerelease named `pr-<number>-demo-assets`.
- Update or replace the PR `## Demo` section so it contains:
  - embedded GIF preview
  - MP4 download link

### 6. Verify and clean up

- Open or inspect the PR body to confirm the GIF renders.
- Confirm the worktree is still clean.
- Delete local scratch files that are no longer needed:
  - temporary integration tests created only for recording
  - raw captures if the published assets are enough
  - temporary palette images, screenshots, and `/tmp` body files

## Recommended Tools

- UI drive:
  - Flutter integration tests
  - iOS simulator MCP
  - Chrome/DevTools MCP if a web or GitHub browser interaction is required
- Processing:
  - `ffmpeg`
  - `ffprobe`
- GitHub publishing:
  - `gh`
  - `scripts/publish_pr_demo.py`

## When to Read References

- Read [references/feature_demo_playbook.md](references/feature_demo_playbook.md) when you need the concrete end-to-end command chain, trim guidance, cleanup checklist, or PR upload pattern.

## Scripts

- `scripts/make_demo_assets.sh`
  - Trim a raw screen recording and generate both MP4 and GIF outputs.
- `scripts/publish_pr_demo.py`
  - Upload or refresh GitHub release assets for a PR and patch the PR body `## Demo` section.
