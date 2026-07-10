from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


BUNDLE = Path(__file__).resolve().parents[1]
SCRIPT = BUNDLE / "scripts/check_diff_scope.py"


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class CheckDiffScopeTest(unittest.TestCase):
    def test_reports_mixed_scope_deleted_tests_generated_output_and_secret(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "src/main/java/acme").mkdir(parents=True)
            (repo / "src/test/java/acme").mkdir(parents=True)
            (repo / "pom.xml").write_text("<project/>\n", encoding="utf-8")
            source = repo / "src/main/java/acme/App.java"
            source.write_text("package acme;\nfinal class App {}\n", encoding="utf-8")
            test = repo / "src/test/java/acme/AppTest.java"
            test.write_text("package acme;\nfinal class AppTest {}\n", encoding="utf-8")

            git(repo, "init", "-q")
            git(repo, "config", "user.name", "Effective Java Test")
            git(repo, "config", "user.email", "effective-java@example.invalid")
            git(repo, "add", ".")
            git(repo, "commit", "-qm", "baseline")

            (repo / "pom.xml").write_text("<project><version>2</version></project>\n", encoding="utf-8")
            source.write_text(
                "package acme;\n"
                "public class App {\n"
                "  public String newApi() { System.out.println(\"debug\"); return \"ok\"; }\n"
                "}\n",
                encoding="utf-8",
            )
            untracked_source = repo / "src/main/java/acme/NewToken.java"
            untracked_source.write_text(
                "package acme;\n"
                "public final class NewToken {\n"
                "  private static final String API_KEY = \"untracked-fixture-secret\";\n"
                "}\n",
                encoding="utf-8",
            )
            test.unlink()
            generated = repo / "target/generated-sources/acme/Generated.java"
            generated.parent.mkdir(parents=True)
            generated.write_text("package acme; final class Generated {}\n", encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(repo), "--format", "json"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            payload = json.loads(completed.stdout)
            codes = {candidate["code"] for candidate in payload["candidates"]}
            expected = {
                "DIFF-GENERATED",
                "DIFF-TEST-DELETION",
                "DIFF-BUILD-AND-CODE",
                "DIFF-PUBLIC-API",
                "DIFF-POSSIBLE-SECRET",
                "DIFF-DEBUG-OUTPUT",
            }
            self.assertTrue(expected.issubset(codes), sorted(codes))
            secret = next(
                candidate
                for candidate in payload["candidates"]
                if candidate["code"] == "DIFF-POSSIBLE-SECRET"
            )
            self.assertIn("src/main/java/acme/NewToken.java", secret["paths"])
            self.assertTrue(payload["advisory"])

            strict = subprocess.run(
                [sys.executable, str(SCRIPT), str(repo), "--strict"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(strict.returncode, 1)


if __name__ == "__main__":
    unittest.main()
