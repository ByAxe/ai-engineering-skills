# Gas Town Concepts Glossary

## Workspace Hierarchy

### HQ (Town)
Top-level workspace directory (typically `~/gt/`). Contains all rigs, services, configuration, and the Mayor. Created with `gt install`.

### Rig
Project container wrapping a git repository. Each rig has its own polecats, witness, refinery, crew, and beads database. Created with `gt init` + `gt rig add`.

## Agents

### Mayor
Global coordinator running from the HQ root. Handles cross-rig work distribution, escalations, and strategic decisions. One per town.

### Deacon
Town-level watchdog monitoring Mayor and Witnesses. Ensures the supervision chain stays healthy.

### Witness
Per-rig patrol agent overseeing polecats and the refinery. Detects stuck agents, triggers recovery (nudge or handoff), manages session cleanup.

### Refinery
Per-rig merge queue processor. Validates polecat work through quality gates and merges to main. Implements Bors-style bisecting merge queue.

### Polecat
Ephemeral worker agent with persistent identity. Spawned on demand for specific tasks, cleaned up after merge. Each gets its own git worktree.

### Boot
Deacon watchdog. Monitors the Deacon itself to keep the supervision chain healthy. Managed by `gt boot`.

### Daemon
Go background process providing heartbeats (every 3 min), event routing, and service coordination.

### Dog
Reusable cross-rig infrastructure worker. Unlike polecats (ephemeral, single-rig), dogs are persistent, have worktrees into every rig, and return to idle state after completing work. Kennel at `~/gt/deacon/dogs/`. Managed by `gt dog`.

### Crew Member
Persistent human workspace within a rig. A full git clone (not a worktree) where you work directly. Named with recognizable names (dave, emma, fred). Created with `gt crew add`.

## Work Tracking

### Bead
Work item tracked in Dolt (SQL database). Has an ID, status, dependencies, labels, and assignee. Created by formulas or manually with `bd create`. Types include: task, epic, bug, agent.

### Wisp
Ephemeral bead for transient work — patrol state, agent metadata, convoy tracking. Automatically cleaned up.

### Hook
Durability primitive. Work attached to a polecat's hook survives session restarts. The hook ensures work continuity even when Codex/Claude sessions crash and respawn.

### Molecule (Mol)
DAG of workflow steps attached to a bead. Created from a formula. Steps auto-continue on completion. Tracked with `bd mol current` and `bd mol step done`.

## Workflow Definitions

### Formula
Reusable TOML workflow template. Defines steps, dependencies, variables, and acceptance criteria. Four types:

- **workflow** — Sequential steps, single orchestrating agent (e.g., `shiny`, `mol-polecat-work`)
- **convoy** — Parallel execution with multiple polecats per leg (e.g., `code-review`, `design`)
- **expansion** — Replaces a single step with multiple sub-steps (e.g., `rule-of-five`, `tdd-cycle`)
- **aspect** — Cross-cutting pre/post behavior applied to steps (e.g., `security-audit`)

### Convoy
Persistent tracking unit for batched work. Analyzes dependency graphs and computes execution waves for parallel dispatch. Auto-closes when all tracked issues complete.

### Wave
Execution group within a convoy. Tasks in the same wave have no mutual dependencies and run in parallel. Waves execute sequentially — Wave 2 starts only when all Wave 1 tasks complete.

### Mountain
Enhanced convoy with active monitoring for large epics. Adds stall detection, skip-after-N-failures, and progress audit tracking. Activated with `gt mountain <epic-id>`.

## Communication

### Nudge
Asynchronous message sent to any Gas Town worker. Does not survive session restarts. Used for real-time coordination.

### Mail
Persistent message stored in Dolt. Survives session death and restart. Used for handoffs and durable communication.

### Escalation
Priority notification sent to the Mayor for critical issues. Severity levels: LOW, MEDIUM, HIGH, CRITICAL.

### Handoff
Session transfer from one polecat instance to a fresh one. Work context is preserved on the hook. The new session picks up where the old one left off.

## Quality System

### Gate Commands
Per-rig configured commands that polecats run to validate their work:
- `setup_command` — dependency installation
- `test_command` — test suite
- `typecheck_command` — type checking
- `lint_command` — linting
- `build_command` — build verification

### Pre-Verify
Step where polecat rebases onto the target branch and runs the full gate suite. Enables fast-path merge by the Refinery (~5 seconds instead of re-running gates).

### Stamps
Portable reputation attestation earned on work completion. Multi-dimensional: quality, reliability, creativity, confidence levels.

## Service Lifecycle

### gt down
Reversible pause — stops all services but keeps worktrees and polecat branches intact. Resume with `gt up`.

### gt shutdown
Permanent cleanup — stops services AND removes polecat worktrees/branches. Polecats with uncommitted work are skipped (protected). Use `--nuclear` to force cleanup (dangerous).

### gt estop (Emergency Stop)
Freezes all agent sessions with SIGTSTP. Mayor and overseers are exempt. Resume with `gt thaw`.

### Scheduler
Capacity-controlled dispatch system. When `scheduler.max_polecats` is set (e.g., 5), excess work is deferred and dispatched as slots become available. Default (-1) means direct dispatch with no limit.

## Federation

### Wasteland
DoltHub-based federation for sharing work across Gas Towns. Join communities (`gt wl join`), post work, claim tasks, earn reputation through stamps. Each participant maintains a sovereign rig fork of the shared commons database.

## Diagnostics

### Feed
Real-time TUI dashboard showing agent tree, convoy panel, and event stream. Use `gt feed -p` (problems view) to surface stuck agents via GUPP violations (hooked work + 30 minutes no progress).

### Seance
Spawns a Claude subprocess resuming a predecessor session with full context. Useful for interrogating what happened in a crashed or completed session. `gt seance --talk <session-id>`.

### Audit
Query provenance data across git commits, beads, and events. Shows unified timeline for an actor. `gt audit --actor <address> --since 1h`.

### Costs
Session cost tracking. Shows token usage and model-specific pricing. `gt costs --today --by-role --by-rig`.

### Warrant
Controlled termination for stuck/unresponsive agents. Boot picks up warrants during triage cycles. `gt warrant file <agent>`.

### KRC (Key Record Chronicle)
Manages TTL-based lifecycle for Level 0 ephemeral data (patrol heartbeats, status checks). Auto-prunes expired records.
