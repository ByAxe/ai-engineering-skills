from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


BUNDLE = Path(__file__).resolve().parents[1]
FIXTURE = BUNDLE / "tests/fixtures/sample-project"
SCRIPT = BUNDLE / "scripts/run_quality_gates.sh"


class QualityGateScriptTest(unittest.TestCase):
    def test_maven_dry_run_is_wrapper_first(self) -> None:
        completed = subprocess.run(
            [str(SCRIPT), "--root", str(FIXTURE), "--mode", "verify", "--dry-run"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertIn(str(FIXTURE / "mvnw"), completed.stdout)
        self.assertIn("verify", completed.stdout)
        self.assertNotIn("fixture mvnw should only appear", completed.stdout)


    def test_gradle_dry_run_is_wrapper_first_and_project_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "build.gradle.kts").write_text('plugins { java }\n', encoding="utf-8")
            wrapper = root / "gradlew"
            wrapper.write_text('#!/usr/bin/env sh\nexit 0\n', encoding="utf-8")
            wrapper.chmod(0o755)
            completed = subprocess.run(
                [
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--mode",
                    "verify",
                    "--project",
                    "service",
                    "--no-daemon",
                    "--dry-run",
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertIn(str(wrapper), completed.stdout)
            self.assertIn("--no-daemon", completed.stdout)
            self.assertIn(":service:check", completed.stdout)

    def test_native_dry_run_is_explicitly_cautious(self) -> None:
        completed = subprocess.run(
            [str(SCRIPT), "--root", str(FIXTURE), "--mode", "native", "--dry-run"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertIn("-Dnative", completed.stdout)
        self.assertIn("verify that this project/version", completed.stderr)


if __name__ == "__main__":
    unittest.main()
