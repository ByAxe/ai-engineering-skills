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

For large epics, activate Mountain for enhanced monitoring:
```bash
gt mountain <epic-id>             # stage + label + launch
gt mountain status <epic-id>      # progress
gt mountain pause/resume <epic-id>
gt mountain cancel <epic-id>
```

Mountain adds:
- Enhanced stall detection
- Skip-after-N-failures
- Active progress monitoring
- Witness audit tracking

## Convoy + Formula Integration

Polecats in a convoy run the formula specified at launch time or the rig's `default_formula`:

```bash
# All polecats use shiny-enterprise
gt convoy stage <epic-id> --launch --formula shiny-enterprise
```

Or set the rig default:
```bash
gt config set rigs.my_project.default_formula shiny-enterprise
```
