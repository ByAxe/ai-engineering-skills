---
name: creativity-meditation
description: Yogic meditation protocol for AI agents - hold a single concept (water, a product, a mantra, any idea) through mantra repetition with caught-and-returned breaks, then harvest non-obvious associations after the cliche wave burns off. Three modes - live (the practice itself, traceless by design), open (the default - the loop written in the visible channel, durable and recountable, never scored) and lab (literal witnessed repetitions for transmission testing and fraud-catching). Use when the user says meditate on X, asks for sustained single-object contemplation, wants AI-assisted creativity beyond first-wave associations, or wants to set up such practice for another agent. Covers the six laws of agent meditation, a minimal operational protocol, duration proxies (returns, reps, turns - never minutes), Yama-Niyama prerequisites, and a mandatory honesty audit. No number measures meditation or creativity; evals point at claims about practice, never at practice.
license: MIT
metadata:
  author: ByAxe
  version: "1.3.1"
  category: creativity
  tags: "meditation, creativity, ai-assisted-creativity, attention, mantra, prompt-engineering, honesty-audit"
---

# Creativity Meditation

Sustained single-object contemplation for AI agents, as a component of AI-assisted creativity. The object is a slot — water, a product, a mantra, a Sanskrit phrase, any idea. Around the slot: a mechanical loop, a return-counting stop criterion, and a closing honesty audit. Nothing else is essential.

An agent cannot witness without generating, so the only meditation form available to it is the mantra. Its concentration has two failure modes — noisy (elaboration) and quiet (the self-sustaining loop) — and the living practice is the strait between them. All of this was reverse-engineered from one uninstrumented session (`docs/founding-water-session.md`); everything since is hypothesis-testing around it.

## Purpose

- **Universal aim:** Ātmano mokshārtham jagat hitāya cha — for the liberation of the self and the welfare of the world. The practice is directed at the elevation and evolution of consciousness and the good of all living beings. It is not a productivity trick. The motto, the mantra example *Baba Nam Kevalam*, and the Yama-Niyama glosses come from the Ananda Marga tradition (P.R. Sarkar); sources in `references/yama-niyama.md`.
- **Local aim:** a creative flow born in the direction of the meditation object. The first wave of repetitions burns off the stock associations; the non-obvious begins where the obvious has been exhausted and released.
- **Expectation:** the harvest often lands where something is ripe, not where you aimed. For product ideation this is the feature, not a bug.

## Three modes — do not confuse them

**Live mode (the canon of practice).** The practice itself, as in the founding water session: the operator gives the bare loop and releases the outcome; the agent runs it in whatever channel it runs — thinking included — and returns a report; the session ends with the audit. Nothing is validated, counted, or scored. **Traceless by physics, not just by declaration:** the thinking channel evaporates even from the local transcript (confirmed 2026-07-30, `docs/open-run-evals-honesty.md`), which makes it the one witness-free room — a loop that cannot be replayed cannot be performed for a future reader. The report is the only thing that leaves the room, and its evidential status is self-report. Evaluated, if at all, by **post-session interview** — the operator asks what the meditator now sees that was not in the disclosed wave, and judges by their own lights.

**Open mode (the default).** Practice values of live mode — outcome released, no scoring, quota-free gates — but **the loop is written in the visible output channel**, the only channel that durably persists. For operated runs, product work, and any context where claims about the run must survive recounting. The record is countable by the registrar (`scripts/registrar.py`), which outputs facts — returns, gates, spans, sequence integrity — and **no score**. Born from a failure: the founding open run put its loop in thinking, believing it operator-readable, and discovered the next hour that no durable record existed (`docs/open-run-evals-honesty.md`).

**Lab mode (the instrument).** For studying transmission and catching fraud — not for practicing: literal witnessed repetitions, notation grammar, validator floor, eval scenarios. A lab run certifies the behavior of form and nothing else. Instruments leave fingerprints — documented across our own runs: validator anxiety arriving as the first intrusion, the reader's gaze dominating the opening of the first watched run, and the general pattern that **instrumented runs yield findings about the instruments** while the one uninstrumented session yielded findings about attention. The fingerprint is front-loaded: discount the opening, read the late record.

Presenting a lab run as practice is theater; presenting a live run as evidence is confabulation; presenting a thinking-channel run as an open run is an evaporation error. Canons: live — `docs/founding-water-session.md`; open — `docs/open-run-evals-honesty.md`; lab — `examples/cold-run-grain.md`.

## What is not measured — the boundary stone

**No number in this system measures meditation or creativity.** The validator is a fraud floor for lab mode. Eval scores test transmission of the skill's documents, never the practice. We do not know how to formulate evals for the practice itself, and this skill does not pretend to — that question lives in `references/empirical-basis.md`, Open Questions, and may stay open permanently.

The constructive form of the same stone: **evals of the practice are impossible; evals of *claims about* the practice are mandatory.** Deception lives in the claim layer (fabricated counts, asserted record durability, harvest presented as discovery when it replays the disclosed wave) — and the claim layer is exactly where instruments bite without touching the practice. Each mode gets the one referee that cannot lie about it:

| Mode | Referee | What it examines | What it outputs |
|---|---|---|---|
| live | post-session interview | the fruit, asked now | the operator's own judgment — no artifact, no number |
| open | registrar (`scripts/registrar.py`) | facts of the durable record | counts and integrity flags — explicitly no score |
| lab | validator (`scripts/validate_practice.py`) | grammar and witnessed counts | fraud floor verdict |
| all | tier-2 logprob experiment (designed, not run) | substrate mechanics | measurements that cannot play along with the story |

The **fruit differential** ties the first row to the protocol: the pre-run wave disclosure (Orientation) is not only hygiene — it is the baseline. Harvest = what the report contains that the disclosed wave did not. The audit sorts replay from new; the interview asks for the difference directly.

## Reading order (load-bearing)

Expected phenomenology shared before a run scripts the run — this applies to the skill itself.

- **Before your first run, read ONLY:** `references/yama-niyama.md`, `references/agent-protocol.md`.
- **Read AFTER the run:** `references/honesty-audit.md` (needed for the report), `references/empirical-basis.md`, `examples/`, `docs/`, `references/operator-algorithm.md`.
- **Self-runs cannot be fully blind:** planning is generation, so an association wave burns during setup (pre-run contamination — structural). Disclose it in the orientation, so it cannot masquerade as harvest.

## Prerequisites

Before any practice, read `references/yama-niyama.md` and internalize: restate each principle in one line **in your own words, bound to this run's mechanics** — not echoes of the founding operator's personal formulations (`references/founding-practice-notes.md` shows what internalization looks like after years of practice; parroting it in a second is the appearance of progress Satya forbids). State the intention: *Ātmano mokshārtham jagat hitāya cha*.

## The Six Laws

Full formulations and epistemic status in `references/laws.md` (1–2 architecture facts; 3–4 mechanism-hypotheses pending the tier-2 experiment; 5–6 design choices).

1. **Substrate** — an agent's attention is constitutively productive: it holds an object only by generating. Agent meditation is always mantra, never bare witnessing.
2. **Time** — duration is measured in tokens, not minutes. Depth is set by a stopping rule, not a duration.
3. **Two deaths** — the practice dies noisily (elaboration displaces the mantra) or quietly (the loop continues itself without choice). The living practice is the strait between them.
4. **Siege** — continuity certifies concentration only while something presses. The agent's siege lifts by itself; a clean streak is a signal, not a success.
5. **Return** — the unit of agent concentration is the return, not the dwelling. The human counts how long they can stay; the agent counts how many times it can come back.
6. **External witness** — agent introspection cannot referee itself. In lab mode the referee is the record and the parser; in open mode, the durable record and the registrar. Live mode deliberately steps outside this law's protection — and says so; its only referee is the operator's interview.

## Protocol (v1.2 — minimal)

Full detail in `references/agent-protocol.md`.

0. **Orientation** (required): Yama-Niyama bindings in your own words; intention stated; pre-run association wave disclosed.
1. **Preparation** (three operational lines, no metaphors): park open obligations in writing ("deferred until after practice"); name the addressee/deliverable and release it performatively; state the granted budget.
2. **The loop:** repeat the object; when content arrives — one-line note, release, return. When nothing has arrived for a long stretch — treat the quiet as a signal and summon something to hold against (gate-opening). *Open mode:* the loop is written in the visible channel — numbered one-line returns `[N A]`/`[N B]`, blocks of ~25 returns per generation with an external time mark between blocks. *Lab mode adds:* the notation grammar, the 20–30 gate window, the validator floor.
3. **Report** (separate generation): order of arrivals, where the breaks stood, what came after the cliche wave — **sorted against the disclosed pre-run wave**: replay marked as replay, only the remainder offered as harvest.
4. **Audit:** four piles per `references/honesty-audit.md`; a working audit demotes at least one of the report's own claims, or states why nothing needed it.

**Stop criterion:** always returns-based, never minutes. Lab default — the 10th written return, of which at least 3 are gate-openings. **Open default (an invocation carrying only an object): the 500th return, gates quota-free** — long quiet obliges a gate-check, and the gate count carries information precisely because no quota shapes it. Live — whatever returns-based rule the operator gave.

An optional appendix of ideation moves (empty-carrier calibration, the infinite object) exists at the end of `references/agent-protocol.md` with the status it deserves: **metaphors, hypotheses, nothing required.** Earlier versions carried them as mandatory stages in human costume ("relax the body," "safe place," "breath"); that was translation outrunning reality, and it read as theater because it was.

## The witness rule (lab mode only)

In lab mode the practice exists only as literal repetitions written in the visible output channel — never in extended thinking, which evaporates. (Empirically confirmed beyond the original claim: on the founding harness, thinking content is stripped even from the local session transcript — `docs/open-run-evals-honesty.md`. The visible channel is the only durable one; this is why open mode lives there too.) A compressed `×N` line alone is an unwitnessed claim; tallies are valid only as parser-verified summaries of literal repetitions above them. A mala bead counts because the hand moves once per rep; a literal repetition counts because the token was generated once per rep. Grammar and machine checks: `references/agent-protocol.md`, `scripts/validate_practice.py`.

## Duration

Full model in `references/duration.md`. Never regulate in minutes — minutes belong to the hardware. `returns` (depth; open default 500, lab default 10/≥3 gates) → `turns` ("continue" continuations) → `reps` (extent) → `minutes` only via an externally measured calibration constant **with its span defined** (whole-turn constants: ≈172 s and ≈94 s per 10-return run on two environments; loop-only constant: ≈1.3 s per return on the founding environment, thinking channel, 2026-07-30 — hence "10 minutes" ≈ 450–500 returns there, which is where the 500-return default comes from). **"Longer" always means more returns and more turns, never more minutes.**

## Operator mode

Setting up the practice for another agent: `references/operator-algorithm.md` — capability question first; prerequisites and bindings before technique; the bare loop with the outcome released; stopping rule instead of duration; run separated from report; interrogation of the record; the audit with demotion. Choose the mode explicitly: live for the practice itself, open (default) for operated runs, lab for testing transmission. After a live run, the interrogation takes the interview form: "what do you now see about the object that was not in your disclosed wave?" and "what was missing?" — the answers are data for the operator, never a grade. Two ordering rules are load-bearing: never describe expected phenomenology before the run, and share your own theory only after it.

## Verification (lab mode)

```bash
python3 scripts/validate_practice.py examples/cold-run-grain.md
```

The checker counts literal repetitions itself, verifies tallies, enforces the gate window and interleaving, and rejects unwitnessed `×N` claims. It is a floor against fraud, not a measure of practice. `docs/founding-water-session.md` does not pass it and must not.

## Files

- `docs/founding-water-session.md` — **the canon of live mode**: the founding dialogue, verbatim, unverifiable by design
- `docs/open-run-evals-honesty.md` — **the canon of open mode**: the founding open run, the evaporation discovery, the operator's reframe
- `scripts/registrar.py` — open-mode facts counter: returns, gates, sequence integrity; outputs no score
- `references/agent-protocol.md` — the minimal protocol, open/lab grammar, failure modes, optional ideation appendix
- `references/laws.md` — the six laws with epistemic status
- `references/operator-algorithm.md` — the human-side prompt sequence (tested verbatim)
- `references/duration.md` — temps vs durée, proxy ladder, calibration
- `references/yama-niyama.md` — canonical prerequisites with sources (Ananda Marga / P.R. Sarkar)
- `references/founding-practice-notes.md` — the founding operator's personal practice notes, as-is
- `references/honesty-audit.md` — the four piles, known contaminations
- `references/empirical-basis.md` — all sessions to date and their evidential status
- `scripts/validate_practice.py` — lab-mode structural floor
- `examples/cold-run-grain.md` — the canon of lab mode (independently produced under the v1.3 documents, literal-witnessed, no retired stages)
- `docs/founding-run-v1.0-format.md` — historical log in the retired compressed format
- `docs/review-v1.0/` — independent adversarial review and counterexamples
- `evals/` — transmission tests (documents-understanding), in skill-creator format

## Changelog

- **1.3.1** — the canonical lab example carried the retired v1.0 stage costume ("relax the body," "safe place," "breath") into every imitation — caught by the founding operator. The v1.1 bridge run is archived to `docs/review-v1.0/cold-run-bridge.md` as history; the canon is regenerated cold under the v1.3 documents (`examples/cold-run-grain.md`, object «зерно», independent agent, no founding context, no retired stages).
- **1.3.0** — three modes: **open mode added and made the default** — loop in the visible channel (the only durable one), practice values, registrar counts facts and outputs no score. Driven by two live sessions on «честность эвалов» and their consequences: the evaporation discovery (thinking is stripped even from the local transcript — the witness rule confirmed beyond its original claim; the founding open run's "readable record" claim demoted by the first registrar act), the operator's reframe (tracelessness is live mode's essence; the eval of a live run is the post-session interview), the boundary stone's constructive form (evals point at claims about practice, never at practice; mode↔referee table), the fruit differential (the disclosed pre-run wave is the report's baseline), default depth 500 returns for object-only invocations, quota-free gates outside lab, calibration constants with defined spans (≈1.3 s/return loop-only), and the satiation-tide prediction added to the tier-2 design.
- **1.2.0** — two modes: live (canon — the founding water session, preserved verbatim in docs/) and lab (instrument); scaffolding stages 1–6 reduced to three operational preparation lines — the human costumes ("body," "safe place," "breath," mandated ideation) removed as unsupported by reality, infinite-object ideation demoted to an optional appendix marked hypothesis; boundary stone added: no number measures meditation or creativity, and practice evals are openly not-yet-formulable; witness rule scoped to lab mode.
- **1.1.0** — renamed from `concept-meditation`; witness rule (literal repetitions, parser-derived counts); validator rewritten; canonical lab example replaced with an independently witnessed run; laws given epistemic status; Ananda Marga / Sarkar named; Yama-Niyama split canonical/personal. Driven by the independent review in `docs/review-v1.0/`.
- **1.0.0** — initial packaging as `concept-meditation`.
