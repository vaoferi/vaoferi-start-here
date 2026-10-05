from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "scripts" / "vaoferi_sync.py"
DESIGN_LOCK = ROOT / "vendor" / "design-skill.lock.json"
SYNC_SPEC = importlib.util.spec_from_file_location("vaoferi_sync", SYNC)
SYNC_MODULE = importlib.util.module_from_spec(SYNC_SPEC)
SYNC_SPEC.loader.exec_module(SYNC_MODULE)


class SyncTest(unittest.TestCase):
    def run_sync(self, action, target, env=None):
        merged = dict(os.environ)
        merged.pop("VAOFERI_START_HERE_CENTRAL_URL", None)
        if env:
            merged.update(env)
        return subprocess.run(
            [sys.executable, str(SYNC), action, "--target", str(target)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            env=merged,
        )

    def test_sync_exposes_explicit_central_freshness_action(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            self.assertEqual(self.run_sync("bootstrap", target).returncode, 0)
            unreachable = target / "no-such-remote"
            result = self.run_sync(
                "check-central",
                target,
                {"VAOFERI_START_HERE_CENTRAL_URL": str(unreachable)},
            )
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CENTRAL STATUS: UNKNOWN", output)
            self.assertNotIn("Central freshness verified", output)

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

            adaptation = target / ".agents" / "skills" / "vaoferi-project-adaptation" / "SKILL.md"
            self.assertTrue(adaptation.is_file())
            self.assertIn(
                ".agents/skills/vaoferi-project-adaptation/SKILL.md",
                manifest["owned_files"],
            )

            runtime_preview = target / ".agents" / "skills" / "vaoferi-runtime-preview" / "SKILL.md"
            self.assertTrue(runtime_preview.is_file())
            self.assertIn(
                ".agents/skills/vaoferi-runtime-preview/SKILL.md",
                manifest["owned_files"],
            )
            runtime_text = runtime_preview.read_text(encoding="utf-8")
            self.assertIn("RECOVERY MODE", runtime_text)
            self.assertIn("Acceptance frontier", runtime_text)
            self.assertIn("Control-plane identity", runtime_text)

            dod = target / "DEFINITION_OF_DONE.md"
            clean_gate = target / ".vaoferi" / "check_worktree_clean.py"
            self.assertTrue(dod.is_file())
            self.assertTrue(clean_gate.is_file())
            self.assertIn("DEFINITION_OF_DONE.md", manifest["owned_files"])
            self.assertIn(".vaoferi/check_worktree_clean.py", manifest["owned_files"])

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

    def test_update_copies_committed_blob_bytes_not_transformed_checkout_bytes(self):
        with TemporaryDirectory() as td:
            source_repo = Path(td) / "source"
            target = Path(td) / "target"
            source_repo.mkdir()
            subprocess.run(["git", "init", "-q", str(source_repo)], check=True)
            subprocess.run(["git", "-C", str(source_repo), "config", "user.name", "Sync Test"], check=True)
            subprocess.run(["git", "-C", str(source_repo), "config", "user.email", "sync-test@example.invalid"], check=True)
            (source_repo / ".gitattributes").write_text("*.md text eol=lf\n", encoding="utf-8")
            source = source_repo / "AGENTS.md"
            committed = b"first line\n\n"
            source.write_bytes(committed)
            subprocess.run(["git", "-C", str(source_repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(source_repo), "commit", "-qm", "fixture"], check=True)

            # Simulate checkout bytes that differ from the pinned Git revision.
            source.write_bytes(b"first line\n\r\n")

            SYNC_MODULE.copy_owned(
                target,
                previous_owned=None,
                sources={"AGENTS.md": source},
                source_root=source_repo,
                source_revision="HEAD",
            )
            self.assertEqual((target / "AGENTS.md").read_bytes(), committed)


if __name__ == "__main__":
    unittest.main()

