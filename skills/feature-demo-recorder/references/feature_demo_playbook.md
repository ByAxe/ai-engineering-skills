# Feature Demo Playbook

Use this as the exact operating sequence for reviewer-facing feature demos.

## 1. Pick the demo slice

- Start at the first screen where the feature is visible.
- Include only the taps needed to prove the feature.
- End on the completed state.

Good examples:

- Open Settings, show the new section, open the picker, choose an option, save, show the resulting localized state.
- Open a new form, toggle the new control, submit, show the successful result.

Bad examples:

- Full app launch from splash unless launch behavior is the feature.
- Long login/auth setup if the feature is elsewhere.
- Repeating the same tap sequence multiple times.

## 2. Record a broader raw clip

Recommended path for Flutter mobile work:

1. Prepare the simulator/app state.
2. Start the recording.
3. Run the scripted UI flow.
4. Stop the recording.

If using the iOS simulator MCP:

- start: `mcp__ios_simulator__record_video`
- stop: `mcp__ios_simulator__stop_recording`

If scripted flow is needed, prefer an integration test that does only the navigation and taps needed for the demo.

## 3. Trim and render final assets

Use the helper:

```bash
scripts/make_demo_assets.sh \
  /absolute/path/raw.mov \
  /absolute/path/output/demo \
  99 \
  110
```

Outputs:

- `/absolute/path/output/demo.mp4`
- `/absolute/path/output/demo.gif`

The helper:

- trims the clip to `start..end`
- writes a web-friendly MP4
- creates a small GIF preview
- removes its temporary palette file

Tips:

- Trim from the frame where the feature is already visible.
- Leave 1-2 seconds on the final state.
- Prefer 6 fps GIF output unless motion is too hard to follow.

## 4. Publish to GitHub and update the PR

Use the publishing helper:

```bash
python3 scripts/publish_pr_demo.py \
  --repo amia-life/amia_flutter_app \
  --pr 307 \
  --gif /absolute/path/output/demo.gif \
  --mp4 /absolute/path/output/demo.mp4 \
  --title "Language settings demo"
```

Behavior:

- creates or updates release tag `pr-307-demo-assets`
- uploads the GIF and MP4 with `--clobber`
- rewrites the PR body so `## Demo` contains the embedded GIF and MP4 link

## 5. Cleanup checklist

Remove local artifacts that are no longer needed:

- temporary integration test files created only for recording
- raw recordings once the final assets are published
- temporary screenshots used for locating trim boundaries
- temporary palette PNGs
- temporary PR body files in `/tmp`

Do not leave repo-only recording helpers on the branch unless they are intentional product tests.
