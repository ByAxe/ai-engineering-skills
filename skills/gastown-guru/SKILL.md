---
name: gastown-guru
description: Expert guide for Gas Town (gt) multi-agent orchestration — setup, rig management, formula workflows, convoy orchestration, quality pipelines, and troubleshooting. Use when working with Gas Town, setting up rigs, dispatching work to polecats, configuring quality workflows, or debugging GT infrastructure issues.
license: MIT
metadata:
  author: ByAxe
  version: 1.0.0
  category: software-development
  environment: Gas Town (gt) installed via Homebrew with a configured HQ workspace. Requires tmux, Dolt, and optionally one or more AI agent CLIs (Claude Code, Codex, Gemini).
  tags:
    - gastown
    - multi-agent
    - orchestration
    - polecats
    - formulas
    - convoys
    - code-quality
    - merge-queue
---

# Gas Town Guru

Expert guide for Gas Town (gt) — the multi-agent workspace manager that coordinates AI coding agents working on shared codebases.

This skill covers the full lifecycle: workspace setup, rig initialization, spec-to-code pipelines, formula-driven quality workflows, convoy orchestration, and operational troubleshooting.

## Important

- **Never modify GT config files while polecats are running.** Changing `.beads/redirect`, `routes.jsonl`, Dolt databases, or `rigs.json` while agents are active kills their sessions and loses all progress. Always check `gt polecat list --all` first.
- GT requires expert supervision. Code is cheap but green CI is priceless. Configure rig test commands before launching convoys.
- Prefer `shiny-enterprise` over raw `mol-polecat-work` for production-quality code. The Rule of Five refinement catches issues that single-pass implementation misses.
- Always run `gt doctor --fix` after infrastructure changes, but only when no polecats are working.
- Gas Town uses eventual consistency — some bugs get fixed 2-3 times. The system self-corrects through iterative molecular acceptance criteria.

## Workflow

### Step 1: Verify or Create the GT Workspace

Check if a Gas Town HQ exists:

```bash
ls ~/gt/mayor/town.json
```

If no HQ exists, create one:

```bash
gt install ~/gt --git --shell
```

If HQ exists, verify health:

```bash
cd ~/gt && gt doctor
```

Fix any issues (only when no polecats are running):

```bash
gt polecat list --all          # verify no active workers
cd ~/gt && gt doctor --fix
```

### Step 2: Initialize a Rig

A rig wraps a git repository for GT agent management. Prerequisites:

1. The directory must be a git repository with at least one commit
2. The rig directory must be accessible from the HQ (symlink if needed)
3. Rig names must use underscores, not hyphens

```bash
# Initialize git if needed
cd /path/to/project
git init && git commit --allow-empty -m "Initial commit"

# Initialize GT rig structure
gt init

# Symlink into HQ if the project lives outside ~/gt/
ln -s /path/to/project ~/gt/my_project

# Register the rig
cd ~/gt && gt rig add my_project --adopt --force

# Set git URL (required for crew workspaces)
# Edit ~/gt/mayor/rigs.json to add the git URL

# Add a crew member
cd ~/gt && gt crew add your_name --rig my_project
```

### Step 3: Configure Infrastructure Services

```bash
# Configure Dolt identity (one-time)
dolt config --global --add user.email "you@example.com"
dolt config --global --add user.name "yourname"

# Initialize Dolt databases
cd ~/gt && gt dolt init-rig hq
cd ~/gt && gt dolt init-rig my_project

# Start Dolt server
cd ~/gt && gt dolt start

# Install shell integration
gt shell install
source ~/.zshrc

# Bring up all services
cd ~/gt && gt up
```

### Step 4: Spec-to-Plan Pipeline

Pass a specification to the `mol-idea-to-plan` formula. This runs an 8-step pipeline with parallel PRD review (6 agents), parallel design (6 agents), alignment rounds, and plan review — producing beads with dependencies.

```bash
cd ~/gt && gt sling mol-idea-to-plan my_project --create \
  --var problem="<your specification text>" \
  --var context="<tech stack, constraints, existing artifacts>"
```

If you have an existing PRD from a prior run, reference it in context:

```bash
--var context="A previous run produced a reviewed PRD at .prd-reviews/project/prd-draft.md. USE IT AS STARTING POINT — skip Steps 1-3 and proceed from Step 4 (design generation)."
```

Monitor progress:

```bash
gt polecat list --all                           # list active workers
gt polecat status my_project/furiosa            # specific polecat
tmux -L gt-$(cat ~/gt/mayor/town.json | grep -o '"[^"]*"' | head -1 | tr -d '"') attach -t <session>
gt trail                                        # recent activity
```

### Step 5: Configure Rig Quality Gates

Before launching a coding convoy, configure test commands for the rig. Check the references for detailed rig settings configuration.

Each rig needs these commands configured so polecats can run quality gates:

- `setup_command` — dependency installation
- `test_command` — test suite
- `typecheck_command` — type checking
- `lint_command` — linting
- `build_command` — build verification

### Step 6: Launch the Coding Convoy

Once the plan creates beads with an epic, launch the convoy:

```bash
# Stage and launch (analyzes dependencies, computes parallel waves, dispatches)
cd ~/gt && gt convoy stage <epic-bead-id> --launch
```

The convoy:
1. Walks all child beads and their dependency graph
2. Computes execution waves (parallel groups)
3. Dispatches Wave 1 to auto-spawned polecats
4. Auto-dispatches subsequent waves as dependencies complete
5. Each polecat runs the configured work formula

Monitor:

```bash
gt convoy status <convoy-id>
gt convoy list
gt ready
gt agents
```

### Step 7: Choose the Right Quality Formula

Select based on risk and quality requirements. Apply via `--formula` on convoy launch or per-sling.

| Formula | Use When | Pipeline |
|---|---|---|
| `mol-polecat-work` | Standard tasks, bug fixes | implement -> gates -> merge |
| `shiny` | Feature work | design -> implement -> review -> test -> submit |
| `shiny-enterprise` | Critical features, production code | design -> implement(5-pass Rule of Five) -> review -> test -> submit |
| `shiny-secure` | Auth, payments, PII | shiny + pre/post security audits |
| `mol-polecat-work-monorepo-tdd` | Test-critical code | red-green-refactor with hard gates |

For code review after merge:

```bash
gt formula run code-review --preset full
```

This spawns 10 parallel reviewers: correctness, performance, security, elegance, resilience, style, wiring, commit-discipline, test-quality, smells.

### Step 8: Select the Default Agent

GT supports multiple AI agent backends:

```bash
gt config default-agent list     # see available agents
gt config default-agent claude   # set default
gt config default-agent codex    # or use Codex (GPT)
```

Override per-sling:

```bash
gt sling <bead> my_project --agent claude
```

## Troubleshooting

### Common Setup Issues

| Problem | Cause | Fix |
|---|---|---|
| `not in a Gas Town workspace` | Missing `GT_TOWN_ROOT` env var | Run commands from `~/gt` or run `gt shell install` |
| `gt init` fails with "not a git repository" | No git repo or no commits | `git init && git commit --allow-empty -m "Initial commit"` |
| Rig name rejected | Hyphens in name | Use underscores: `my_project` not `my-project` |
| `gt rig add --adopt` can't find directory | Running from wrong location | Run from `~/gt`, ensure symlink exists |
| Crew add fails "no git URL" | Empty `git_url` in rigs.json | Set the git URL in `~/gt/mayor/rigs.json` |
| Dolt "Author identity unknown" | Missing dolt config | `dolt config --global --add user.email/name` |
| "redirect chains not allowed" | Stale `.beads/redirect` file | Delete the redirect file (when no agents running) |
| CSV parse errors in doctor | Multiline text in Dolt fields | Clean up multiline descriptions in Dolt tables |
| Agent beads missing | Beads not in Dolt server | Run `gt doctor --fix` (when no agents running) |
| Polecat session not found | Services not started | Run `cd ~/gt && gt up` |
| Sling "getting pane" error | No tmux session for target | Add `--create` flag to spawn new polecat |

### Operational Commands

```bash
# Health
gt doctor                    # full health check
gt doctor --fix              # auto-fix (NO running polecats!)
gt status                    # town overview
gt vitals                    # unified health dashboard

# Services
gt up                        # start all services
gt down                      # stop all services
gt dolt start/stop/restart   # Dolt server management

# Monitoring
gt polecat list --all        # all polecats across rigs
gt polecat status <rig>/<name>
gt agents                    # active agent sessions
gt trail                     # recent activity
gt peek <rig>/<polecat>      # view agent output
gt convoy status <id>        # convoy progress

# Communication
gt nudge <agent> "message"   # async message to agent
gt mail send <agent>         # persistent message
gt escalate -s HIGH "issue"  # escalate to Mayor

# Work management
gt sling <bead> <target>     # dispatch work
gt unsling <target> --force  # remove work from agent
gt hook show <target>        # see what's on an agent's hook
gt ready                     # show unblocked work
gt done                      # signal work complete
```

## Key Concepts

- **HQ (Town)**: Top-level workspace directory (`~/gt/`). Contains all rigs, services, and configuration.
- **Rig**: Project container wrapping a git repository. Each rig has its own polecats, witness, refinery, and crew.
- **Polecat**: Ephemeral worker agent with persistent identity. Spawned on demand, cleaned up after merge.
- **Bead**: Work item tracked in Dolt. Has status, dependencies, labels. Created by formulas or manually.
- **Wisp**: Ephemeral bead for transient work (patrol state, agent metadata).
- **Hook**: Durability primitive. Work on a hook survives session restarts.
- **Molecule (Mol)**: DAG of steps attached to a bead. Steps auto-continue.
- **Formula**: Reusable TOML workflow template. Types: workflow, convoy, expansion, aspect.
- **Convoy**: Persistent tracking unit for batched work. Computes dependency waves for parallel dispatch.
- **Witness**: Per-rig health monitor for polecats. Detects stuck agents, triggers recovery.
- **Refinery**: Per-rig merge queue processor. Validates and merges polecat work.
- **Mayor**: Global coordinator for cross-rig work.
- **Deacon**: Town-level watchdog overseeing Mayor and Witnesses.
- **Daemon**: Go background process providing heartbeats and event routing.
