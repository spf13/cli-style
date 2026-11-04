"""Tests for check_invariants.py: each mutates a temp copy of the repo and expects a failure."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COPY = ["README.md", "CHANGELOG.md", ".claude-plugin", "cli-style", ".github/scripts"]


class CheckInvariantsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        for name in COPY:
            source, target = ROOT / name, self.tmp / name
            if source.is_dir():
                shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy2(source, target)

    def edit(self, name: str, old: str, new: str) -> None:
        path = self.tmp / name
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"fixture text missing from {name}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def run_check(self) -> subprocess.CompletedProcess[str]:
        script = self.tmp / ".github" / "scripts" / "check_invariants.py"
        return subprocess.run([sys.executable, script], capture_output=True, text=True, check=False)

    def assert_fails(self, message: str) -> None:
        result = self.run_check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stderr)

    def test_clean_repo_passes(self) -> None:
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("invariants hold", result.stdout)

    def test_non_canonical_anchor(self) -> None:
        self.edit("cli-style/SKILL.md", "(`#idempotent-or-refuse`)", "(`#be-idempotent`)")
        self.assert_fails("principle 19 anchor is #be-idempotent; cli.style uses #idempotent-or-refuse")

    def test_swapped_anchors(self) -> None:
        self.edit("cli-style/SKILL.md", "(`#long-flags-first`)", "(`#TMP`)")
        self.edit("cli-style/SKILL.md", "(`#run-without-config`)", "(`#long-flags-first`)")
        self.edit("cli-style/SKILL.md", "(`#TMP`)", "(`#run-without-config`)")
        self.assert_fails("principle 10 anchor is #run-without-config")

    def test_missing_principle(self) -> None:
        skill = self.tmp / "cli-style" / "SKILL.md"
        text = re.sub(r"^37\. \*\*.*\n.*\n", "", skill.read_text(encoding="utf-8"), count=1, flags=re.M)
        skill.write_text(text, encoding="utf-8")
        self.assert_fails("expected numbered principles 1..56")

    def test_divergent_set_drift(self) -> None:
        self.edit("cli-style/SKILL.md", "Detect the terminal; never assume one. ⚡ Divergent**", "Detect the terminal; never assume one.**")
        self.assert_fails("⚡ Divergent principles are [32, 33, 40]")

    def test_metadata_version_drift(self) -> None:
        self.edit("cli-style/SKILL.md", 'version: "1.', 'version: "0.')
        self.assert_fails("SKILL.md metadata.version")

    def test_metadata_category_drift(self) -> None:
        self.edit("cli-style/SKILL.md", "category: development", "category: coding")
        self.assert_fails("SKILL.md metadata.category 'coding'")

    def test_description_too_long(self) -> None:
        self.edit("cli-style/SKILL.md", "description: >\n", "description: >\n  " + "x" * 1024 + "\n")
        self.assert_fails("must be 40..1024")

    def test_marketplace_tags_drift(self) -> None:
        self.edit(".claude-plugin/marketplace.json", '"ux"]', '"ux", "extra"]')
        self.assert_fails("!= plugin.json keywords")

    def test_missing_changelog_entry(self) -> None:
        self.edit("CHANGELOG.md", "## [1.", "## [0.")
        self.assert_fails("CHANGELOG.md has no")

    def test_readme_table_missing_skill(self) -> None:
        self.edit("README.md", "[`cli-style`](./cli-style/SKILL.md)", "`cli-style`")
        self.assert_fails("README skills table must list every skill exactly once")


if __name__ == "__main__":
    unittest.main()
