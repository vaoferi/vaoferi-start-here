from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RuntimePreviewContractTest(unittest.TestCase):
    def test_runtime_preview_contract_is_wired(self):
        with (ROOT / "pyproject.toml").open("rb") as fh:
            self.assertEqual(tomllib.load(fh)["project"]["version"], "0.3.0")

        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        dod = (ROOT / "DEFINITION_OF_DONE.md").read_text(encoding="utf-8")
        tracking = (ROOT / ".agents/skills/vaoferi-task-tracking/SKILL.md").read_text(encoding="utf-8")
        runtime = (ROOT / ".agents/skills/vaoferi-runtime-preview/SKILL.md").read_text(encoding="utf-8")
        codex = (ROOT / "templates/provider/codex.md").read_text(encoding="utf-8")

        self.assertIn("vaoferi-runtime-preview", agents)
        self.assertIn("RECOVERY MODE", dod)
        self.assertIn("Acceptance frontier", tracking)
        self.assertIn("Acceptance frontier", runtime)
        self.assertIn("Control-plane identity", runtime)
        self.assertIn("two consecutive iterations", runtime)
        self.assertIn("RECOVERY MODE", codex)


if __name__ == "__main__":
    unittest.main()
