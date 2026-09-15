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

    def test_bootstrapped_repo_verifies_offline(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            boot = self.run_sync("bootstrap", target)
            self.assertEqual(boot.returncode, 0, boot.stderr)
            verify = subprocess.run(
                [sys.executable, str(target / ".vaoferi" / "verify.py")],
                cwd=target,
                text=True,
                capture_output=True,
            )
            self.assertEqual(verify.returncode, 0, verify.stderr)

    def test_verifier_detects_manifest_hash_drift(self):
        with TemporaryDirectory() as td:
            target = Path(td)
            self.assertEqual(self.run_sync("bootstrap", target).returncode, 0)
            skill = target / ".agents" / "skills" / "vaoferi-engineering" / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\nmanual drift\n", encoding="utf-8")
            verify = subprocess.run(
                [sys.executable, str(target / ".vaoferi" / "verify.py")],
                cwd=target,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(verify.returncode, 0)
            self.assertIn("hash", (verify.stderr + verify.stdout).lower())


if __name__ == "__main__":
    unittest.main()
