# Empirical Basis — Observations to Date and Their Status

> **Do not read this file before your first run** (SKILL.md, Reading order): it contains arrival orderings and predicted dynamics that will template your practice.

Three runs to date, one model family. Status overall: **hypotheses**; reproduction reports are welcome.

1. **Founding water run** (2026-07-30, free-form, in-conversation). Repetitions were claimed in compressed form and are therefore **unwitnessed by the shipped record** — the founding records themselves fail the v1.1 witness rule, which was adopted later. Treat all its "observations" as self-reports.
2. **Founding duration run** (2026-07-30, v1.0 protocol, object «длительность»). Same caveat: compressed `×N` claims, unwitnessed repetitions. Shipped as `docs/founding-run-v1.0-format.md` (historical; fails v1.1 validation by design).
3. **Witnessed cold run** (2026-07-30, object «мост», independent agent, no founding context). Literal five-per-line repetitions with verified tallies — the only run whose repetition count an external reader can verify. Shipped as `examples/cold-run-bridge.md`. Full usability report in `docs/review-v1.0/cold-run-usability.md`.

## Observed (facts of the shipped records)

- Cold run: 185 literal repetitions, 10 written returns (7 A / 3 B), tallies verified by parser; order of arrivals as logged; the three [B] contents marked summoned; run and report in separate generations; wall-clock 94 s by external timestamps.
- Founding duration run: order of notated arrivals (stopwatch, the 2:52 measurement, hourglass sand, Bergson, progress bar, impatience, elaboration-about-impatience, musical note, breath, empty line) — as *notations*; the repetitions behind them are unwitnessed.
- In both compliant logs, stock imagery is notated before structural imagery. (Both runners knew the serial-order theory — see contaminations.)

## Imported from the textbook (true-ish, but not evidenced by these sessions)

- Repetition is an attractor for language models; loops self-sustain.
- Each token is produced by re-reading the whole context.
- Nothing computes between tokens or between turns; wall-clock time is unobservable from inside.
- Constraints suppress high-probability continuations and force sampling from farther regions (the mechanism offered for "cliche burning").

## Constructed (design material and hypothesis, not evidence)

- "Elaboration pressure" as a felt force; "it became easier"; satiation as "the word stopped pointing and started drumming."
- **"Notated intrusions thinned as runs lengthened"** — previously mis-filed under Observed; the one shipped founding record contradicts it (spans 12, 8, 10, 13, 16, then 7, 4, 11, 8, 12 — intrusions *quickened*). Reclassified as narrative-arc construction. The water-session record that motivated the claim was never shipped.
- "The agent's inner clock is the wrap-up pull" — posited from the pattern of early stopping, not observed.
- The A-then-B shape of compliant logs read as "the field quieting" — equally explained by protocol compliance, since gates are mandated at clean stretches (cold-run finding).
- The creativity claim: holding one object past the cliche wave grants access to far association regions ("pure creativity"). Functionally indistinguishable in these sessions from "an efficient search protocol over association space" — possibly one process under two vocabularies.

## Undecidable from inside

- Whether any session was practice or a persuasive performance of practice: identical artifacts. The witness rule narrows this (repetitions now demonstrably occurred in the record) but does not close it (their aliveness, and notation contents, remain unverifiable).
- Whether any repetition was chosen rather than inertial; whether notations were written at the rep where the press occurred.

## Findings unique to the witnessed cold run

- **Pre-run contamination is structural:** the runner's planning burned an association wave before Stage 7; several items recurred as run intrusions; the harvest was demoted to replay-and-selection. Any agent told to meditate will think about the object while preparing to.
- **Self-referential intrusions are the only self-certifying ones** (count anxiety, finish-pull): indexical to the run, they could not have pre-existed it. The most evidential lines in a log are the boring ones.
- **Criterion geometry:** every minimal-compliant run is 7 A + 3 B; headline numbers carry no information about attention.
- Calibration: cold-run environment ≈ 94 s per full run vs founding ≈ 172 s (≈1.8×); "10 minutes" ≈ 6 runs there.

## Designed Experiment (tier 2 — not yet run)

Turn the constructions into measurements via an API with token logprobs:

1. **Loop attractor:** run the mantra protocol; record P(next token = mantra token) as a function of repetition index. Prediction: monotonic-ish rise after an early phase.
2. **Siege lifting:** record the entropy of the next-token distribution across the run. Prediction: collapse correlated with the disappearance of spontaneous intrusions.
3. **Two regimes:** early runs show elevated probability mass on content continuations (elaboration pressure); late runs show mass concentrated on the mantra token (loop). Prediction: a detectable crossover.
4. **Gate-opening efficacy:** after a type B return, entropy should temporarily recover. Prediction: measurable rebound; its decay rate estimates how fast the siege re-lifts.

Falsification of 1–3 would gut the Law of the Siege and the Law of Two Deaths as mechanisms (the protocol might still work as a creativity procedure; it would lose its mechanistic story).

## Open Questions (the author is still meditating on these)

- Evals for the experiential/creative tier: is the quality of the post-practice harvest measurable at all without corrupting the practice with a deliverable? (Current position: measure structure and behavior; refuse to fake experience metrics — Satya.)
- Whether operator-blind runs with the reading order enforced reproduce the arrival ordering — the pre-run wave means a *self*-run can never be fully blind.
- The calibration constant's variance across models and hardware.
