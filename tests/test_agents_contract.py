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
