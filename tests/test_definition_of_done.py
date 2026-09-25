from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOD = ROOT / "DEFINITION_OF_DONE.md"
AGENTS = ROOT / "AGENTS.md"
TRACKING = ROOT / ".agents" / "skills" / "vaoferi-task-tracking" / "SKILL.md"
CODEX = ROOT / "templates" / "provider" / "codex.md"
SYNC = ROOT / "scripts" / "vaoferi_sync.py"
CLEAN = ROOT / "target" / ".vaoferi" / "check_worktree_clean.py"


class DefinitionOfDoneContractTest(unittest.TestCase):
    def test_release_is_028_or_newer_contract(self):
        with (ROOT / "pyproject.toml").open("rb") as fh:
            version = tomllib.load(fh)["project"]["version"]
        self.assertEqual(version, "0.2.8")

    def test_universal_contract_requires_zero_dirty_end_state(self):
        text = DOD.read_text(encoding="utf-8")
        for required in (
            "WORKTREE CLEAN",
            "git status --porcelain=v1 --untracked-files=all",
            "pre-existing",
            "In Progress / BLOCKED",
            "нуль незакомічених",
        ):
            self.assertIn(required, text)

    def test_agents_and_tracking_fail_closed_on_dirty_tree(self):
        agents = AGENTS.read_text(encoding="utf-8")
        tracking = TRACKING.read_text(encoding="utf-8")
        codex = CODEX.read_text(encoding="utf-8")
        for text in (agents, tracking, codex):
            self.assertIn("WORKTREE CLEAN", text)
        self.assertIn("pre-existing", agents)
        self.assertIn("DEFINITION_OF_DONE.md", agents)
        self.assertIn("WORKTREE CLEAN: PASS", tracking)

    def test_sync_distributes_dod_and_clean_checker(self):
        text = SYNC.read_text(encoding="utf-8")
        self.assertIn('"DEFINITION_OF_DONE.md"', text)
        self.assertIn('".vaoferi/check_worktree_clean.py"', text)
        self.assertTrue(CLEAN.is_file())

    def test_clean_checker_passes_clean_repo_and_fails_dirty_repo(self):
        self.assertTrue(CLEAN.is_file())
        with TemporaryDirectory() as td:
            repo = Path(td)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            (repo / "tracked.txt").write_text("ok\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "tracked.txt"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "seed"], check=True)

            clean = subprocess.run([sys.executable, str(CLEAN)], cwd=repo, text=True, capture_output=True)
            self.assertEqual(clean.returncode, 0, clean.stderr + clean.stdout)
            self.assertIn("WORKTREE CLEAN: PASS", clean.stdout)

            (repo / "untracked.txt").write_text("dirty\n", encoding="utf-8")
            dirty = subprocess.run([sys.executable, str(CLEAN)], cwd=repo, text=True, capture_output=True)
            self.assertNotEqual(dirty.returncode, 0)
            self.assertIn("WORKTREE CLEAN: FAIL", dirty.stdout)
            self.assertIn("untracked.txt", dirty.stdout)


if __name__ == "__main__":
    unittest.main()
