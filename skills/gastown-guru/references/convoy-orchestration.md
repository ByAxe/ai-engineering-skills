# Convoy Orchestration

Convoys are Gas Town's primary mechanism for orchestrating batched, dependency-aware work across multiple polecats.

## Core Concepts

- A **convoy** is a persistent tracking unit with an ID (hq-* prefix)
- It tracks issues across rigs and can span multiple rig boundaries
- A **swarm** is the ephemeral set of workers currently assigned to a convoy's issues
- Convoys auto-close when all tracked issues complete, notifying subscribers

## Lifecycle

```
Created → Staged → Open (Wave 1 dispatched) → ... → Landed (all complete)
```

### Stage
Analyzes dependencies and computes execution waves:
```bash
# From an epic bead (walks all children)
gt convoy stage <epic-id>

# From specific tasks
gt convoy stage <task-1> <task-2> <task-3>

# Re-analyze existing convoy
gt convoy stage <convoy-id>
```

### Launch
Transitions from staged to open, dispatches Wave 1:
```bash
# Launch a staged convoy
gt convoy launch <convoy-id>

# Stage + launch in one step
gt convoy stage <epic-id> --launch
```

### Monitor
```bash
gt convoy status <convoy-id>    # progress, tracked issues, active workers
gt convoy list                  # dashboard view of all convoys
gt convoy stranded              # find stuck convoys needing attention
```

### Complete
```bash
gt convoy close <convoy-id>     # close (verifies all items done)
gt convoy land <convoy-id>      # land: cleanup worktrees + close
```

## Wave Execution

Convoys compute waves from the dependency DAG:

- **Wave 1**: All tasks with no dependencies (run in parallel)
- **Wave 2**: Tasks whose dependencies are all in Wave 1 (dispatched when Wave 1 completes)
- **Wave N**: Tasks whose dependencies are all in prior waves

Each task in a wave gets its own polecat. Tasks within a wave run in parallel. Waves execute sequentially.

### Throttling
Use `--max-concurrent` on batch sling to limit parallel polecat spawns:
```bash
gt sling <bead-1> <bead-2> <bead-3> my_project --max-concurrent 3
```

### Scheduler (Capacity Control)
For persistent capacity limits, use the dispatch scheduler:
```bash
gt config set scheduler.max_polecats 5   # enable deferred dispatch (limit to 5)
gt scheduler status                       # show queue state
gt scheduler pause                        # pause dispatch
gt scheduler resume                       # resume dispatch
gt scheduler clear                        # clear queue
```
When `max_polecats` is set, excess work is queued and dispatched as slots free up. Default (-1) means direct dispatch with no limit.

## Auto-Convoy

When you sling a single bead, GT auto-creates a convoy for dashboard visibility. Disable with `--no-convoy`.

## Synthesis

After all convoy legs complete, run synthesis:
```bash
gt synthesis status <convoy-id>   # check if ready
gt synthesis start <convoy-id>    # run synthesis step
gt synthesis close <convoy-id>    # close synthesis
```

## Mountain-Eater (Autonomous Grinding)

For large epics, **always use Mountain-Eater** for autonomous multi-wave grinding:

```bash
gt mountain <epic-id> --force     # stage + label + launch (--force skips tracking warnings)
gt mountain status <convoy-id>    # progress
gt mountain pause <convoy-id>     # stop dispatching
gt mountain resume <convoy-id>    # resume
gt mountain cancel <convoy-id>    # remove mountain label, keep convoy
```

Mountain activates three autonomous systems:
- **ConvoyManager** — auto-dispatches next waves when current ones complete
- **Deacon** — audits progress every ~10 minutes, detects stalls
- **Witness** — monitors polecat health, handles recovery (nudge or handoff)
- **Skip-after-N-failures** — prevents infinite retry loops on broken beads

### Mountain vs Manual Convoy

| Feature | `gt convoy stage --launch` | `gt mountain` |
|---|---|---|
| Wave 1 dispatch | Yes | Yes |
| Auto-dispatch next waves | Only if tracking connects | Yes, via ConvoyManager |
| Stall detection | No | Yes, via Deacon (~10 min) |
| Failure handling | Manual | Skip-after-N-failures |
| Health monitoring | Basic Witness | Enhanced Witness audit |

**Recommendation:** Always use Mountain for multi-wave epics. Use plain convoys only for single-wave batch dispatch.

### Cross-Prefix Tracking Warnings

Mountain launch may show "Warning: could not track tt-xxx in convoy" for every bead. This happens when the HQ beads database (`hq-*` prefix) can't resolve rig-prefixed beads (`tt-*`). The mountain still works — the ConvoyManager dispatches based on the bead dependency graph in the rig database, not the tracking relations.

If Mountain can't sling beads that are already assigned, it reports "bead is already being slung" — this is expected and harmless.

## Convoy + Formula Integration

Polecats run the rig's `default_formula`. Set it before launching:

```bash
gt rig config set my_project default_formula shiny-enterprise --global
gt rig config show my_project    # verify
```
