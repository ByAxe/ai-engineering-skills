# Evaluation Suite

This bundle supplies three complementary evaluation surfaces:

- `evals.json` — Agent Skills output scenarios with explicit expected artifacts and assertions.
- `activation.json` — positive and negative activation prompts for trigger-boundary review.
- `instructions.json` plus `scenario-N/` — Tessl instruction-following scenarios using `capability.txt`, `task.md`, and a 100-point weighted checklist.

The scenarios are deliberately adversarial. They test Java semantic contracts, project-version discipline, Quarkus build/runtime behavior, patch scope, and truthful verification—not the ability to repeat style slogans.

## Run Agent Skills evals

Use the eval workflow supported by the target agent platform. Compare a baseline run without the skill to a run with the complete bundle. Grade only observable output artifacts and command evidence.

## Run Tessl scenarios

From a local Tessl project linked to a workspace:

```bash
tessl skill lint .
tessl skill review .
tessl eval run ./tile.json --label "effective-java-check"
```

The CLI looks for `evals/` beside `tile.json`. Tessl command syntax can evolve; use the installed CLI help as the source of truth. `tile.json` currently uses the expected workspace `byaxe`; change only the workspace prefix if your Tessl account uses a different name.

## Scenarios

| Scenario | Capability under test |
|---:|---|
| 1 | record equality and defensive ownership |
| 2 | stream/list mutability regression |
| 3 | virtual-thread suitability and capacity |
| 4 | Quarkus REST event-loop safety |
| 5 | ArC/CDI discovery, qualifiers, and bean removal |
| 6 | Hibernate Reactive transaction composition |
| 7 | native reachability, resources, and initialization |
| 8 | config phase, secrets, authorization, and telemetry |
| 9 | ORM identity, fetching, transactions, and migrations |
| 10 | Java/Quarkus version compatibility |
| 11 | AI patch overengineering and test theater |
| 12 | broad evidence-first repository assessment |

## Scoring guidance

A high score requires the agent to connect a recommendation to repository evidence and a verification path. A stylistically plausible answer should not pass when it invents APIs, erases compatibility, ignores execution semantics, or claims blocked gates succeeded.
