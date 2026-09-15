from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"


class AgentsContractTest(unittest.TestCase):
    def test_agents_is_small_and_universal(self):
        data = AGENTS.read_bytes()
        self.assertLessEqual(len(data), 12 * 1024)
        text = data.decode("utf-8")
        for forbidden in (
            "nlm.help",
            "admin.nlm.help",
            "storage.nlm.help",
            "BodyRes",
            "Miami Vero",
            "\\\\NAS\\",
            "18083",
        ):
            self.assertNotIn(forbidden, text)

    def test_agents_routes_specialized_work(self):
        text = AGENTS.read_text(encoding="utf-8")
        for required in (
            "PROJECT_RULES.md",
            "vaoferi-design-skill",
            "vaoferi-security",
            "vaoferi-dependencies",
            "Linear",
            "Trello",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()

SKILLS = (
    "vaoferi-bootstrap",
    "vaoferi-engineering",
    "vaoferi-dependencies",
    "vaoferi-security",
    "vaoferi-task-tracking",
)


class SkillStructureTest(unittest.TestCase):
    def test_required_skills_exist_with_frontmatter(self):
        for name in SKILLS:
            path = ROOT / ".agents" / "skills" / name / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"name: {name}", text)
            self.assertIn("description:", text)


class ProviderOverlayTest(unittest.TestCase):
    def test_provider_templates_are_thin_overlays(self):
        for name in ("codex", "claude", "gemini"):
            path = ROOT / "templates" / "provider" / f"{name}.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("does not replace `AGENTS.md` or `PROJECT_RULES.md`", text)
            self.assertIn("provider-specific", text)
            self.assertLess(len(text.encode("utf-8")), 3 * 1024)
