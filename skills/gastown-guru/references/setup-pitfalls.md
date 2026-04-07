# Gas Town Setup Pitfalls and Fixes

Hard-won lessons from real setup sessions. Each issue was encountered and resolved in practice.

## Rig Initialization

### gt init requires a git repo with commits
`gt init` checks for a valid git repository. An empty directory fails. A git-initialized directory with no commits also fails.

**Fix:**
```bash
git init
git commit --allow-empty -m "Initial commit"
gt init
```

### Rig names cannot contain hyphens
GT rejects names with hyphens, dots, spaces, or path separators.

**Fix:** Use underscores: `time_tracker` not `time-tracker`.

### Rigs must be accessible from HQ
`gt rig add` expects the rig directory to exist under the HQ path (`~/gt/`). If your project lives elsewhere, symlink it.

**Fix:**
```bash
ln -s /path/to/your/project ~/gt/project_name
cd ~/gt && gt rig add project_name --adopt --force
```

### git_url must be set for crew workspaces
Crew creation clones the repo. If `git_url` is empty in `rigs.json`, crew add fails.

**Fix:** Edit `~/gt/mayor/rigs.json` and set the `git_url` field to the repo path or remote URL.

## Dolt Server

### Dolt requires identity configuration
First-time Dolt database initialization fails without author identity.

**Fix:**
```bash
dolt config --global --add user.email "you@example.com"
dolt config --global --add user.name "yourname"
```

### Dolt databases must be initialized per-rig
The Dolt server needs a database for each rig plus one for `hq`.

**Fix:**
```bash
cd ~/gt && gt dolt init-rig hq
cd ~/gt && gt dolt init-rig my_project
cd ~/gt && gt dolt start
```

### Multiline text in Dolt fields breaks CSV parsing
GT doctor queries Dolt via CSV output. Descriptions with newlines cause "wrong number of fields" parse errors, producing false warnings about stuck patrols.

**Fix:** Clean up multiline descriptions:
```bash
cd ~/gt/.dolt-data/my_project && dolt sql -q \
  "UPDATE issues SET description = 'Single line description.' WHERE id = 'my-bead-id';"
```

Then restart Dolt: `cd ~/gt && gt dolt restart`

## Beads and Routing

### Redirect chains
If a rig's `.beads/redirect` points to the HQ `.beads/`, which then routes to Dolt, GT warns about redirect chains. This can also crash running polecats.

**Fix:** Remove the rig-level redirect file (only when no polecats are running):
```bash
rm /path/to/project/.beads/redirect
```

### Stale routes.jsonl in rig .beads
A `routes.jsonl` file inside a rig's `.beads/` directory breaks cross-rig routing.

**Fix:** `gt doctor --fix` deletes it automatically. Or remove manually when no agents are running.

### .beads directory permissions
GT warns when `.beads` has 0755 permissions.

**Fix:**
```bash
chmod 700 /path/to/project/.beads
```

## Shell Integration

### GT_TOWN_ROOT not set
Commands run from outside `~/gt` fail with "not in a Gas Town workspace".

**Fix:**
```bash
gt shell install
source ~/.zshrc
```

Or prefix commands with `cd ~/gt &&`.

## Services

### Sling fails with "getting pane" error
GT needs tmux sessions running for agent dispatch.

**Fix:**
```bash
cd ~/gt && gt up          # start all services
```

### Sling needs --create for new polecats
When no idle polecat exists, sling fails unless `--create` is specified.

**Fix:** Add `--create` to the sling command.

## Critical Safety Rule

### NEVER modify GT config while agents are running

This includes:
- `.beads/redirect` or `.beads/routes.jsonl`
- `.beads/config.yaml`
- `~/gt/mayor/rigs.json`
- Dolt databases (direct SQL modifications)
- Any file under `.beads/`

**Why:** Modifying these files while a polecat is running can break its beads access, kill the session, clean up the wisp, clear the hook, and lose all progress. The agent must be re-slung from scratch.

**How to check:**
```bash
gt polecat list --all     # must show no active workers
```

Only then is it safe to run `gt doctor --fix` or modify infrastructure files.

## Non-Claude Agent (Codex/Gemini) Sits at Blank Prompt

### Symptom
After `gt sling`, the polecat shows "working" but the agent (Codex/Gemini) sits at its prompt doing nothing. No work context loaded.

### Cause
Non-Claude agents don't support GT's SessionStart hooks. Without hooks, `gt prime --hook` is never called, so the agent has no idea what work is assigned.

### Fix
Install wrapper scripts and configure GT to use them:

```bash
# Install wrappers
cd ~/gt && gt install --wrappers --force

# Point the agent to the wrapper (critical step!)
gt config agent set codex "$HOME/bin/gt-codex"

# Verify
gt config agent get codex
# Should show: Type: custom, Command: /Users/.../bin/gt-codex
```

The wrapper calls `gt prime` before launching the agent, injecting Gas Town context.

### Common Mistake
Setting `gt config default-agent codex` without installing and configuring the wrapper. GT will launch bare `codex` which starts with zero context.

## Convoy Launch Tracking Warnings

### Symptom
`gt convoy stage --launch` shows "Warning: could not track tt-xxx in convoy" for every bead. Convoy creates but tracking doesn't connect.

### Cause
Cross-prefix routing issue. The HQ beads database (prefix `hq-`) can't resolve `tt-` prefixed beads from the rig database. Often caused by stale prefix config from a removed rig.

### Fix
Check and fix the HQ database prefix:
```bash
cd ~/gt/.dolt-data/hq && dolt sql -q "SELECT * FROM config WHERE \`key\` = 'issue_prefix';"
# If it shows a wrong prefix (e.g., 'dwa' from a deleted rig):
dolt sql -q "UPDATE config SET value = 'hq' WHERE \`key\` = 'issue_prefix';"
```

If convoy auto-dispatch doesn't work, sling Wave 1 manually:
```bash
cd ~/gt && gt sling <wave-1-bead> <rig> --create
```

## Convoy Auto-Dispatch and Mountain-Eater

### Waves don't auto-dispatch after polecat completes

**Symptom:** A polecat finishes its bead, calls `gt done`, goes idle, but no new work is dispatched. The next wave's beads show as ready in `gt ready` but no polecat picks them up.

**Cause:** The convoy tracking didn't connect (cross-prefix routing issue) so the ConvoyManager doesn't know when to dispatch next waves. The Witness may also have stale state about which beads are hooked.

**Fix — use Mountain-Eater for autonomous grinding:**
```bash
cd ~/gt && gt mountain <epic-id> --force
```

Mountain activates:
- **ConvoyManager** auto-feeds subsequent waves when current ones complete
- **Deacon** audits progress every ~10 minutes, detects stalls
- **Witness** monitors polecat health and handles recovery
- Skip-after-N-failures prevents infinite loops on broken beads

If Mountain launch fails to sling beads that are already assigned ("bead is already being slung"), that's expected — it means polecats are already working on them.

**Monitor the mountain:**
```bash
gt mountain status <convoy-id>
gt polecat list --all
```

### Manual wave dispatch as fallback

If Mountain-Eater can't connect tracking due to cross-prefix routing, dispatch waves manually:

```bash
# Check what's ready
gt ready

# Sling ready beads to the rig (each gets its own polecat)
cd ~/gt && gt sling <bead-1> <rig> --create
cd ~/gt && gt sling <bead-2> <rig> --create
```

### Rig config commands must use `gt rig config set`

**Symptom:** Gate commands (test, lint, build) not picked up by polecats. Manual edits to `settings/config.json` are ignored.

**Cause:** GT reads gate commands from the bead layer, not from the settings JSON file.

**Fix — use the proper command:**
```bash
gt rig config set <rig> default_formula shiny-enterprise --global
gt rig config set <rig> setup_command "pnpm install" --global
gt rig config set <rig> test_command "pnpm -r run test" --global
gt rig config set <rig> typecheck_command "pnpm -r run typecheck" --global
gt rig config set <rig> lint_command "pnpm -r run lint" --global
gt rig config set <rig> build_command "pnpm -r run build" --global

# Verify
gt rig config show <rig>
```

### Removing a rig leaves stale data

**Symptom:** After `gt rig remove`, doctor finds broken worktrees, orphan databases, stale agent beads, and the HQ database retains the old rig's prefix.

**Fix — clean up in order:**
1. `gt rig remove <name>` — unregister from rigs.json
2. `rm -rf ~/gt/<name>` — delete rig files
3. Remove broken worktrees in `~/gt/deacon/dogs/*/` if they reference the deleted rig
4. `cd ~/gt && gt doctor --fix` — clean orphan databases, stale beads, broken sessions
5. Fix HQ prefix if needed:
   ```bash
   cd ~/gt/.dolt-data/hq && dolt sql -q \
     "UPDATE config SET value = 'hq' WHERE \`key\` = 'issue_prefix';"
   ```
