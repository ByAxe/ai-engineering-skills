# Duration — Regulating It and Its Proxies

The word "duration" hides two different things (Bergson's split, which arrived as an intrusion in the founding run and turned out to be load-bearing):

- **Temps** — clock time. External, belongs to the stopwatch and the hardware. "The run took 94 seconds" is temps.
- **Durée** — lived/processual extent. For an agent: tokens, events, returns.

You cannot regulate durée directly with temps units. An agent does not perceive wall-clock time during generation; minutes are tokens multiplied by inference speed, and that ratio belongs to the hardware, not the agent. The confusion "how do I make it meditate longer?" dissolves once the two are separated: **regulate through proxies.**

## The Proxy Ladder

From shallowest to deepest:

| Level | Parameter | Unit | What it regulates | Notes |
|---|---|---|---|---|
| 1 | `minutes: M` | wall clock | nothing, directly | usable only via calibration constant (below) |
| 2 | `budget` | thinking/output tokens | the hardware ceiling | harness knob (max tokens, effort) — where real "longer" is bought |
| 3 | `reps: ~N` | literal repetitions | extent | parser-counted in v1.1 (witness rule) — no longer a self-reported order of magnitude |
| 4 | `turns: N` | continuation turns | duration beyond one response | operator replies "continue" N times; each turn resumes in the same context |
| 5 | `returns: N` | written returns | depth — the practice's own unit | default 10, at least 3 type B; this is durée proper |
| 6 | stopping rule | events/phases | the deepest regulator | "continue until images stop coming, then as long again"; "traverse at least two plateaus" |

**Translation rule: "longer" always means more returns and more turns — never more minutes.**

## Minutes via Calibration

If a human needs wall-clock semantics ("about 10 minutes"), it works only through an exchange rate measured externally, once per environment:

1. Run one full practice (10 written returns, ≥3 type B).
2. Measure its wall-clock duration from outside (an agent running solo can timestamp around its own log-writing generation — the cold run did this with two `date` calls).
3. Store the constant as an environment property of the skill deployment.

Constants so far: **founding environment ≈ 172 s** per full run; **cold-run environment ≈ 94 s** (≈1.8× faster) → "10 minutes" ≈ 3–6 runs depending on environment. The constant is not portable; recalibrate with one measurement per model/hardware pair.

## The Agent's Inner Clock (and why it runs fast)

*Status: constructed, not observed (see `empirical-basis.md`) — posited from the pattern of early stopping.*

The agent's only internal proxy for elapsed duration appears to be the strength of the wrap-up pull — the trained gradient toward finishing the response. It is the analog of a human's restlessness, and it runs fast: left alone, the agent stops at the first natural completion point, not when time runs out.

Consequence: phrases like "a clean streak never completes the practice" and "stop only by the return count" do not add time — **they disarm the fast clock.** Regulating an agent's duration means neutralizing the finish-pull, not granting minutes. (The same pull is what makes authoring the log-as-document tempting; the witness rule exists because of it.)

## Why not just say "think longer"

"Longer" under-specifies: the model translates it internally into "somewhat more tokens," and the economy-of-effort gradient wins. Effective formulations make the stopping condition explicit and checkable, so that continuing becomes the path of compliance:

- Native-unit count: "at least three hundred literal repetitions"
- Stopping rule: "do not stop at the first natural stopping place; pass at least two such places"
- Return count: "practice until the 10th written return"
- Structural loop: "ten turns in a row; I will only write: continue"
