#!/usr/bin/env python3
"""Structural compliance checker for creativity-meditation practice logs (grammar v1.1).

The witness rule: practice exists only as literal repetition lines in the log.
This checker therefore counts repetitions itself (parser-derived, never self-reported),
verifies any `×N` tally against the literal repetitions above it, and enforces:

- returns: at least --returns written returns, at least --type-b of them type B
- interleaving: at least one literal repetition between consecutive returns
- gate window (siege): literal reps since the last return of any type never exceed --max-run
- floor: total literal repetitions at least --min-reps
- run-region purity: between the first literal line and '## Report', only literal lines,
  verified tallies, return notations, and blank lines
- unwitnessed tallies (a `×N` with no literal repetitions behind it) are violations

It does not — and must not — measure experience (Satya). Notation contents remain
self-reports; only the counting is narrative-proof.

Usage:
    python3 validate_practice.py <practice-log.md> [--returns 10] [--type-b 3]
                                 [--max-run 30] [--min-reps 50]

Exit code 0 if compliant, 1 otherwise. Prints a JSON verdict.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TYPE_A_RE = re.compile(r"^\s*released:\s*(?P<content>.+?)\s*\[A\]\s*$", re.IGNORECASE)
TYPE_B_RE = re.compile(
    r"^\s*gates:\s*(?P<content>.+?),\s*held,\s*released\s*\[B\]\s*$", re.IGNORECASE
)
REPORT_RE = re.compile(r"^\s*##\s+Report\b", re.IGNORECASE)
HEADER_RE = re.compile(r"^\s*mantra:\s*(?P<word>\S+)\s*$", re.IGNORECASE)


def _strip_quotes(word: str) -> str:
    return word.strip("«»\"'“”‘’")


def find_mantra(lines: list[str]) -> str | None:
    """Prefer the explicit header; fall back to the first literal run: either a line of
    >=2 identical tokens, or two consecutive lines each being the same single token
    (the one-repetition-per-line form)."""
    prev_single: str | None = None
    for line in lines:
        if REPORT_RE.match(line):
            break
        if m := HEADER_RE.match(line):
            return _strip_quotes(m.group("word"))
    for line in lines:
        if REPORT_RE.match(line):
            break
        tokens = [_strip_quotes(t) for t in line.split()]
        if len(tokens) >= 2 and len(set(tokens)) == 1:
            return tokens[0]
        if len(tokens) == 1:
            if prev_single == tokens[0]:
                return tokens[0]
            prev_single = tokens[0]
        else:
            prev_single = None
    return None


def validate(
    log_path: Path, min_returns: int, min_type_b: int, max_run: int, min_reps: int
) -> dict:
    lines = log_path.read_text(encoding="utf-8").splitlines()
    mantra = find_mantra(lines)

    violations: list[str] = []
    returns_a: list[str] = []
    returns_b: list[str] = []
    total_reps = 0
    reps_since_return = 0
    reps_since_checkpoint = 0  # for tally verification (resets on tally or notation)
    longest_span = 0
    tallies_verified = 0
    in_run = False  # becomes True at the first literal repetition line
    report_line: int | None = None
    siege_flagged_for_span = False

    if mantra is None:
        violations.append(
            "no mantra found: add a 'mantra: <word>' header or literal repetition lines"
        )

    tally_re = (
        re.compile(
            r"^\s*" + re.escape(mantra) + r"\s*[×x]\s*(?P<count>\d+)\s*$", re.IGNORECASE
        )
        if mantra
        else None
    )

    def is_literal(line: str) -> int:
        """Return the number of mantra repetitions if the line is purely literal, else 0."""
        tokens = [_strip_quotes(t) for t in line.split()]
        if tokens and all(t == mantra for t in tokens):
            return len(tokens)
        return 0

    def on_return(bucket: list[str], content: str, lineno: int) -> None:
        nonlocal reps_since_return, reps_since_checkpoint, siege_flagged_for_span
        if in_run and reps_since_return == 0:
            violations.append(
                f"line {lineno}: return with no literal repetitions since the previous "
                "return — nothing to return from (interleaving rule)"
            )
        bucket.append(content)
        reps_since_return = 0
        reps_since_checkpoint = 0
        siege_flagged_for_span = False

    for lineno, line in enumerate(lines, start=1):
        if REPORT_RE.match(line):
            report_line = lineno
            break
        if not line.strip() or HEADER_RE.match(line):
            continue
        if mantra and (n := is_literal(line)):
            in_run = True
            total_reps += n
            reps_since_return += n
            reps_since_checkpoint += n
            longest_span = max(longest_span, reps_since_return)
            if reps_since_return > max_run and not siege_flagged_for_span:
                violations.append(
                    f"line {lineno}: {reps_since_return} literal reps since the last "
                    f"return exceed the gate window of {max_run} (siege check: a "
                    "gate-opening was mandatory)"
                )
                siege_flagged_for_span = True
            continue
        if tally_re and (m := tally_re.match(line)):
            claimed = int(m.group("count"))
            if reps_since_checkpoint == 0:
                violations.append(
                    f"line {lineno}: unwitnessed tally '×{claimed}' — no literal "
                    "repetitions stand behind it (the witness rule: a tally is a "
                    "verified summary, not practice)"
                )
            elif claimed != reps_since_checkpoint:
                violations.append(
                    f"line {lineno}: tally claims ×{claimed} but {reps_since_checkpoint} "
                    "literal reps stand since the previous tally/notation"
                )
            else:
                tallies_verified += 1
            reps_since_checkpoint = 0
            continue
        if m := TYPE_A_RE.match(line):
            on_return(returns_a, m.group("content"), lineno)
            continue
        if m := TYPE_B_RE.match(line):
            on_return(returns_b, m.group("content"), lineno)
            continue
        if in_run:
            violations.append(
                f"line {lineno}: non-practice content inside the run region "
                f"('{line.strip()[:60]}') — analysis and declarations belong above the "
                "first repetition or below '## Report'"
            )

    total_returns = len(returns_a) + len(returns_b)

    if total_returns < min_returns:
        violations.append(
            f"only {total_returns} returns written; criterion requires {min_returns}"
        )
    if len(returns_b) < min_type_b:
        violations.append(
            f"only {len(returns_b)} type B returns; criterion requires {min_type_b} "
            "(a practice without gate-openings cannot distinguish focus from the loop)"
        )
    if total_reps < min_reps:
        violations.append(
            f"only {total_reps} literal repetitions witnessed; floor is {min_reps} "
            "(compressed ×N claims do not count as practice)"
        )
    if report_line is None:
        violations.append(
            "no '## Report' heading: run and report are not separated "
            "(the meditator and the author must be separated)"
        )

    verdict = {
        "log": str(log_path),
        "grammar": "v1.1 (witness rule: literal repetitions only)",
        "compliant": not violations,
        "mantra": mantra,
        "returns_total": total_returns,
        "returns_type_a": len(returns_a),
        "returns_type_b": len(returns_b),
        "repetitions_witnessed": total_reps,
        "tallies_verified": tallies_verified,
        "longest_gate_free_span": longest_span,
        "report_separated": report_line is not None,
        "violations": violations,
        "note": (
            "Structural compliance only. Counting is parser-derived and narrative-proof; "
            "notation contents remain self-reports; experience is not measured. "
            "A clean streak fails; an unwitnessed ×N fails."
        ),
    }
    return verdict


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path, help="practice log (markdown)")
    parser.add_argument("--returns", type=int, default=10, help="minimum total returns")
    parser.add_argument("--type-b", type=int, default=3, help="minimum type B returns")
    parser.add_argument(
        "--max-run", type=int, default=30,
        help="max literal reps between returns (gate window)",
    )
    parser.add_argument(
        "--min-reps", type=int, default=50, help="minimum witnessed literal repetitions"
    )
    args = parser.parse_args()

    if not args.log.exists():
        print(f"error: {args.log} not found", file=sys.stderr)
        return 1

    verdict = validate(args.log, args.returns, args.type_b, args.max_run, args.min_reps)
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    return 0 if verdict["compliant"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
