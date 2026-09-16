from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "scripts" / "vaoferi_sync.py"


class VerifyTest(unittest.TestCase):
    def run_sync(self, action, target):
        return subprocess.run(
            [sys.executable, str(SYNC), action, "--target", str(target)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def run_verifier(self, target):
        return subprocess.run(
            [sys.executable, str(target / ".vaoferi" / "verify.py")],
            cwd=target,
            text=True,
            capture_output=True,
        )

    def init_git_and_track_all(self, target):
        subprocess.run(["git", "init", "-q"], cwd=target, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=target, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=target, check=True)
        subprocess.run(["git", "add", "-A"], cwd=target, check=True)

    def test_bootstrapped_repo_verifies_offline(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            boot = self.run_sync("bootstrap", target)
            self.assertEqual(boot.returncode, 0, boot.stderr)
            verify = self.run_verifier(target)
            self.assertEqual(verify.returncode, 0, verify.stderr)

    def test_verifier_detects_manifest_hash_drift(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            self.assertEqual(self.run_sync("bootstrap", target).returncode, 0)
            skill = target / ".agents" / "skills" / "vaoferi-engineering" / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\nmanual drift\n", encoding="utf-8")
            verify = self.run_verifier(target)
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("hash", (verify.stderr + verify.stdout).lower())

    def test_tracked_real_env_fails(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            self.assertEqual(self.run_sync("bootstrap", target).returncode, 0)
            (target / ".env").write_text("EXAMPLE=not-a-real-secret\n", encoding="utf-8")
            self.init_git_and_track_all(target)
            verify = self.run_verifier(target)
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("tracked env forbidden", (verify.stderr + verify.stdout).lower())

    def test_env_example_is_allowed(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            self.assertEqual(self.run_sync("bootstrap", target).returncode, 0)
            (target / ".env.example").write_text("EXAMPLE=value\n", encoding="utf-8")
            self.init_git_and_track_all(target)
            verify = self.run_verifier(target)
            self.assertEqual(verify.returncode, 0, verify.stderr)

    def test_named_env_example_is_allowed(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            self.assertEqual(self.run_sync("bootstrap", target).returncode, 0)
            (target / ".env.vault.example").write_text("VAULT_ADDR=https://example.invalid\n", encoding="utf-8")
            self.init_git_and_track_all(target)
            verify = self.run_verifier(target)
            self.assertEqual(verify.returncode, 0, verify.stderr)

    def test_high_confidence_secret_pattern_fails_without_echoing_value(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            self.assertEqual(self.run_sync("bootstrap", target).returncode, 0)
            secret = "AKIAABCDEFGHIJKLMNOP"
            (target / "notes.txt").write_text(f"key={secret}\n", encoding="utf-8")
            self.init_git_and_track_all(target)
            verify = self.run_verifier(target)
            output = verify.stderr + verify.stdout
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("AWS_ACCESS_KEY_ID", output)
            self.assertIn("notes.txt", output)
            self.assertNotIn(secret, output)

    def test_bom_in_centrally_owned_markdown_fails_as_bom(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            self.assertEqual(self.run_sync("bootstrap", target).returncode, 0)
            agents = target / "AGENTS.md"
            agents.write_bytes(b"\xef\xbb\xbf" + agents.read_bytes())
            verify = self.run_verifier(target)
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("bom check failed", (verify.stderr + verify.stdout).lower())


if __name__ == "__main__":
    unittest.main()
