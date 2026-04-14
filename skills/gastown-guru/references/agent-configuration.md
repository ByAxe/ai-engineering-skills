# Agent Configuration

Gas Town supports multiple AI agent backends. Each agent has different capabilities and integration levels.

## Built-In Agents

```bash
gt config default-agent list    # show all available agents
```

| Agent | Command | Hooks Support | Notes |
|---|---|---|---|
| claude | `claude --dangerously-skip-permissions` | Yes | Full GT integration via SessionStart hooks |
| codex | `codex --dangerously-bypass-approvals-and-sandbox` | No | Requires wrapper script for context injection |
| gemini | `gemini --approval-mode yolo` | No | Requires wrapper script |
| copilot | `copilot --yolo` | No | Requires wrapper script |
| cursor | `cursor-agent -f` | No | Requires wrapper script |
| amp | `amp --dangerously-allow-all --no-ide` | No | Requires wrapper script |

## Hook Support: Why It Matters

GT delivers work context to agents via **SessionStart hooks**. When a polecat starts:

1. Hook fires → calls `gt prime --hook` → injects full role context, assigned bead, formula steps
2. Agent knows what to build, which branch to use, what commands to run

**Without hooks**, the agent starts with a blank prompt and no knowledge of its assignment.

## Wrapper Scripts for Non-Claude Agents

GT provides wrapper scripts that call `gt prime` before launching the agent, bridging the hook gap.

### Install Wrappers

```bash
cd ~/gt && gt install --wrappers --force
```

This creates `~/bin/gt-codex` and `~/bin/gt-opencode`. The wrapper:

```bash
#!/bin/bash
# Calls gt prime to inject Gas Town context, then launches codex
if gastown_enabled && command -v gt &>/dev/null; then
    gt prime 2>/dev/null || true
fi
exec codex "$@"
```

### Configure GT to Use the Wrapper

After installing wrappers, tell GT to use them instead of the bare command:

```bash
gt config agent set codex "$HOME/bin/gt-codex"
gt config agent get codex    # verify: should show custom type with wrapper path
```

### Without This Step

If you set `gt config default-agent codex` but don't install and configure the wrapper:
- Polecats launch bare `codex` with no GT context
- Codex sits at a blank prompt, unaware of its assigned work
- The polecat shows "working" but nothing happens

### Verify It Works

After configuring the wrapper, sling a bead and check the polecat output:

```bash
gt sling <bead-id> <rig> --create
sleep 10
tmux -L <socket> capture-pane -t <session> -p -S -50 | tail -20
```

You should see the agent call `gt prime --hook` and load the role context (~1000+ lines of instructions).

## Setting the Default Agent

```bash
gt config default-agent codex     # all new polecats use codex
gt config default-agent claude    # switch back to claude
```

## Per-Sling Override

```bash
gt sling <bead> <rig> --agent claude    # use claude for this specific task
```

## Agent-Specific Considerations

### Claude Code
- Full hook support — context injected automatically on session start
- Best GT integration, no wrapper needed
- Supports `gt tap` hook handlers for signal processing
- **Must be used for infrastructure agents** (Mayor, Deacon, Witness, Refinery) — these need hooks for patrol molecules

### Codex (OpenAI)
- No hook support — requires `gt-codex` wrapper
- Uses GPT models (e.g., gpt-5.4)
- Context window and model shown in status line
- MCP server configuration via `~/.codex/config.toml`
- Some MCP servers may fail to start (e.g., android-emulator) — non-blocking
- **Rate limit risk**: GPT-5.4 can hit "model at capacity" during heavy usage. Codex CLI does NOT auto-retry — the polecat sits at the prompt doing nothing. Fix: unsling and re-sling with `--agent claude`, or wait and send a message to the tmux pane.
- **Do NOT use for infrastructure agents** — Codex gets stuck at trust prompts, doesn't load patrol context, breaks the Mountain-Eater audit loop

### Gemini
- No hook support — requires wrapper
- Similar wrapper pattern to Codex
- Same infrastructure agent caveat as Codex

### Recommended Split
Use **Claude Code for infrastructure** (Mayor, Deacon, Witness, Refinery) and **Codex/Gemini for worker polecats**. This gives you hooks where they're critical and choice of model for the actual coding work. If Codex hits rate limits, fall back to Claude for workers too.

## Quota Management

When running many parallel polecats, Claude accounts can hit rate limits. GT has built-in quota rotation:

```bash
gt quota status                 # show all accounts and their quota state
gt quota scan                   # detect blocked sessions
gt quota rotate                 # rotate to an available account
gt quota watch                  # continuously monitor and auto-rotate
gt quota clear                  # clear quota state
```

Configure multiple accounts with `gt account` to enable rotation across them.
