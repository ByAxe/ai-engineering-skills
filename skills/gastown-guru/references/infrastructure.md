# Infrastructure Services

Gas Town runs several long-lived services that must be operational before dispatching work.

## Service Overview

| Service | Role | Managed By |
|---|---|---|
| **Dolt** | SQL database for beads (work items) | `gt dolt start/stop/restart` |
| **Daemon** | Go background process, heartbeats, event routing | `gt daemon start/stop` |
| **Mayor** | Global work coordinator (Claude/Codex session) | `gt up` |
| **Deacon** | Town-level watchdog monitoring Mayor and Witnesses | `gt up` |
| **Boot** | Deacon watchdog (monitors the Deacon itself) | `gt up` |
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

Three stop modes with increasing permanence:

| Command | Effect | Reversible? |
|---|---|---|
| `gt down` | Pause all services, keep worktrees | Yes (`gt up`) |
| `gt down --all` | Pause + orphan cleanup + verification | Yes (`gt up`) |
| `gt shutdown --force` | Stop + remove worktrees + delete branches | No (polecats lost) |
| `gt estop` | SIGTSTP freeze all agents (Mayor exempt) | Yes (`gt thaw`) |

```bash
cd ~/gt && gt down                                # reversible pause
cd ~/gt && gt down --polecats                     # also stop polecat sessions
cd ~/gt && gt down --nuke                         # also kill shared tmux server
cd ~/gt && gt down --dry-run                      # preview what would stop
cd ~/gt && gt shutdown --force                    # permanent: stop + cleanup worktrees
cd ~/gt && gt shutdown --all --force              # also stop crew sessions
cd ~/gt && gt shutdown --graceful                 # let agents save state first
cd ~/gt && gt shutdown --polecats-only            # only stop polecats
cd ~/gt && gt estop --reason "investigating bug"  # emergency freeze
cd ~/gt && gt estop --rig my_project              # freeze single rig
cd ~/gt && gt thaw                                # resume after estop
cd ~/gt && gt thaw --rig my_project               # thaw single rig
cd ~/gt && gt dolt stop                           # stop Dolt only
```

**Warning:** `gt shutdown --nuclear` forces cleanup even with uncommitted polecat work. Only use if you're sure nothing valuable is in-flight.

## Monitoring and Diagnostics

```bash
cd ~/gt && gt feed                  # real-time TUI (j/k scroll, tab panels, q quit)
cd ~/gt && gt feed --plain          # plain event stream
cd ~/gt && gt feed -p               # problems view (stuck agents via GUPP)
cd ~/gt && gt dashboard --open      # web dashboard (convoy tracking, auto-refresh)
cd ~/gt && gt vitals                # unified health dashboard
cd ~/gt && gt health                # data plane: Dolt, DBs, backups, zombies
cd ~/gt && gt health --json         # machine-readable health
cd ~/gt && gt costs --today         # today's session costs
cd ~/gt && gt costs --by-role       # costs by agent role
cd ~/gt && gt audit --actor <addr>  # provenance timeline for an agent
cd ~/gt && gt seance --recent       # list recent sessions
cd ~/gt && gt seance --talk <id>    # interrogate a predecessor session
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
