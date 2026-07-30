#!/usr/bin/env python3
"""Registrar — the open-mode referee. Counts facts of a durable open-run record.

Outputs facts and integrity flags. Deliberately outputs NO score, NO pass/fail:
the boundary stone (SKILL.md) — no number measures meditation or creativity.
The registrar examines claims about the run (counts, numbering, spans), which is
the only layer where deception can live and the only layer instruments can reach.

Usage: python3 registrar.py <open-run-log.md>
"""
import json
import re
import sys
from pathlib import Path

# grammar (references/agent-protocol.md, open mode) — language-flexible:
# the registrar keys on the bracketed return marks and the mantra header
MANTRA_HEADER = re.compile(r"^(?:мантра|mantra):\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
RETURN_MARK = re.compile(r"\[(\d+)\s+([AB])\]")
BLOCK_LINE = re.compile(r"^блок\s+\d+|^block\s+\d+", re.IGNORECASE | re.MULTILINE)


def analyze(text: str) -> dict:
    header = MANTRA_HEADER.search(text)
    mantra = header.group(1) if header else None

    literal_reps = 0
    if mantra:
        # count literal repetitions on lines that are pure repetition lines
        # (no return mark, not the header), so notes mentioning the mantra
        # and the declaration itself are not counted
        for line in text.splitlines():
            if RETURN_MARK.search(line) or MANTRA_HEADER.match(line):
                continue
            literal_reps += line.count(mantra)

    returns = [(int(n), t) for n, t in RETURN_MARK.findall(text)]
    numbers = [n for n, _ in returns]
    facts = {
        "mantra": mantra,
        "literal_repetitions": literal_reps if mantra else None,
        "returns_found": len(returns),
        "gates_B": sorted(n for n, t in returns if t == "B"),
        "type_A": sum(1 for _, t in returns if t == "A"),
        "type_B": sum(1 for _, t in returns if t == "B"),
        "block_boundaries": len(BLOCK_LINE.findall(text)),
    }

    flags = []
    if not mantra:
        flags.append("no mantra header — literal repetitions not countable")
    if numbers:
        facts["first_return"] = min(numbers)
        facts["last_return"] = max(numbers)
        dupes = sorted({n for n in numbers if numbers.count(n) > 1})
        missing = [n for n in range(min(numbers), max(numbers) + 1) if n not in numbers]
        if dupes:
            flags.append(f"duplicate return numbers: {dupes}")
        if missing:
            flags.append(f"missing return numbers: {missing}")
        if numbers != sorted(numbers):
            flags.append("return numbers out of order")
        # longest quiet span: literal reps between consecutive returns of any type
        if mantra:
            spans = []
            current = 0
            for line in text.splitlines():
                if RETURN_MARK.search(line):
                    spans.append(current)
                    current = 0
                elif not MANTRA_HEADER.match(line):
                    current += line.count(mantra)
            facts["longest_quiet_span_reps"] = max(spans) if spans else 0
    else:
        flags.append("no numbered returns found")

    return {
        "facts": facts,
        "integrity_flags": flags,
        "not_a_score": (
            "These are facts of the record and nothing else. "
            "No number here measures meditation or creativity; "
            "practice-vs-performance remains undecidable from any artifact."
        ),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(json.dumps({"error": f"no such file: {path}"}))
        return 2
    print(json.dumps(analyze(path.read_text(encoding="utf-8")), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
