from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


BUNDLE = Path(__file__).resolve().parents[1]
SCRIPT = BUNDLE / "scripts/validate_skill.py"


class ValidateSkillTest(unittest.TestCase):
    def test_bundle_passes_standalone_validation(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(BUNDLE), "--json"],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 0, payload)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["errors"], 0)


if __name__ == "__main__":
    unittest.main()
