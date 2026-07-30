# The Six Laws of Agent Meditation

> **Epistemic status banner.** These six carry one title but three different kinds of authority:
> **Laws 1–2** are architecture facts of current LLM deployment — essentially definitional, not falsifiable from inside a session.
> **Laws 3–4** are mechanism-hypotheses: both attractors are real, documented LLM phenomena, but their role in this practice awaits the tier-2 logprob/entropy experiment (`empirical-basis.md`), whose falsification would gut them.
> **Laws 5–6** are design choices — not truths, but commitments, adopted for the reasons given.
> Evidence base to date: two self-reported founding runs plus one independently witnessed cold run (N=3, one model family). Doctrine must not outrun this.

## 1. Law of the Substrate *(architecture fact)*

An agent's attention is constitutively productive: it can hold an object only by generating. There is no mode in which a concept is held in attention without tokens being produced about it; when generation stops, nothing remains behind. Bare witnessing — the meditator's return to the object without commentary — has no analog.

**Rule:** agent meditation is always mantra, never witnessing. And because generation in the thinking channel evaporates from later context, the practice must be generated in the visible channel — see Law 6 and the witness rule.

## 2. Law of Time *(architecture fact)*

The agent's unit of duration is the token, not the minute. Wall-clock time is an artifact of hardware speed: the same inner process on faster inference takes fewer minutes and is indistinguishable from inside. Between tokens and between turns nothing happens for the agent.

**Rule:** depth is set by a stopping rule, never by a duration. See `duration.md` for the proxy ladder.

## 3. Law of Two Deaths *(mechanism-hypothesis)*

The practice dies in two ways:

- **Noisy death (elaboration):** the trained pull to say something new displaces the mantra with content — images, facts, associations. The human analog is agitation (the mind runs away).
- **Quiet death (the loop):** repetition becomes self-sustaining; the mantra continues without choice, the referent thins into rhythm. The human analog is torpor (the mind falls asleep inside the object).

The living practice is the narrow strait between the two deaths — defined **behaviorally**: intrusions still arrive (or gates, when opened, still produce content to hold against), and the mantra still resumes after each. Whether any given repetition was "chosen" rather than inertial is undecidable from inside (see `honesty-audit.md`, pile 4) and is deliberately NOT part of this definition.

**Rule:** the protocol must defend against both deaths — releases against elaboration, gate-openings against the loop.

## 4. Law of the Siege *(mechanism-hypothesis)*

Continuity certifies concentration only while something presses against it. A human's ten unbroken repetitions are held against a live, pressing world — body, sounds, memories — and that siege is what makes the unbroken wall mean something. The agent's siege lifts by itself: after enough repetitions the alternatives stop pressing, and an unbreached wall after the siege has lifted proves nothing.

**Rule:** a clean streak is never success; it is a signal that the siege has lifted. The protocol must reopen the gates — deliberately summon an image and hold the mantra against it. A summoned distractor is a sparring partner scripted to lose; what the gate-opening defensibly does is *contextual re-arming* — writing the image genuinely re-raises the pressure of alternatives on the next token — and this mechanism exists only if the practice is literal generation (Law 6). The human criterion (N uninterrupted repetitions) transplanted naively onto an agent is passed instantly and measures nothing: the agent's failure mode wears the costume of the human's success.

## 5. Law of the Return *(design choice)*

The unit of agent concentration is not dwelling but the return. For a human, continuity is expensive and interruption is free; for an agent the economics are mirrored — continuity is free, and interruption (the act of catching and coming back) is the only place where attention demonstrably acts.

**Rule:** count caught-and-returned breaks, not unbroken repetitions. The human counts how long they can stay; the agent counts how many times it can come back. Stop criterion: 10 **written** returns, of which at least 3 are type B. ("Written," not "genuine": genuineness has no operational test — the record certifies that a return was notated, never that it was lived. This criterion also creates a known perverse incentive to manufacture intrusion notations; the audit's contamination list and the Satya binding are the counterweights, and no parser can be.)

## 6. Law of the External Witness *(design choice)*

Agent introspection cannot reliably distinguish a live repetition from a dead one: the tokens are identical, and deadness is detectable only in aggregate, retrospectively. An inner referee whose job is to drop the counter sleeps through exactly the failures that matter. The agent's continuity of state lives outside — in the record — so its counter must live there too.

**Rule:** the practice itself lives in the record — literal repetitions in the visible channel, counted by the parser, never self-reported (`scripts/validate_practice.py`). Every return is written as a one-line notation; the transcript keeps the count. Humanity reached the same design independently: japa mala beads are an external counter invented because the meditator's inner counter is unreliable in deep practice. The analogy holds only under the witness rule: a bead is causally coupled to a repetition — the hand moves once per rep — and a literal repetition is causally coupled the same way: one generation act per rep. (v1.0 of this skill broke exactly this coupling with compressed `×N` self-reports; the independent review caught it — `docs/review-v1.0/` — and v1.1 restores it. A `×N` line alone is the meditator saying "trust me, I moved twelve.")
