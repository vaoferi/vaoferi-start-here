"""Contract tests for the estate-level macOS metadata hygiene check.

A Mac that edits canonical NAS source over the WebDAV mount leaves AppleDouble
`._*` siblings next to every written file. Those siblings are visible to Git as
untracked noise and therefore break the zero-dirty completion gate in every
repository, not just one. The check below is the deterministic way to prove the
estate is free of them, and that the remedy (an ignore rule) actually works.
"""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check_macos_metadata.py"


def run_check(*repo_roots):
    return subprocess.run(
        [sys.executable, str(CHECK), *[str(p) for p in repo_roots]],
        capture_output=True,
        text=True,
    )


def init_repo(home):
    repo = Path(home) / "repo"
    repo.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
    (repo / "index.ts").write_text("export const a = 1;\n", encoding="utf-8")
    (repo / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "seed"], check=True)
    return repo


class MacOSMetadataHygieneTest(unittest.TestCase):
    def test_checker_exists(self):
        self.assertTrue(CHECK.is_file(), f"{CHECK.name} is missing from the canonical repo")

    def test_clean_repository_passes(self):
        with tempfile.TemporaryDirectory() as home:
            repo = init_repo(home)
            result = run_check(repo)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("MACOS METADATA: PASS", result.stdout)

    def test_untracked_appledouble_sibling_is_reported_by_exact_path(self):
        with tempfile.TemporaryDirectory() as home:
            repo = init_repo(home)
            (repo / "._index.ts").write_bytes(b"\x00\x05\x16\x07 mac metadata")
            result = run_check(repo)
            self.assertNotEqual(result.returncode, 0, "an AppleDouble sibling must block")
            self.assertIn("._index.ts", result.stdout)

    def test_ignore_rule_is_a_real_remedy(self):
        with tempfile.TemporaryDirectory() as home:
            repo = init_repo(home)
            (repo / ".gitignore").write_text("node_modules/\n._*\n", encoding="utf-8")
            (repo / "._index.ts").write_bytes(b"\x00\x05\x16\x07 mac metadata")
            result = run_check(repo)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("MACOS METADATA: PASS", result.stdout)

    def test_tracked_file_that_looks_like_metadata_is_not_invented_as_a_violation(self):
        with tempfile.TemporaryDirectory() as home:
            repo = init_repo(home)
            (repo / "_doc.md").write_text("# kept\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "keep"], check=True)
            result = run_check(repo)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_several_repos_are_audited_in_one_run_and_the_bad_one_is_named(self):
        with tempfile.TemporaryDirectory() as home:
            roots = []
            for name in ("alpha", "beta"):
                repo = Path(home) / name
                repo.mkdir()
                subprocess.run(["git", "init", "-q", str(repo)], check=True)
                ignore = "node_modules/\n._*\n" if name == "alpha" else "node_modules/\n"
                (repo / ".gitignore").write_text(ignore, encoding="utf-8")
                (repo / "index.ts").write_text("export const a = 1;\n", encoding="utf-8")
                subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
                subprocess.run(
                    ["git", "-C", str(repo), "-c", "user.email=t@example.invalid",
                     "-c", "user.name=Test", "commit", "-qm", "seed"],
                    check=True,
                )
                roots.append(repo)
            for repo in roots:
                (repo / "._index.ts").write_bytes(b"\x00\x05\x16\x07 mac metadata")
            result = run_check(*roots)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("._index.ts", result.stdout)
            self.assertIn("beta", result.stdout)
            self.assertNotIn("alpha: BLOCKED", result.stdout)

    def test_canonical_repository_ignores_appledouble_itself(self):
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertTrue(
            any(line.strip() == "._*" for line in text.splitlines()),
            "the canonical Start Here repo must ignore macOS AppleDouble siblings",
        )


if __name__ == "__main__":
    unittest.main()
