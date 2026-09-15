from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "scripts" / "vaoferi_sync.py"
DESIGN_LOCK = ROOT / "vendor" / "design-skill.lock.json"


class SyncTest(unittest.TestCase):
    def run_sync(self, action, target):
        return subprocess.run(
            [sys.executable, str(SYNC), action, "--target", str(target)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_bootstrap_preserves_project_rules_and_is_idempotent(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            project_rules = target / "PROJECT_RULES.md"
            project_rules.write_text("PROJECT ONLY\n", encoding="utf-8")
            first = self.run_sync("bootstrap", target)
            self.assertEqual(first.returncode, 0, first.stderr)
            first_agents = (target / "AGENTS.md").read_bytes()
            first_manifest = (target / ".vaoferi" / "manifest.json").read_bytes()
            second = self.run_sync("update", target)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first_agents, (target / "AGENTS.md").read_bytes())
            self.assertEqual(first_manifest, (target / ".vaoferi" / "manifest.json").read_bytes())
            self.assertEqual(project_rules.read_text(encoding="utf-8"), "PROJECT ONLY\n")
            manifest = json.loads((target / ".vaoferi" / "manifest.json").read_text())
            self.assertEqual(manifest["schema"], 1)

            design_lock = json.loads(DESIGN_LOCK.read_text(encoding="utf-8"))
            for rel, expected in design_lock["files_sha256"].items():
                installed = target / ".agents" / "skills" / "vaoferi-design-skill" / rel
                self.assertTrue(installed.is_file(), rel)
                actual = hashlib.sha256(installed.read_bytes()).hexdigest()
                self.assertEqual(actual, expected, rel)

    def test_update_fails_closed_on_manual_universal_edit(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            self.assertEqual(self.run_sync("bootstrap", target).returncode, 0)
            (target / "AGENTS.md").write_text("manual drift\n", encoding="utf-8")
            result = self.run_sync("update", target)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("drift", (result.stderr + result.stdout).lower())

    def test_bootstrap_refuses_unmanaged_conflict(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            (target / "AGENTS.md").write_text("old local rules\n", encoding="utf-8")
            result = self.run_sync("bootstrap", target)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("conflict", (result.stderr + result.stdout).lower())


if __name__ == "__main__":
    unittest.main()
