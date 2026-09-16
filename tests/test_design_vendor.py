from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "vendor" / "design-skill.lock.json"
VENDOR = ROOT / "vendor" / "vaoferi-design-skill"
AGENTS = ROOT / "AGENTS.md"
EXPECTED_VERSION = "0.4.0"
EXPECTED_COMMIT = "03bf403992df459f3cf85cf000d27ce9ed36f698"
REQUIRED_V040_REFERENCES = (
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

    def test_vendor_contains_v040_contract_and_preserved_policy(self):
        skill = (VENDOR / "SKILL.md").read_text(encoding="utf-8")
        quality = (VENDOR / "references" / "quality-gates.md").read_text(encoding="utf-8")
        catalog = VENDOR / "config" / "component-libraries.json"

        self.assertIn(f"version: {EXPECTED_VERSION}", skill)
        self.assertIn("contract architecture v1.2", skill)
        self.assertIn("48x48 CSS px", quality)
        self.assertIn("strong heuristic failure", quality)
        self.assertTrue(catalog.is_file())
        for rel in REQUIRED_V040_REFERENCES:
            self.assertTrue((VENDOR / rel).is_file(), rel)

    def test_root_contract_routes_design_conditionally_without_embedding_doctrine(self):
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("vaoferi-design-skill", agents)
        self.assertNotIn("20 Principles Gate", agents)
        self.assertNotIn("48x48 CSS px", agents)
        self.assertNotIn("contract architecture v1.2", agents)


if __name__ == "__main__":
    unittest.main()
