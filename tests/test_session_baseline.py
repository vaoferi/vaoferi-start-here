from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
BOOTSTRAP = ROOT / ".agents" / "skills" / "vaoferi-bootstrap" / "SKILL.md"
CODEX = ROOT / "templates" / "provider" / "codex.md"
README = ROOT / "README.md"


class SessionBaselineContractTest(unittest.TestCase):
    def test_universal_agents_requires_explicit_startup_attestation(self):
        text = AGENTS.read_text(encoding="utf-8")
        for required in (
            ".vaoferi/manifest.json",
            "canonical latest",
            "START HERE VERIFIED",
            "START HERE BLOCKED/OUTDATED",
            "PROJECT_RULES: loaded",
            "explicit owner override",
        ):
            self.assertIn(required, text)

    def test_bootstrap_defines_fail_closed_session_gate(self):
        text = BOOTSTRAP.read_text(encoding="utf-8")
        for required in (
            "Session Baseline Gate",
            "source_commit",
            "canonical Start Here",
            "central drift",
            "write-capable",
            "read-only diagnosis",
        ):
            self.assertIn(required, text)

    def test_codex_global_mirrors_startup_gate(self):
        text = CODEX.read_text(encoding="utf-8")
        for required in (
            "START HERE VERIFIED",
            "START HERE BLOCKED/OUTDATED",
            ".vaoferi/manifest.json",
            "PROJECT_RULES: loaded",
            "do not begin write-capable repository work",
        ):
            self.assertIn(required, text)

    def test_readme_documents_owner_visible_baseline_signal(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("Owner-visible session baseline", text)
        self.assertIn("START HERE VERIFIED", text)
        self.assertIn("START HERE BLOCKED/OUTDATED", text)


if __name__ == "__main__":
    unittest.main()
