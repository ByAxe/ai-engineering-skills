from __future__ import annotations

import json
import os
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path


BUNDLE = Path(__file__).resolve().parents[1]
FIXTURE = BUNDLE / "tests/fixtures/sample-project"
SCRIPT = BUNDLE / "scripts/profile_java_project.py"


class ProfileJavaProjectTest(unittest.TestCase):
    def test_profiles_maven_java_and_quarkus_metadata(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE), "--format", "json"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        profile = json.loads(completed.stdout)

        self.assertEqual(profile["build_systems"], ["maven"])
        self.assertIn("mvnw", profile["wrappers"])
        self.assertIn("maven.compiler.release=21", profile["java"]["release_candidates"])
        self.assertTrue(profile["quarkus"]["detected"])
        self.assertTrue(
            any("quarkus.platform.version=3.15.3" in value for value in profile["quarkus"]["version_candidates"])
        )
        self.assertIn(
            "io.quarkus:quarkus-rest-jackson", profile["quarkus"]["extensions"]
        )
        self.assertIn("Spotless", profile["quality_tools"])
        self.assertGreaterEqual(profile["source_counts"]["java_main"], 1)
        self.assertGreaterEqual(profile["source_counts"]["java_test"], 1)
        self.assertIn("src/main/resources/application.properties", profile["config_files"])


    def test_profiles_gradle_kotlin_dsl_toolchain_and_quarkus(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "settings.gradle.kts").write_text(
                'rootProject.name = "fixture"\ninclude(":service")\n',
                encoding="utf-8",
            )
            (root / "build.gradle.kts").write_text(
                'plugins {\n'
                '  java\n'
                '  id("io.quarkus") version "3.15.3"\n'
                '  id("com.diffplug.spotless") version "6.25.0"\n'
                '}\n'
                'java { toolchain { languageVersion.set(JavaLanguageVersion.of(21)) } }\n'
                'dependencies {\n'
                '  implementation(enforcedPlatform("io.quarkus.platform:quarkus-bom:3.15.3"))\n'
                '  implementation("io.quarkus:quarkus-rest-jackson")\n'
                '}\n',
                encoding="utf-8",
            )
            wrapper = root / "gradlew"
            wrapper.write_text('#!/usr/bin/env sh\nexit 0\n', encoding="utf-8")
            wrapper.chmod(0o755)

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(root), "--format", "json"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            profile = json.loads(completed.stdout)
            self.assertEqual(profile["build_systems"], ["gradle"])
            self.assertIn("gradlew", profile["wrappers"])
            self.assertIn("languageVersion=21", profile["java"]["release_candidates"])
            self.assertIn("service", profile["modules"])
            self.assertTrue(profile["quarkus"]["detected"])
            self.assertIn("io.quarkus:quarkus-rest-jackson", profile["quarkus"]["extensions"])
            self.assertIn("Spotless", profile["quality_tools"])

    def test_markdown_labels_candidates_as_static_evidence(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE), "--format", "markdown"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertIn("# Java Project Profile", completed.stdout)
        self.assertIn("Confirm effective Maven/Gradle configuration", completed.stdout)


if __name__ == "__main__":
    unittest.main()
