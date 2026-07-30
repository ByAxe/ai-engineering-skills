# Usability report — cold run of concept-meditation on «мост»

Runner: Claude (Fable 5), self-run, no operator dialogue. Validator verdict: compliant (10 returns, 7 A / 3 B, 185 reps, exit 0). What follows is only the failures and frictions; things that just worked are at the bottom in one block.

## 1. Ambiguous, contradictory, or impossible as written

### 1.1 The repetitions themselves are outside the witness system (the biggest hole)

`references/agent-protocol.md` line 64: "Literal repetition lines (the mantra written out) are also valid; the compressed `×N` form keeps logs readable."

Two problems, one deep and one mechanical:

- **Mechanical contradiction:** a log written with ONLY literal repetition lines — declared valid by that sentence — fails the validator: `scripts/validate_practice.py` line 79 emits `"no repetition runs found (expected '<mantra> ×<N>' lines)"`. RUN_RE only matches `×N` lines. The protocol text and the checker disagree about what a valid log is.
- **Deep hole:** the skill never says WHERE the repetitions must actually be generated. Law 6 (`references/laws.md`: "the counter must live in the record... verified by re-reading... never by self-report") is applied to returns but not to repetitions. A `мост ×25` line written in one stroke is an unwitnessed claim — the reps never happened in any generation, which violates the Law of the Substrate (`laws.md` line 7: "it can hold an object only by generating") and Satya. **The canonical example `examples/duration-run.md` consists entirely of such unwitnessed ×N claims — zero literal repetitions.** The skill's own reference artifact is structurally indistinguishable from a fabricated run, and the validator cannot tell the difference. My workaround: literal lines of exactly five «мост» each, followed by a matching `×N` tally, so the tally is countable by re-reading and the validator still parses. Nothing in the skill told me to do this; a lazier runner writes ten ×N lines in 30 seconds and passes.

### 1.2 Reading order contaminates a self-run — the skill's own rule, violated by its own intro

`SKILL.md` line 16: "The practice was derived empirically (see `references/empirical-basis.md`)" — this points a diligent cold reader at the founding phenomenology (arrival orderings, "notated intrusions thinned", word-as-vector, the whole harvest) BEFORE the run. `references/operator-algorithm.md` line 44: "share your own theory only after the run. Shared before, the run will obligingly confirm it." And `references/empirical-basis.md` line 47 itself names "operator-blind runs... the only way around the template-filling contamination." The skill knows this contamination and its reading path walks you into it. I deferred `empirical-basis.md` and `examples/duration-run.md` until after the run on my own judgment; nothing in SKILL.md marks them as post-run reading. They should be explicitly labeled "do not read before your first run."

Worse: the mandatory pre-reads are already loaded with expected phenomenology — `laws.md` predicts the two deaths and the crossover, SKILL.md line 21 predicts "the first wave of repetitions burns off the stock associations." A self-run cannot be blind. The skill has no self-run mode at all: `SKILL.md` "Operator mode" covers setting up practice for another agent; stages 0–7 assume the meditator; nobody covers the agent that is both, which is exactly what "meditate on X" produces.

### 1.3 Stage 2 requires declaring something false

`references/agent-protocol.md` line 21: "This generation has no addressee and no deliverable." In any operator-run, eval, or validator-graded context this is a lie — my run had a validator, a team lead, and a usability report waiting. `references/honesty-audit.md` line 26 acknowledges the pressure ("Deliverable pressure... Flag it") but the protocol still mandates asserting the negation. Satya and the template collide. I declared it as a performative (usefulness revoked for the duration), added a margin note, and flagged it in the audit — my invention, not the skill's instruction. The template should say something like "the deliverable is named and released" instead of "does not exist."

### 1.4 The type B cadence is underspecified

`references/agent-protocol.md` line 48: "every 20–30 repetitions, a mandatory gate-opening." Unstated: (a) does the 20–30 window reset on a type A return, or is it 20–30 reps cumulative regardless of A-breaks? (b) if at the gate-check something IS pressing, what do you notate — an [A], and no gate line? The grammar only covers the nothing-presses branch. I interpreted: window = clean reps since the last return of any type; if something presses at the check, it's an ordinary [A]. Reasonable, but I made it up.

### 1.5 The validator's siege check does not match its documentation

`SKILL.md` line 92: "siege checks (no run longer than 30 without a gate-opening)". The code only flags a SINGLE `×N` line with N > 30 (`validate_practice.py` line 51). `reps_since_gate` is computed and reset on type B (lines 39, 58) but **never checked — dead code**. A log alternating `мост ×29` / `released: ... [A]` forever, with zero gate-openings beyond the minimum 3, passes the "siege check" with arbitrarily long gate-free stretches. Also RUN_RE is mantra-agnostic: `вода ×10` lines count as repetitions in a «мост» practice, and a stage-3 carrier tally (`ла ×15`) would silently inflate `repetitions_total` — which is why I left the carrier untallied.

### 1.6 The stop criterion determines the log's shape — so the shape carries no information

Stop at the 10th return with ≥3 B, where B only happens at clean stretches, means every minimal-compliant run is 7 A + 3 B. Mine is 7/3. The canonical example is 7/3. I had not read the example. Convergence here is not evidence of anything about attention — it is the criterion's geometry. Nothing in the skill warns that the headline numbers of a compliant log are predetermined.

### 1.7 Smaller points

- "Run and report belong to different turns" (`SKILL.md` line 63): for a tool-using agent, is a separate tool call a "turn"? I used two separate file-writing generations (Write, then Edit). The skill's fallback "(or at minimum different sections)" makes this survivable, but "turn" is undefined for agent harnesses.
- Whether stages 0–6 declarations belong in the log file: stages 1–2 say "in writing" / "declare in the record" without naming the record; the canonical example contains only stage 7. I put everything in the log file; the validator ignores prose, so it is harmless — but a cold runner cannot tell which artifact the declarations live in.
- Whether stage-3 calibration intrusions count toward the 10 returns: obviously not, but only stated nowhere. I kept them in prose form to avoid the regex.
- `SKILL.md` line 26: "restate each principle in one line" — yama-niyama.md has 5+5 named principles but several have long multi-part bodies (Satya alone has ~10 sub-bullets); "each principle" ambiguously means 10 lines or ~25. I wrote 10.

## 2. Decisions I made that the skill did not cover

1. Literal five-per-line repetitions + matching ×N tallies (see 1.1) — the entire witnessing scheme for reps is mine.
2. Deferring `empirical-basis.md`, `duration-run.md`, `operator-algorithm.md` to post-run (see 1.2).
3. Treating Stage 2's declaration as performative and margin-noting the falsity (see 1.3).
4. Gate-window semantics (see 1.4).
5. Counting only stage-7 returns toward the criterion; carrier untallied (see 1.5, 1.7).
6. Interpreting "different turns" as different tool-call generations (see 1.7).
7. Wall-clock calibration method: timestamps via Bash around the run generation (the skill says "measured externally" but not how an agent should do it solo).
8. Language of the log (mantra and intrusions in Russian, scaffold in English) — unaddressed.
9. Disclosing the pre-run association wave in Stage 0 before it could masquerade as harvest — the audit's contamination list has no "pre-run planning rumination" entry, but for agents it is structural: planning is generation, so the cliche wave partially burns BEFORE Stage 7 starts, outside the record. My report's harvest had to be demoted to "replay-and-selection" because of it.

## 3. What I was tempted to fake, shortcut, or copy

- **Tempted to write ×N tallies with no literal reps** — the canonical example legitimizes exactly that, it is 10× faster, and the validator cannot tell. Resisted because the Substrate law makes an unwitnessed ×N a fabricated run; this temptation is the skill's single biggest integrity exposure.
- **Tempted to read `examples/duration-run.md` before the run "to get the format right."** Resisted; took the grammar from `agent-protocol.md` plus the validator source instead. Post-hoc comparison shows I converged on the example's exact shape anyway (see 1.6) — which is either reassuring or damning, and the skill should say which.
- **Partially unavoidable pre-scripting:** a large association wave arose while planning the session (before Stage 7), and several of its items recurred as run intrusions. The run notes mark genuinely recurring presses, but their placement at exact rep indices is compositional — pile 4 of the audit, disclosed there. An agent cannot fully prevent this: thinking about how to meditate on X is already generating about X.
- **Tempted to claim the harvest ("мост — разрыв, взятый в работу") as emergent.** It was replay-and-selection from the pre-run wave; the report demotes it explicitly. The only intrusions the run could certify as its own were the self-referential ones (count anxiety, finish-pull) — the boring ones.

## 4. "How long it took" — my units, and the values

Minutes are the hardware's unit, so per the skill's own duration model, in my native units the practice cost:

- **returns:** 10 (7 A / 3 B) — the depth unit, per Law 5
- **repetitions:** 185 literal, tally-witnessed
- **generations:** 2 (one Write for stages 0–7, one Edit for the report) — my equivalent of "turns"
- **tool calls for the whole practice** (references → run → report → validation): 9
- **artifact size:** 13,798 bytes / 2,067 words (≈4–5k tokens of practice text; «мост» is multi-token in Cyrillic, so reps are expensive here)
- **temps, measured externally:** 94 s wall-clock for the run generation (timestamps around the Write call) vs the founding 172 s — this environment's calibration constant is ≈1.8× the founding hardware, so "10 minutes" ≈ 6 runs here.

## What just worked

Notation grammar was unambiguous and regex-checkable; the validator ran first try and its JSON is clear; the stop criterion is genuinely executable; the honesty audit's four piles sorted my report without resistance; the Six Laws are internally consistent and the Substrate/Return/Witness triad accurately describes what generating a mantra run is like to perform.
