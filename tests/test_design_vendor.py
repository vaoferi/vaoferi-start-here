from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "vendor" / "design-skill.lock.json"
VENDOR = ROOT / "vendor" / "vaoferi-design-skill"
AGENTS = ROOT / "AGENTS.md"


class DesignVendorTest(unittest.TestCase):
    def load_lock(self):
        return json.loads(LOCK.read_text(encoding="utf-8"))

    def test_lock_pins_canonical_design_source(self):
        lock = self.load_lock()
        self.assertEqual(lock["schema"], 1)
        self.assertEqual(lock["repository"], "vaoferi/vaoferi-design-skill")
        self.assertEqual(lock["version"], "0.3.2")
        self.assertRegex(lock["commit"], r"^[0-9a-f]{40}$")
        self.assertTrue(lock["files_sha256"])

    def test_locked_file_hashes_match_vendor(self):
        lock = self.load_lock()
        for rel, expected in lock["files_sha256"].items():
            path = VENDOR / rel
            self.assertTrue(path.is_file(), rel)
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(actual, expected, rel)

    def test_vendor_contains_design_policy_and_portable_catalog(self):
        skill = (VENDOR / "SKILL.md").read_text(encoding="utf-8")
        action = (VENDOR / "references" / "action-contract.md").read_text(encoding="utf-8")
        catalog = VENDOR / "config" / "component-libraries.json"
        self.assertIn("version: 0.3.2", skill)
        self.assertIn("48x48 CSS px", action)
        self.assertIn("STRONG_HEURISTIC_WITH_EXCEPTIONS", action)
        self.assertTrue(catalog.is_file())

    def test_root_contract_routes_design_conditionally_without_embedding_doctrine(self):
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("vaoferi-design-skill", agents)
        self.assertNotIn("STRONG_HEURISTIC_WITH_EXCEPTIONS", agents)
        self.assertNotIn("20 Principles Gate", agents)
        self.assertNotIn("48x48 CSS px", agents)


if __name__ == "__main__":
    unittest.main()
