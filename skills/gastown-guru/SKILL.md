---
name: gastown-guru
description: Expert guide for Gas Town (gt) multi-agent orchestration — setup, rig management, formula workflows, convoy orchestration, quality pipelines, and troubleshooting. Use when working with Gas Town, setting up rigs, dispatching work to polecats, configuring quality workflows, or debugging GT infrastructure issues.
license: MIT
metadata:
  author: ByAxe
  version: 1.1.0
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

## Important

- **Never modify GT config files while polecats are running.** Changing `.beads/redirect`, `routes.jsonl`, Dolt databases, or `rigs.json` while agents are active kills their sessions and loses all progress. Always check `gt polecat list --all` first.
- GT requires expert supervision. Configure rig test commands before launching convoys.
- Prefer `shiny-enterprise` over raw `mol-polecat-work` for production-quality code.
- Always run `gt doctor --fix` after infrastructure changes, but only when no polecats are working.
- Non-Claude agents (Codex, Gemini) require wrapper scripts for context injection. See the agent configuration reference.

## Workflow

### Step 1: Verify or Create the Workspace

Check for existing HQ, create if needed, verify health. See `references/setup-pitfalls.md` for common issues and fixes.

```bash
ls ~/gt/mayor/town.json                          # check HQ exists
gt install ~/gt --git --shell --wrappers          # create HQ if needed
cd ~/gt && gt doctor                              # verify health
cd ~/gt && gt doctor --fix                        # auto-fix (no running polecats!)
```

### Step 2: Initialize a Rig

A rig wraps a git repository. See `references/setup-pitfalls.md` for detailed steps and gotchas (hyphen naming, symlinks, git_url).

```bash
cd /path/to/project && git init && git commit --allow-empty -m "Initial commit"
gt init
ln -s /path/to/project ~/gt/project_name         # if project lives outside ~/gt/
cd ~/gt && gt rig add project_name --adopt --force
```

### Step 3: Configure Infrastructure

Initialize Dolt, install shell integration, start services. See `references/infrastructure.md` for detailed setup and Dolt troubleshooting.

```bash
cd ~/gt && gt dolt init-rig hq && gt dolt init-rig project_name && gt dolt start
gt shell install && source ~/.zshrc
cd ~/gt && gt up
```

### Step 4: Configure the Agent Runtime

GT supports multiple AI agents. Non-Claude agents need wrapper scripts. See `references/agent-configuration.md` for setup details.

```bash
gt config default-agent list                      # see available agents
gt config default-agent codex                     # set default
gt install --wrappers --force                     # install gt-codex, gt-gemini wrappers
gt config agent set codex "$HOME/bin/gt-codex"    # point agent to wrapper
```

### Step 5: Run the Spec-to-Plan Pipeline

Pass a specification to `mol-idea-to-plan`. See `references/spec-to-code-pipeline.md` for the full 8-step pipeline, variable options, and how to reuse prior PRD work.

```bash
cd ~/gt && gt sling mol-idea-to-plan project_name --create \
  --var problem="<specification>" \
  --var context="<tech stack, constraints>"
```

### Step 6: Configure Rig Quality Gates

Before launching coding work, configure test commands. See `references/formula-hierarchy.md` for formula selection guidance.

```bash
gt rig config set project_name default_formula shiny-enterprise --global
gt rig config set project_name setup_command "pnpm install" --global
gt rig config set project_name test_command "pnpm -r run test" --global
gt rig config set project_name typecheck_command "pnpm -r run typecheck" --global
gt rig config set project_name lint_command "pnpm -r run lint" --global
gt rig config set project_name build_command "pnpm -r run build" --global
gt rig config show project_name                   # verify
```

### Step 7: Launch the Coding Convoy

Stage and launch the convoy from the epic bead. See `references/convoy-orchestration.md` for wave execution, monitoring, and Mountain-Eater mode.

```bash
cd ~/gt && gt convoy stage <epic-bead-id> --launch --no-validate
gt convoy status <convoy-id>
gt polecat list --all
```

If auto-dispatch doesn't connect, sling Wave 1 manually:

```bash
cd ~/gt && gt sling <wave-1-bead> project_name --create
```

### Step 8: Monitor and Manage

```bash
gt polecat list --all                             # active workers
gt polecat status project_name/<name>             # specific polecat
tmux -L <socket> attach -t <session>              # live output (Ctrl+B D to detach)
gt trail                                          # recent activity
gt convoy status <convoy-id>                      # convoy progress
gt ready                                          # unblocked work
```

## Key Concepts

See `references/concepts-glossary.md` for full definitions of all Gas Town components.

| Concept | Role |
|---|---|
| **HQ (Town)** | Top-level workspace (`~/gt/`) |
| **Rig** | Project container wrapping a git repo |
| **Polecat** | Ephemeral worker agent |
| **Bead** | Work item tracked in Dolt |
| **Hook** | Durability primitive — work survives session restarts |
| **Formula** | TOML workflow template (shiny, TDD, code-review) |
| **Convoy** | Dependency-aware batch orchestration with parallel waves |
| **Witness** | Per-rig polecat health monitor |
| **Refinery** | Per-rig merge queue processor |
| **Mayor** | Global cross-rig coordinator |
