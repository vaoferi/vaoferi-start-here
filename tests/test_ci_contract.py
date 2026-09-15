from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "vaoferi-checks.yml"


class CiContractTest(unittest.TestCase):
    def test_reusable_workflow_is_current_and_fail_closed(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_call:", text)
        self.assertIn("actions/checkout@v7", text)
        self.assertIn("actions/setup-python@v7", text)
        self.assertIn("python .vaoferi/verify.py", text)
        self.assertIn("require-project-checks", text)
        self.assertIn("project-check-command", text)


if __name__ == "__main__":
    unittest.main()
