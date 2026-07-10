from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


BUNDLE = Path(__file__).resolve().parents[1]
SOURCE = BUNDLE / "tests/fixtures/java-compile/ValueContracts.java"


class JavaFixtureTest(unittest.TestCase):
    def test_java_21_contract_fixture_compiles_and_runs(self) -> None:
        javac = shutil.which("javac")
        java = shutil.which("java")
        if not javac or not java:
            self.skipTest("JDK tools are unavailable")
        version = subprocess.run(
            [javac, "-version"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        ).stdout
        match = re.search(r"javac\s+(\d+)", version)
        if not match or int(match.group(1)) < 21:
            self.skipTest(f"Java 21+ required, found {version.strip()}")

        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [javac, "--release", "21", "-d", tmp, str(SOURCE)],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            completed = subprocess.run(
                [java, "-ea", "-cp", tmp, "ValueContracts"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
