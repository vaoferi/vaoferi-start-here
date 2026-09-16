from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "vendor" / "design-skill.lock.json"
VENDOR = ROOT / "vendor" / "vaoferi-design-skill"
AGENTS = ROOT / "AGENTS.md"
EXPECTED_VERSION = "0.4.1"
EXPECTED_COMMIT = "264991d7a6c79322b39567391634f1045ccb170d"
REQUIRED_V041_REFERENCES = (
    "references/scopes.md",
    "references/lifecycle.md",
    "references/stages.md",
    "references/verification.md",
    "references/admin-workspace.md",
)


class DesignVendorTest(unittest.TestCase):
    def load_lock(self):
        return json.loads(LOCK.read_text(encoding="utf-8"))

    def test_lock_pins_canonical_design_source(self):
        lock = self.load_lock()
        self.assertEqual(lock["schema"], 1)
        self.assertEqual(lock["repository"], "vaoferi/vaoferi-design-skill")
        self.assertEqual(lock["version"], EXPECTED_VERSION)
        self.assertEqual(lock["commit"], EXPECTED_COMMIT)
        self.assertTrue(lock["files_sha256"])

    def test_locked_file_hashes_match_vendor(self):
        lock = self.load_lock()
        for rel, expected in lock["files_sha256"].items():
            path = VENDOR / rel
            self.assertTrue(path.is_file(), rel)
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(actual, expected, rel)

    def test_vendor_contains_v041_contract_and_preserved_policy(self):
        skill = (VENDOR / "SKILL.md").read_text(encoding="utf-8")
        quality = (VENDOR / "references" / "quality-gates.md").read_text(encoding="utf-8")
        stages = (VENDOR / "references" / "stages.md").read_text(encoding="utf-8")
        catalog = VENDOR / "config" / "component-libraries.json"

        self.assertIn(f"version: {EXPECTED_VERSION}", skill)
        self.assertIn("contract architecture v1.2", skill)
        self.assertIn("48x48 CSS px", quality)
        self.assertIn("strong heuristic failure", quality)
        self.assertIn("style owner", stages)
        self.assertIn("override layer", stages)
        self.assertIn("whole dependency/library", stages)
        self.assertIn("trivial visual", stages)
        self.assertTrue(catalog.is_file())
        for rel in REQUIRED_V041_REFERENCES:
            self.assertTrue((VENDOR / rel).is_file(), rel)

    def test_root_contract_routes_design_conditionally_without_embedding_doctrine(self):
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("vaoferi-design-skill", agents)
        self.assertNotIn("20 Principles Gate", agents)
        self.assertNotIn("48x48 CSS px", agents)
        self.assertNotIn("contract architecture v1.2", agents)


if __name__ == "__main__":
    unittest.main()
