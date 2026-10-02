from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
MEMORY = ROOT / "MEMORY.md"
ENGINEERING = ROOT / ".agents" / "skills" / "vaoferi-engineering" / "SKILL.md"
SECURITY = ROOT / ".agents" / "skills" / "vaoferi-security" / "SKILL.md"
TRACKING = ROOT / ".agents" / "skills" / "vaoferi-task-tracking" / "SKILL.md"
SYNC = ROOT / "scripts" / "vaoferi_sync.py"


class MemoryAndRecoveryContractTest(unittest.TestCase):
    def test_agents_blocks_unexplained_canonical_route_bypass(self):
        text = AGENTS.read_text(encoding="utf-8")
        for required in (
            "canonical route",
            "Hindsight",
            "invalidating condition",
            "MEMORY.md",
        ):
            self.assertIn(required, text)

    def test_memory_contract_is_synced_to_every_participating_repo(self):
        self.assertTrue(MEMORY.is_file())
        text = SYNC.read_text(encoding="utf-8")
        self.assertIn('"MEMORY.md": ROOT / "MEMORY.md"', text)

    def test_memory_is_guardrail_not_source_of_truth(self):
        text = MEMORY.read_text(encoding="utf-8")
        for required in (
            "not a source of truth",
            "coding-agent::{gitProject}",
            '"autoInject": "reflect"',
            '"observationScopes": "shared"',
            '"retainSessions": false',
            "toolGuideExtra",
            "problem signature",
            "do-not-repeat-until",
        ):
            self.assertIn(required, text)

    def test_engineering_requires_root_cause_before_bypass(self):
        text = ENGINEERING.read_text(encoding="utf-8")
        for required in (
            "Canonical-route stop",
            "Hindsight",
            "Linear",
            "smallest experiment",
        ):
            self.assertIn(required, text)

    def test_security_recovers_existing_credentials_before_reasking_owner(self):
        text = SECURITY.read_text(encoding="utf-8")
        for required in (
            "Before asking the owner",
            "Vaultwarden",
            "project-root `.env`",
            "NLM-178",
            "credential names",
        ):
            self.assertIn(required, text)

    def test_linear_overview_activity_and_memory_have_distinct_jobs(self):
        text = TRACKING.read_text(encoding="utf-8")
        for required in ("Project Overview", "Project Updates", "Hindsight", "material correction"):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
