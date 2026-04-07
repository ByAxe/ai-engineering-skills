# Spec-to-Code Pipeline

The complete Gas Town pipeline from a raw specification to production code.

## Phase 1: Spec to Plan (mol-idea-to-plan)

Single command entry point:

```bash
cd ~/gt && gt sling mol-idea-to-plan <rig> --create \
  --var problem="<specification text>" \
  --var context="<tech stack, constraints, existing artifacts>"
```

### Pipeline Steps

1. **Intake** — Agent structures raw idea into draft PRD
2. **PRD Review** — 6 parallel polecats review (requirements, gaps, ambiguity, feasibility, scope, stakeholders)
3. **Human Clarification** — ONLY human gate: agent presents questions, you answer
4. **Design Generation** — 6 parallel polecats design (api, data, ux, scale, security, integration)
5. **PRD Alignment Round 1** — Requirements + Goals coverage (2 polecats)
6. **PRD Alignment Round 2** — Constraints + Non-goals enforcement (2 polecats)
7. **PRD Alignment Round 3** — User stories + Open questions resolution (2 polecats)
8. **Plan Self-Review** — 3 rounds x 2 polecats (completeness, sequencing, risk, scope-creep, testability, coherence)

### Output
- PRD document at `.prd-reviews/<project>/prd-draft.md`
- 6 review artifacts (ambiguity.md, feasibility.md, gaps.md, requirements.md, scope.md, stakeholders.md)
- Design document at `.designs/<project>/`
- Beads with dependency graph
- Epic bead linking everything

### Reusing Prior PRD Work
If a previous run produced artifacts, skip early steps:
```bash
--var context="Previous PRD at .prd-reviews/project/prd-draft.md plus review artifacts. Skip Steps 1-3, proceed from Step 4."
```

## Phase 2: Plan to Code (Convoy)

### Configure Quality Gates First
Set up rig test/build commands before launching coding work. See rig-settings reference.

### Launch
```bash
# One command: analyze dependencies, compute waves, dispatch
cd ~/gt && gt convoy stage <epic-bead-id> --launch
```

### What Happens Automatically
1. Dependency DAG analyzed, waves computed
2. Wave 1 tasks (no dependencies) dispatched to parallel polecats
3. Each polecat runs the work formula (default: `mol-polecat-work`)
4. Polecats: implement → run gates → pre-verify → `gt done`
5. Refinery processes merge queue, merges to main
6. Wave 2 dispatched when Wave 1 dependencies complete
7. Repeat until all waves done

### With Quality Formulas
```bash
# Use shiny-enterprise for production quality
gt convoy stage <epic-id> --launch --formula shiny-enterprise
```

Each polecat then follows: design → implement(5-pass) → review → test → submit

## Phase 3: Code Review (Optional)

After coding convoy lands, run a review convoy:
```bash
cd ~/gt && gt formula run code-review --preset full
```

10 parallel reviewers produce synthesized findings filed as beads.

## Phase 4: Integration and Polish

Run synthesis on the convoy:
```bash
gt synthesis status <convoy-id>
gt synthesis start <convoy-id>
```

This combines all polecat work into a coherent whole, resolves integration issues, and validates end-to-end behavior.

## Agent Selection

GT defaults to Claude Code. Override globally or per-sling:
```bash
gt config default-agent codex      # global default
gt sling <bead> <rig> --agent claude  # per-task override
```

Available built-in agents: claude, codex, gemini, copilot, cursor, amp, auggie, opencode, omp, pi.
