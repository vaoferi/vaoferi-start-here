from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "codex_global.py"
TEMPLATE = ROOT / "templates" / "provider" / "codex.md"


def load_module():
    spec = importlib.util.spec_from_file_location("codex_global", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CodexGlobalTest(unittest.TestCase):
    def test_install_creates_managed_global_agents(self):
        mod = load_module()
        with TemporaryDirectory() as td:
            home = Path(td)
            target = mod.install(home)
            text = target.read_text(encoding="utf-8")
            self.assertIn(mod.BEGIN_MARKER, text)
            self.assertIn(mod.END_MARKER, text)
            self.assertIn(TEMPLATE.read_text(encoding="utf-8").strip(), text)
            self.assertEqual(mod.verify(home), target)

    def test_update_preserves_user_content_outside_managed_block(self):
        mod = load_module()
        with TemporaryDirectory() as td:
            home = Path(td)
            target = mod.install(home)
            original = target.read_text(encoding="utf-8")
            target.write_text(
                "# My personal notes\n\n" + original + "\n## Local preference\n\nKeep this.\n",
                encoding="utf-8",
            )
            mod.install(home)
            text = target.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("# My personal notes"))
            self.assertIn("## Local preference", text)
            self.assertIn("Keep this.", text)
            self.assertEqual(text.count(mod.BEGIN_MARKER), 1)
            self.assertEqual(text.count(mod.END_MARKER), 1)

    def test_unmanaged_existing_file_fails_closed_without_overwrite(self):
        mod = load_module()
        with TemporaryDirectory() as td:
            home = Path(td)
            home.mkdir(parents=True, exist_ok=True)
            target = home / "AGENTS.md"
            original = "# Existing global rules\n\nDo not overwrite me.\n"
            target.write_text(original, encoding="utf-8")
            with self.assertRaises(mod.CodexGlobalError):
                mod.install(home)
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_verify_rejects_managed_block_drift(self):
        mod = load_module()
        with TemporaryDirectory() as td:
            home = Path(td)
            target = mod.install(home)
            target.write_text(
                target.read_text(encoding="utf-8").replace("TDD", "TDD-DRIFT", 1),
                encoding="utf-8",
            )
            with self.assertRaises(mod.CodexGlobalError):
                mod.verify(home)

    def test_resolve_home_prefers_codex_home_environment(self):
        mod = load_module()
        with TemporaryDirectory() as td:
            home = Path(td)
            self.assertEqual(mod.resolve_home({"CODEX_HOME": str(home)}), home.resolve())


if __name__ == "__main__":
    unittest.main()
