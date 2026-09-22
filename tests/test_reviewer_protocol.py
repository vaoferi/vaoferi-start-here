from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
TRACKING = ROOT / ".agents" / "skills" / "vaoferi-task-tracking" / "SKILL.md"
ENGINEERING = ROOT / ".agents" / "skills" / "vaoferi-engineering" / "SKILL.md"
CODEX = ROOT / "templates" / "provider" / "codex.md"
REVIEWER_PROMPT = ROOT / "templates" / "reviewer" / "linear-reviewer.md"


class ReviewerProtocolContractTest(unittest.TestCase):
    def test_agents_exposes_compact_executor_reviewer_lifecycle(self):
        text = AGENTS.read_text(encoding="utf-8")
        for required in (
            "Ready for Review",
            "blocked",
            "In Progress",
            "In Review",
            "детальнішим",
            "Definition of Done",
            "мовою користувача",
        ):
            self.assertIn(required, text)

    def test_task_tracking_defines_executor_handoff_and_blocked_first_review(self):
        text = TRACKING.read_text(encoding="utf-8")
        for required in (
            "Executor → Reviewer",
            "Ready for Review",
            "Blocked handoff",
            "BLOCKED ON",
            "WHAT WAS TRIED",
            "what was ruled out",
            "blocked-first",
            "one issue per run",
            "Urgent",
            "oldest waiting first",
            "Linear",
            "GitHub",
            "Opera Browser Connector",
            "Context7",
            "Superpowers",
            "Wayfinder",
            "I have ADHD",
            "topmost user-facing target",
            "Done",
            "In Progress",
        ):
            self.assertIn(required, text)

    def test_engineering_requires_handoff_to_preserve_failures_as_evidence(self):
        text = ENGINEERING.read_text(encoding="utf-8")
        for required in (
            "reviewer handoff",
            "failed attempt",
            "expected outcome",
            "actual outcome",
            "what was ruled out",
        ):
            self.assertIn(required, text)

    def test_codex_mirrors_high_risk_linear_review_rules(self):
        text = CODEX.read_text(encoding="utf-8")
        for required in (
            "Ready for Review",
            "Blocked",
            "In Progress",
            "In Review",
            "executor",
            "reviewer",
        ):
            self.assertIn(required, text)

    def test_canonical_reviewer_prompt_exists_and_is_single_issue_quiet_when_idle(self):
        self.assertTrue(REVIEWER_PROMPT.is_file())
        text = REVIEWER_PROMPT.read_text(encoding="utf-8")
        for required in (
            "one issue per run",
            "blocked-first",
            "no candidate",
            "do not notify",
            "Linear",
            "GitHub",
            "Opera Browser Connector",
            "filesystem",
            "Context7",
            "Superpowers",
            "Wayfinder",
            "I have ADHD",
            "systematic-debugging",
            "verification-before-completion",
            "topmost user-facing target",
            "owner-only",
            "Done",
        ):
            self.assertIn(required, text)

    def test_reviewer_prompt_does_not_auto_delete_linear_history(self):
        text = REVIEWER_PROMPT.read_text(encoding="utf-8")
        self.assertIn("Never auto-delete", text)
        self.assertIn("retention", text.lower())


if __name__ == "__main__":
    unittest.main()
