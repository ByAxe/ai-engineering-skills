from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


BUNDLE = Path(__file__).resolve().parents[1]
FIXTURE = BUNDLE / "tests/fixtures/sample-project"
SCRIPT = BUNDLE / "scripts/scan_java_risks.py"


class ScanJavaRisksTest(unittest.TestCase):
    def run_scan(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE), "--format", "json", *extra],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_detects_high_value_semantic_candidates(self) -> None:
        completed = self.run_scan()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        ids = {finding["rule_id"] for finding in payload["findings"]}

        expected = {
            "EJ-NUM-001",
            "EJ-NULL-002",
            "EJ-TEXT-001",
            "EJ-COL-001",
            "EJ-COL-002",
            "EJ-ERR-004",
            "EJ-TX-001",
            "EJ-REC-001",
            "EJ-REC-002",
            "EJ-QUA-002",
            "EJ-QUA-006",
            "EJ-QUA-008",
            "EJ-CON-003",
            "EJ-CON-006",
        }
        self.assertTrue(expected.issubset(ids), sorted(ids))
        self.assertTrue(payload["project"]["quarkus"])
        self.assertEqual(payload["project"]["java_release"], 21)
        self.assertIn("heuristic candidates", payload["disclaimer"])
        self.assertTrue(all(finding["heuristic"] for finding in payload["findings"]))
        execution = next(
            finding for finding in payload["findings"] if finding["rule_id"] == "EJ-QUA-008"
        )
        self.assertIn("Files.readAllBytes", execution["excerpt"])

    def test_fail_on_is_opt_in(self) -> None:
        advisory = self.run_scan("--min-severity", "high")
        strict = self.run_scan("--min-severity", "high", "--fail-on", "high")
        self.assertEqual(advisory.returncode, 0)
        self.assertEqual(strict.returncode, 1)

    def test_sarif_is_well_formed(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE), "--format", "sarif"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["version"], "2.1.0")
        self.assertEqual(payload["runs"][0]["tool"]["driver"]["name"], "effective-java-risk-scanner")
        self.assertGreater(len(payload["runs"][0]["results"]), 0)


if __name__ == "__main__":
    unittest.main()
