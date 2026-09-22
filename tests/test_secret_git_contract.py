from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
SECURITY = ROOT / ".agents" / "skills" / "vaoferi-security" / "SKILL.md"
TRACKING = ROOT / ".agents" / "skills" / "vaoferi-task-tracking" / "SKILL.md"
CODEX = ROOT / "templates" / "provider" / "codex.md"
REVIEWER = ROOT / "templates" / "reviewer" / "linear-reviewer.md"
SYNC = ROOT / "scripts" / "vaoferi_sync.py"


class SecretAndGitContractTest(unittest.TestCase):
    def test_agents_requires_pushed_sha_before_review_or_done(self):
        text = AGENTS.read_text(encoding="utf-8")
        for required in (
            "commit + push",
            "pushed SHA",
            "In Review",
            "Done",
        ):
            self.assertIn(required, text)

    def test_agents_exposes_two_copy_secret_invariant(self):
        text = AGENTS.read_text(encoding="utf-8")
        for required in (
            "Vaultwarden",
            "project-root `.env`",
            "дві",
        ):
            self.assertIn(required, text)

    def test_security_skill_defines_dual_store_and_discovered_secret_flow(self):
        text = SECURITY.read_text(encoding="utf-8")
        for required in (
            "Vaultwarden",
            "project-root `.env`",
            "working credential",
            "BOTH",
            "Vaultwarden only",
            "не чекати",
            "не echo",
        ):
            self.assertIn(required, text)

    def test_task_tracking_requires_remote_traceability(self):
        text = TRACKING.read_text(encoding="utf-8")
        for required in (
            "commit + push",
            "pushed SHA",
            "remote",
            "In Review",
            "Done",
        ):
            self.assertIn(required, text)

    def test_codex_mirrors_git_and_secret_hard_rules(self):
        text = CODEX.read_text(encoding="utf-8")
        for required in (
            "pushed SHA",
            "Vaultwarden",
            "project-root `.env`",
        ):
            self.assertIn(required, text)

    def test_reviewer_requires_remote_pushed_sha(self):
        text = REVIEWER.read_text(encoding="utf-8")
        for required in ("pushed SHA", "remote", "FAIL"):
            self.assertIn(required, text)

    def test_sync_owns_security_and_tracking_contracts(self):
        text = SYNC.read_text(encoding="utf-8")
        for required in (
            '"AGENTS.md"',
            '".agents/skills/vaoferi-security/SKILL.md"',
            '".agents/skills/vaoferi-task-tracking/SKILL.md"',
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
