from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "vaoferi-observability" / "SKILL.md"


class ObservabilityDefaultContractTest(unittest.TestCase):
    def test_major_version_and_readme(self):
        version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
        self.assertEqual(version, "4.0.0")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Current release: 4.0.0", readme)
        self.assertIn("vaoferi-observability", readme)

    def test_skill_is_centrally_synced(self):
        sync = (ROOT / "scripts" / "vaoferi_sync.py").read_text(encoding="utf-8")
        self.assertIn('".agents/skills/vaoferi-observability/SKILL.md": ROOT / ".agents/skills/vaoferi-observability/SKILL.md"', sync)
        self.assertTrue(SKILL.is_file())

    def test_default_routed_from_bootstrap_core_and_engineering(self):
        for path in ("AGENTS.md", ".agents/skills/vaoferi-bootstrap/SKILL.md", ".agents/skills/vaoferi-engineering/SKILL.md", "DEFINITION_OF_DONE.md"):
            self.assertIn("vaoferi-observability", (ROOT / path).read_text(encoding="utf-8"), path)

    def test_skill_covers_provider_roles_static_host_and_safe_privacy(self):
        text = SKILL.read_text(encoding="utf-8")
        for term in ("Microsoft Clarity", "PostHog", "Sentry", "static", "NOT_APPLICABLE", "BLOCKED", "consent", "replay", "quota", "dashboard", "ingestion", "canary", "docs/observability/STATUS.md", "PHP", "Never auto deploy"):
            # Case-insensitive for prose style, except the explicit status tokens.
            self.assertIn(term.lower(), text.lower(), term)
        self.assertIn("ONE replay provider", text)
        self.assertIn("No secrets", text)

if __name__ == "__main__":
    unittest.main()
