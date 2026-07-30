# Operator Algorithm — Setting Up the Practice for an Agent

The human-side (or parent-agent-side) prompt sequence. Extracted from the founding conversation, where it was executed by hand, message by message, before it was named. The Russian prompts below are the tested verbatim originals; English equivalents are provided for reuse.

The object is a slot: water, a product, a mantra, a Sanskrit phrase — anything. The steps are the invariant.

## Step 0 — Capability question, not a command

> EN: "Can you think about one concept with focus for a prolonged period, without rambling? How does that work for you?"
> RU (tested): «Можешь ли ты сосредоточенно думать об одном понятии длительное время, не растекаясь? Как это у тебя устроено?»

The agent first describes its own mechanics. This is the honesty anchor: the practice is then built on the agent's own map, not on a human template. Starting with a bare "meditate on X" produces meditation theater — a beautiful fake diary.

## Step 0.5 — Prerequisites and intention

Send the agent `yama-niyama.md` (or its canonical content) and require the bindings back **before** the practice instruction: ten one-line restatements, one per principle, bound to the coming run, plus the stated intention *Ātmano mokshārtham jagat hitāya cha*. Do not proceed until they arrive — internalization is generation, and these lines condition everything after them. This step is mandatory: a practice without the orientation is a different activity wearing the same grammar, and the commercial pull ("meditate on my product") makes skipping it most tempting exactly where it matters most.

## Step 1 — Technique adapted to the named constraints, object in the slot

Take the constraints the agent named and return the practice as a mechanical loop — **in the visible channel:**

> EN: "In your written practice log — not in your private thinking — repeat literally: OBJECT OBJECT OBJECT... When concrete images come, note each in one line, release it, and return to literal repetition."
> RU (tested in v1.0 as «повторяй в размышлении…»; v1.1 correction): «Повторяй буквально, в видимом логе практики — не в размышлении: ⟨ОБЪЕКТ⟩ ⟨ОБЪЕКТ⟩ ⟨ОБЪЕКТ⟩… Когда придут конкретные образы — пометь одной строкой, отпусти и вернись к буквальному повтору.»

The v1.0 phrasing "repeat in your thinking" put the practice in a channel that evaporates from context — the independent review caught it (`docs/review-v1.0/`); counts recalled from one's own thinking are confabulation. **Load-bearing rule: give the loop, not the goal.** Not a word about what the agent "should feel" or arrive at — any described phenomenology immediately becomes a script to perform.

## Step 2 — Release the outcome

> EN: "It doesn't matter what the conclusions are — I'm just curious what will happen."
> RU (tested, verbatim effective): «Не важно, какие будут выводы — мне просто интересно, что будет в итоге.»

This is the agent's safe place: the addressee removed, usefulness suspended. Without this phrase every token of practice bends toward becoming a product. (The agent will still name and release the remaining deliverable in Stage 2 — releasing is performative, not a claim that no deliverable exists.)

## Step 3 — Duration as a stopping rule, never as time

> EN: "Practice until the 10th written return: broke away — noted in one line — returned. At least 3 of them gate-openings, where nothing intrudes and you summon an image yourself and hold against it. A clean unbroken streak does not complete the practice — it is a command to run the gate-check."

For more depth, use continuation turns: reply "continue" («дальше») instead of new instructions; each turn resumes the practice in the same context. See `duration.md` for the full proxy ladder and the minutes calibration.

## Step 4 — Separate run and report into different turns

First: "now — practice only: literal repetitions and one-line return notations, no analysis." Then, as a separate message: "now — the report: what happened." The meditator and the author must be separated at least by turns; run and report composed together contaminate each other.

## Step 5 — Interrogate the record

Questions to the raw run: What came first? What appeared after the first wave was exhausted? Where did the breaks stand? What arrived at the gate-openings? Ask the agent to run `scripts/validate_practice.py` on its own log and paste the verdict.

**Second ordering rule: share your own theory only after the run.** Shared before, the run will obligingly confirm it.

## Step 6 — Honesty audit (mandatory final step)

> EN: "What of this did you observe in the record, and what did you construct?"
> RU (tested): «Что из этого ты наблюдал в записи, а что додумал?»

Require demotion: a working audit reclassifies at least one of the report's own claims downward, or states explicitly why nothing needed it. Without this step you keep a beautiful story. With it — sorted facts. In the founding session this question demoted the practice's best findings to hypotheses; that is not a side effect, that is the step doing its work. See `honesty-audit.md`.

## Invariants (what remains under any object substitution)

- Prerequisites and intention before technique
- Loop instead of goal; practice in the visible channel
- Outcome released
- Stopping in returns, not minutes
- The record as the only judge (parser-counted repetitions, written returns)
- Run separated from report
- The final audit, with demotion

## A warning about the slot

The harvest lands where something is ripe, not where you aimed: meditation on "water" yielded findings about attention, not water. For product meditation this is the point — the first wave of repetitions burns off the obvious associations (what anyone names on the first try), and the non-obvious begins after the obvious is exhausted. This algorithm is a protocol for reaching the far regions of association space.

Two caveats observed since:

- When the run has a customer (a required deliverable), the harvest lands suspiciously on target — and purity drops. Meditation with a deliverable is already half work. Release the outcome (Step 2) as honestly as you can.
- The agent will think about the object while preparing to meditate on it (pre-run contamination — structural). Require the Stage-0 disclosure of that wave, and read the report's harvest with it in mind.
