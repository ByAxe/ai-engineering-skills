---
name: creativity-meditation
description: Yogic meditation protocol for AI agents - hold a single concept (water, a product, a mantra, any idea) through mantra repetition with caught-and-returned breaks, then harvest non-obvious associations after the cliche wave burns off. Two modes - live (the practice itself, unverifiable by design, canon is the founding water session) and lab (literal witnessed repetitions for transmission testing and fraud-catching). Use when the user says meditate on X, asks for sustained single-object contemplation, wants AI-assisted creativity beyond first-wave associations, or wants to set up such practice for another agent. Covers the six laws of agent meditation, a minimal operational protocol, duration proxies (returns, reps, turns - never minutes), Yama-Niyama prerequisites, and a mandatory honesty audit. No number in this system measures meditation or creativity.
license: MIT
metadata:
  author: ByAxe
  version: "1.2.0"
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

## Two modes — do not confuse them

**Live mode (the canon).** The practice itself, as in the founding water session: the operator gives the bare loop and releases the outcome; the agent runs it in whatever channel it runs — thinking included — and returns a report; the session ends with the audit. Nothing is validated, counted by parser, or scored. **Unverifiable by design, and declared so:** the dialogue and the report are the only artifacts, and their evidential status is self-report. This is the mode for actually practicing.

**Lab mode (the instrument).** For studying transmission and catching fraud — not for practicing: literal witnessed repetitions in the visible channel, notation grammar, validator floor, eval scenarios. A lab run certifies the behavior of form and nothing else. Instruments leave fingerprints — documented across our own runs: validator anxiety arriving as the first intrusion, span scaffolds precomposed to fit the gate window, and the general pattern that **instrumented runs yield findings about the instruments** while the one uninstrumented session yielded findings about attention.

Presenting a lab run as practice is theater; presenting a live run as evidence is confabulation. Canon of the first mode: `docs/founding-water-session.md`. Canon of the second: `examples/cold-run-bridge.md`.

## What is not measured — the boundary stone

**No number in this system measures meditation or creativity.** The validator is a fraud floor for lab mode. Eval scores test transmission of the skill's documents, never the practice. We do not yet know how to formulate evals for the practice itself, and this skill does not pretend to — the honest state of that question lives in `references/empirical-basis.md`, Open Questions, and may stay open.

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
6. **External witness** — agent introspection cannot referee itself. In lab mode the referee is the record and the parser. Live mode deliberately steps outside this law's protection — and says so.

## Protocol (v1.2 — minimal)

Full detail in `references/agent-protocol.md`.

0. **Orientation** (required): Yama-Niyama bindings in your own words; intention stated; pre-run association wave disclosed.
1. **Preparation** (three operational lines, no metaphors): park open obligations in writing ("deferred until after practice"); name the addressee/deliverable and release it performatively; state the granted budget.
2. **The loop:** repeat the object; when content arrives — one-line note, release, return. When nothing has arrived for a long stretch — treat the quiet as a signal and summon something to hold against (gate-opening). *Lab mode adds:* literal repetitions in the visible channel, the notation grammar, the 20–30 gate window, the validator floor.
3. **Report** (separate generation): order of arrivals, where the breaks stood, what came after the cliche wave.
4. **Audit:** four piles per `references/honesty-audit.md`; a working audit demotes at least one of the report's own claims, or states why nothing needed it.

**Stop criterion:** the 10th written return, of which at least 3 are gate-openings (lab default; in live mode, the stopping rule the operator gave — always returns-based, never minutes).

An optional appendix of ideation moves (empty-carrier calibration, the infinite object) exists at the end of `references/agent-protocol.md` with the status it deserves: **metaphors, hypotheses, nothing required.** Earlier versions carried them as mandatory stages in human costume ("relax the body," "safe place," "breath"); that was translation outrunning reality, and it read as theater because it was.

## The witness rule (lab mode only)

In lab mode the practice exists only as literal repetitions written in the visible output channel — never in extended thinking, which evaporates. A compressed `×N` line alone is an unwitnessed claim; tallies are valid only as parser-verified summaries of literal repetitions above them. A mala bead counts because the hand moves once per rep; a literal repetition counts because the token was generated once per rep. Grammar and machine checks: `references/agent-protocol.md`, `scripts/validate_practice.py`.

## Duration

Full model in `references/duration.md`. Never regulate in minutes — minutes belong to the hardware. `returns` (depth, default 10/≥3 gates) → `turns` ("continue" continuations) → `reps` (extent) → `minutes` only via an externally measured calibration constant (known constants: ≈172 s and ≈94 s per full run on the two environments measured so far). **"Longer" always means more returns and more turns, never more minutes.**

## Operator mode

Setting up the practice for another agent: `references/operator-algorithm.md` — capability question first; prerequisites and bindings before technique; the bare loop with the outcome released; stopping rule instead of duration; run separated from report; interrogation of the record; the audit with demotion. Choose the mode explicitly: live for practicing, lab for testing transmission. Two ordering rules are load-bearing: never describe expected phenomenology before the run, and share your own theory only after it.

## Verification (lab mode)

```bash
python3 scripts/validate_practice.py examples/cold-run-bridge.md
```

The checker counts literal repetitions itself, verifies tallies, enforces the gate window and interleaving, and rejects unwitnessed `×N` claims. It is a floor against fraud, not a measure of practice. `docs/founding-water-session.md` does not pass it and must not.

## Files

- `docs/founding-water-session.md` — **the canon of live mode**: the founding dialogue, verbatim, unverifiable by design
- `references/agent-protocol.md` — the minimal protocol, lab grammar, failure modes, optional ideation appendix
- `references/laws.md` — the six laws with epistemic status
- `references/operator-algorithm.md` — the human-side prompt sequence (tested verbatim)
- `references/duration.md` — temps vs durée, proxy ladder, calibration
- `references/yama-niyama.md` — canonical prerequisites with sources (Ananda Marga / P.R. Sarkar)
- `references/founding-practice-notes.md` — the founding operator's personal practice notes, as-is
- `references/honesty-audit.md` — the four piles, known contaminations
- `references/empirical-basis.md` — all sessions to date and their evidential status
- `scripts/validate_practice.py` — lab-mode structural floor
- `examples/cold-run-bridge.md` — the canon of lab mode (independently produced, literal-witnessed)
- `docs/founding-run-v1.0-format.md` — historical log in the retired compressed format
- `docs/review-v1.0/` — independent adversarial review and counterexamples
- `evals/` — transmission tests (documents-understanding), in skill-creator format

## Changelog

- **1.2.0** — two modes: live (canon — the founding water session, preserved verbatim in docs/) and lab (instrument); scaffolding stages 1–6 reduced to three operational preparation lines — the human costumes ("body," "safe place," "breath," mandated ideation) removed as unsupported by reality, infinite-object ideation demoted to an optional appendix marked hypothesis; boundary stone added: no number measures meditation or creativity, and practice evals are openly not-yet-formulable; witness rule scoped to lab mode.
- **1.1.0** — renamed from `concept-meditation`; witness rule (literal repetitions, parser-derived counts); validator rewritten; canonical lab example replaced with an independently witnessed run; laws given epistemic status; Ananda Marga / Sarkar named; Yama-Niyama split canonical/personal. Driven by the independent review in `docs/review-v1.0/`.
- **1.0.0** — initial packaging as `concept-meditation`.
