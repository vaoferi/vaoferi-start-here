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
            "vaoferi-project-adaptation",
            "Linear",
            "Trello",
        ):
            self.assertIn(required, text)

    def test_owner_profile_preferences_survive_pilot_migration(self):
        text = AGENTS.read_text(encoding="utf-8")
        for required in (
            "80/20",
            "**Рекомендую:**",
            "**Альтернатива:**",
            "**Компроміс:**",
            "18+",
            "шахрай",
        ):
            self.assertIn(required, text)

    def test_trello_is_retired_incrementally_after_parity(self):
        agents = AGENTS.read_text(encoding="utf-8")
        tracking = (ROOT / ".agents" / "skills" / "vaoferi-task-tracking" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("архів", agents.lower())
        self.assertIn("hard-delete", tracking.lower())
        self.assertIn("якщо hard-delete недоступний", tracking.lower())
        self.assertIn("не запускай окремий повний sweep", tracking.lower())
        self.assertIn("Linear", tracking)


if __name__ == "__main__":
    unittest.main()

SKILLS = (
    "vaoferi-bootstrap",
    "vaoferi-engineering",
    "vaoferi-dependencies",
    "vaoferi-security",
    "vaoferi-task-tracking",
    "vaoferi-project-adaptation",
)


class SkillStructureTest(unittest.TestCase):
    def test_required_skills_exist_with_frontmatter(self):
        for name in SKILLS:
            path = ROOT / ".agents" / "skills" / name / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn(f"name: {name}", text)
            self.assertIn("description:", text)

    def test_engineering_preserves_high_value_pilot_rules(self):
        text = (ROOT / ".agents" / "skills" / "vaoferi-engineering" / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "SOLID",
            "не видаляй test",
            "admin/API/БД",
            "powershell.exe",
            "bulk rewrite",
            "явним UTF-8",
            "mojibake",
        ):
            self.assertIn(required, text)

    def test_project_adaptation_has_lossless_lifecycle(self):
        text = (ROOT / ".agents" / "skills" / "vaoferi-project-adaptation" / "SKILL.md").read_text(encoding="utf-8")
        for required in (
            "inventory -> classify -> conflicts -> owner decisions -> migrate -> machine-enforce -> parity -> cleanup -> verify",
            "UNIVERSAL_CORE",
            "UNIVERSAL_CONDITIONAL",
            "DESIGN",
            "PROJECT_SPECIFIC",
            "PROVIDER_OVERLAY",
            "MACHINE_ENFORCEABLE",
            "DUPLICATE",
            "CONFLICT_REQUIRES_REVIEW",
            "DELETE_CANDIDATE",
            "No silent rule loss",
            "Рекомендую",
            "Альтернатива",
            "Компроміс",
            "recursive",
            "history",
        ):
            self.assertIn(required, text)


class ProviderOverlayTest(unittest.TestCase):
    def test_provider_templates_are_thin_overlays(self):
        for name in ("codex", "claude", "gemini"):
            path = ROOT / "templates" / "provider" / f"{name}.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("does not replace `AGENTS.md` or `PROJECT_RULES.md`", text)
            self.assertIn("provider-specific", text)
            self.assertLess(len(text.encode("utf-8")), 3 * 1024)
