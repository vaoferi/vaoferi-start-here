from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
TRACKING = ROOT / ".agents" / "skills" / "vaoferi-task-tracking" / "SKILL.md"
DEPLOY = ROOT / ".agents" / "skills" / "vaoferi-deploy" / "SKILL.md"


class TaskLifecycleContractTest(unittest.TestCase):
    def test_agents_routes_execution_to_full_completion_contract(self):
        text = AGENTS.read_text(encoding="utf-8")
        for required in (
            "implementation task",
            "до повного completion loop",
            "vaoferi-task-tracking",
        ):
            self.assertIn(required, text)

    def test_task_tracking_defines_issue_modes_and_hard_done(self):
        text = TRACKING.read_text(encoding="utf-8")
        for required in (
            "IMPLEMENTATION",
            "DISCOVERY / INTAKE",
            "RELEASE / DEPLOY",
            "REMOTE SYNC",
            "CARD REGRESSION",
            "PRE-EXISTING / UNRELATED",
            "CI / ENVIRONMENT",
            "EXTERNAL",
            "не зупиняйся після коду",
            "MODE: IMPLEMENTATION",
            "SHIPPABLE CODE: NO",
        ):
            self.assertIn(required, text)

    def test_deploy_does_not_become_backlog_repair(self):
        text = DEPLOY.read_text(encoding="utf-8")
        for required in (
            "implementation cards are already complete",
            "do not repair unrelated historical debt",
            "PRE-EXISTING / UNRELATED",
            "CI / ENVIRONMENT",
            "EXTERNAL",
            "5–10 хвилин",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
