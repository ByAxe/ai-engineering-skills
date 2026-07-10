from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


BUNDLE = Path(__file__).resolve().parents[1]
SCRIPT = BUNDLE / "migration/replace-legacy-skills.sh"


class MigrationTest(unittest.TestCase):
    def test_dry_run_and_apply_replace_only_legacy_java_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "skills/java-refactoring").mkdir(parents=True)
            (repo / "skills/java-21-refactor-assessor").mkdir(parents=True)
            (repo / "skills/other-skill").mkdir(parents=True)
            (repo / "skills/java-refactoring/SKILL.md").write_text("legacy\n", encoding="utf-8")
            (repo / "skills/java-21-refactor-assessor/SKILL.md").write_text("legacy\n", encoding="utf-8")
            (repo / "skills/other-skill/SKILL.md").write_text("keep\n", encoding="utf-8")
            (repo / "README.md").write_text(
                "# Skills\n\n"
                "### Java\n\n"
                "| Skill | Description |\n"
                "|---|---|\n"
                "| **java-refactoring** | old |\n"
                "| **java-21-refactor-assessor** | old |\n"
                "| **other-skill** | keep |\n\n"
                "## Structure\n\n"
                "```\n"
                "skills/\n"
                "│ # Java\n"
                "├── java-refactoring/\n"
                "│   ├── SKILL.md\n"
                "│   └── references/\n"
                "│       └── old.md\n"
                "├── java-21-refactor-assessor/\n"
                "│   ├── SKILL.md\n"
                "│   └── references/\n"
                "│       └── java-21-best-practices.md\n"
                "│\n"
                "│ # Kotlin / JVM\n"
                "├── other-skill/\n"
                "```\n\n"
                "To update one skill:\n\n"
                "```bash\n"
                "npx skills add example/repo --skill java-refactoring\n"
                "```\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Effective Java Test"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "effective-java@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "baseline"], check=True)

            dry = subprocess.run(
                [str(SCRIPT), "--repo", str(repo)],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertIn("Dry-run only", dry.stdout)
            self.assertFalse((repo / "skills/effective-java").exists())

            applied = subprocess.run(
                [str(SCRIPT), "--repo", str(repo), "--apply"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            self.assertTrue((repo / "skills/effective-java/SKILL.md").is_file())
            self.assertFalse((repo / "skills/java-refactoring").exists())
            self.assertFalse((repo / "skills/java-21-refactor-assessor").exists())
            self.assertTrue((repo / "skills/other-skill/SKILL.md").is_file())
            readme = (repo / "README.md").read_text(encoding="utf-8")
            self.assertEqual(readme.count("| **effective-java** |"), 1)
            self.assertEqual(readme.count("├── effective-java/"), 1)
            self.assertIn("--skill effective-java", readme)
            self.assertNotIn("old.md", readme)
            self.assertNotIn("java-21-best-practices.md", readme)
            self.assertNotIn("java-refactoring", readme)
            self.assertNotIn("java-21-refactor-assessor", readme)
            backups = list((repo / ".effective-java-migration-backup").glob("*"))
            self.assertEqual(len(backups), 1)


if __name__ == "__main__":
    unittest.main()
