from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "scripts" / "vaoferi_sync.py"

CENTRAL_URL_ENV = "VAOFERI_START_HERE_CENTRAL_URL"


class CentralFreshnessTest(unittest.TestCase):
    """A locally valid installation must never be reported as central-current.

    An installed manifest can satisfy every offline hash/hygiene check while its
    start_here.source_commit lags trusted central main. Only an explicit central
    comparison may establish CURRENT; missing central evidence is UNKNOWN.
    """

    def run_sync(self, target):
        return subprocess.run(
            [sys.executable, str(SYNC), "bootstrap", "--target", str(target)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def run_verifier(self, target, env=None):
        merged = dict(os.environ)
        merged.pop(CENTRAL_URL_ENV, None)
        if env:
            merged.update(env)
        return subprocess.run(
            [sys.executable, str(target / ".vaoferi" / "verify.py"), "check-central"],
            cwd=target,
            text=True,
            capture_output=True,
            env=merged,
        )

    def run_local_verifier(self, target):
        merged = dict(os.environ)
        merged.pop(CENTRAL_URL_ENV, None)
        return subprocess.run(
            [sys.executable, str(target / ".vaoferi" / "verify.py")],
            cwd=target,
            text=True,
            capture_output=True,
            env=merged,
        )

    def make_central(self, path, marker):
        path.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ)
        env.update(
            {
                "GIT_AUTHOR_NAME": "Central",
                "GIT_AUTHOR_EMAIL": "central@example.invalid",
                "GIT_COMMITTER_NAME": "Central",
                "GIT_COMMITTER_EMAIL": "central@example.invalid",
            }
        )
        subprocess.run(["git", "init", "-q", str(path)], check=True)
        subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], cwd=path, check=True)
        (path / "central.txt").write_text(marker + "\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=path, check=True)
        subprocess.run(["git", "commit", "-q", "-m", marker], cwd=path, check=True, env=env)
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=path, text=True, capture_output=True, check=True
        )
        return head.stdout.strip()

    def set_installed_commit(self, target, commit):
        manifest_path = target / ".vaoferi" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["start_here"]["source_commit"] = commit
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def test_local_pass_never_claims_central_current(self):
        with TemporaryDirectory() as td:
            target = Path(td) / "repo"
            self.assertEqual(self.run_sync(target).returncode, 0)
            local = self.run_local_verifier(target)
            self.assertEqual(local.returncode, 0, local.stderr)
            output = local.stdout + local.stderr
            self.assertNotIn("central drift: none", output)
            self.assertNotIn("START HERE VERIFIED", output)
            self.assertIn("central freshness not established", output)

    def test_installed_matching_central_is_current(self):
        with TemporaryDirectory() as td:
            target = Path(td) / "repo"
            central = Path(td) / "central"
            self.assertEqual(self.run_sync(target).returncode, 0)
            commit = self.make_central(central, "v1")
            self.set_installed_commit(target, commit)
            result = self.run_verifier(target, {CENTRAL_URL_ENV: str(central)})
            output = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, output)
            self.assertIn("CENTRAL STATUS: CURRENT", output)
            self.assertIn(commit, output)

    def test_installed_older_than_central_is_outdated(self):
        with TemporaryDirectory() as td:
            target = Path(td) / "repo"
            central = Path(td) / "central"
            self.assertEqual(self.run_sync(target).returncode, 0)
            stale = self.make_central(central, "stale")
            self.set_installed_commit(target, stale)
            advanced = self.make_central(central, "advanced")
            result = self.run_verifier(target, {CENTRAL_URL_ENV: str(central)})
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CENTRAL STATUS: OUTDATED", output)
            self.assertIn(stale, output)
            self.assertIn(advanced, output)
            self.assertNotIn("CENTRAL STATUS: CURRENT", output)

    def test_unreachable_central_is_unknown_not_current(self):
        with TemporaryDirectory() as td:
            target = Path(td) / "repo"
            self.assertEqual(self.run_sync(target).returncode, 0)
            missing = Path(td) / "does-not-exist"
            result = self.run_verifier(target, {CENTRAL_URL_ENV: str(missing)})
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CENTRAL STATUS: UNKNOWN", output)
            self.assertNotIn("CENTRAL STATUS: CURRENT", output)
            self.assertNotIn("CENTRAL STATUS: OUTDATED", output)

    def test_central_identity_defaults_to_public_canonical_repo(self):
        verifier = (ROOT / "target" / ".vaoferi" / "verify.py").read_text(encoding="utf-8")
        self.assertIn("https://github.com/vaoferi/vaoferi-start-here.git", verifier)


if __name__ == "__main__":
    unittest.main()


