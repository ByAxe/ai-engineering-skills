# Infrastructure Services

Gas Town runs several long-lived services that must be operational before dispatching work.

## Service Overview

| Service | Role | Managed By |
|---|---|---|
| **Dolt** | SQL database for beads (work items) | `gt dolt start/stop/restart` |
| **Daemon** | Go background process, heartbeats, event routing | `gt daemon start/stop` |
| **Mayor** | Global work coordinator (Claude/Codex session) | `gt up` |
| **Deacon** | Town-level watchdog monitoring Mayor and Witnesses | `gt up` |
| **Witness** | Per-rig polecat health monitor | `gt up` |
| **Refinery** | Per-rig merge queue processor | `gt up` |

## Starting Everything

```bash
cd ~/gt && gt up          # starts all services idempotently
cd ~/gt && gt up --restore  # also restarts crew and pinned polecats
```

## Verify the Real HQ First

When a rig is adopted or symlinked into `~/gt`, the repo path can accumulate a stale shadow town. Before restarting services or launching work, compare both views:

```bash
gt status
cd ~/gt && gt status
cd ~/gt && gt polecat list --all
cd ~/gt && gt dolt status
```

If the repo path and `~/gt` disagree, use the root that has the live tmux sessions and the real Dolt data directory as the control plane. Do not start, stop, or repair Dolt from the shadow town.

## Dolt Server Setup

Dolt provides the SQL database backing all beads (work items).

### First-Time Setup

```bash
# Configure identity (one-time)
dolt config --global --add user.email "you@example.com"
dolt config --global --add user.name "yourname"

# Initialize databases
cd ~/gt && gt dolt init-rig hq
cd ~/gt && gt dolt init-rig <rig_name>

# Start server
cd ~/gt && gt dolt start
```

### Common Dolt Issues

**"Author identity unknown"**
Dolt needs user identity before creating databases.
Fix: Run `dolt config --global --add user.email/name`.

**"no databases found"**
Databases not initialized.
Fix: Run `gt dolt init-rig` for each rig plus `hq`.

**CSV parse errors in gt doctor**
Multiline text in Dolt fields breaks CSV output parsing. Produces false warnings about stuck patrols.
Fix: Clean up multiline descriptions:
```bash
cd ~/gt/.dolt-data/<rig> && dolt sql -q \
  "UPDATE issues SET description = 'Single line.' WHERE id = '<bead-id>';"
cd ~/gt && gt dolt restart
```

**Stale prefix in HQ config table**
After removing a rig, the HQ database may retain the old prefix.
Fix:
```bash
cd ~/gt/.dolt-data/hq && dolt sql -q \
  "UPDATE config SET value = 'hq' WHERE \`key\` = 'issue_prefix';"
```

## Shell Integration

GT needs `GT_TOWN_ROOT` and `GT_RIG` env vars to find the workspace from any directory.

```bash
gt shell install          # adds cd hook to ~/.zshrc
source ~/.zshrc           # activate in current session
gt shell status           # verify installation
```

Without this, commands from outside `~/gt` fail with "not in a Gas Town workspace".

## Health Checks

```bash
cd ~/gt && gt doctor          # full diagnostic (87 checks)
cd ~/gt && gt doctor --fix    # auto-fix (ONLY when no polecats running)
cd ~/gt && gt doctor -v       # verbose output for debugging
cd ~/gt && gt status          # quick overview of services and agents
cd ~/gt && gt vitals          # unified health dashboard
cd ~/gt && gt dolt status     # Dolt server health
```

## Stopping Services

```bash
cd ~/gt && gt down            # stop all services
cd ~/gt && gt dolt stop       # stop Dolt only
cd ~/gt && gt shutdown        # full shutdown with cleanup
```

## After Reboot

All services need restarting after a system reboot:

```bash
cd ~/gt && gt dolt start      # start Dolt first (other services depend on it)
cd ~/gt && gt up              # start all remaining services
```

Or configure auto-start:

```bash
cd ~/gt && gt install --supervisor --force    # configure launchd/systemd
```
