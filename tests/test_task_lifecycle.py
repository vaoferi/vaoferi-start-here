from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
DEPLOY = ROOT / ".agents" / "skills" / "vaoferi-deploy" / "SKILL.md"


class TaskLifecycleContractTest(unittest.TestCase):
    def test_agents_requires_complete_implementation_before_done(self):
        text = AGENTS.read_text(encoding="utf-8")
        for required in (
            "IMPLEMENTATION",
            "DISCOVERY / INTAKE",
            "RELEASE / DEPLOY",
            "commit + push",
            "REMOTE SYNC",
            "CARD REGRESSION",
            "PRE-EXISTING / UNRELATED",
            "CI / ENVIRONMENT",
            "EXTERNAL",
            "не зупиняйся після коду",
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
