from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
DEPLOY = ROOT / ".agents" / "skills" / "vaoferi-deploy" / "SKILL.md"
SYNC = ROOT / "scripts" / "vaoferi_sync.py"


class DeployProtocolContractTest(unittest.TestCase):
    def test_agents_routes_production_release_work_to_deploy_skill(self):
        text = AGENTS.read_text(encoding="utf-8")
        self.assertIn("vaoferi-deploy", text)
        self.assertIn("production", text.lower())
        self.assertIn("deploy", text.lower())

    def test_deploy_skill_is_fail_closed_and_layered(self):
        self.assertTrue(DEPLOY.is_file())
        text = DEPLOY.read_text(encoding="utf-8")
        for required in (
            "Capability preflight",
            "Candidate identity",
            "Target identity before mutation",
            "Preview artifact parity",
            "Rollback before apply",
            "Guarded apply",
            "Publication verification layers",
            "transport/upload",
            "remote target/read-back",
            "effective origin",
            "CDN/cache",
            "browser/user behavior",
            "HTTP 200",
            "exact pushed SHA",
        ):
            self.assertIn(required, text)

    def test_deploy_skill_prevents_repeated_blind_attempts(self):
        text = DEPLOY.read_text(encoding="utf-8")
        for required in (
            "Attempt frontier",
            "changed precondition",
            "same write-capable action",
            "what was ruled out",
            "last proven frontier",
        ):
            self.assertIn(required, text)

    def test_deploy_skill_covers_config_secrets_and_target_mapping(self):
        text = DEPLOY.read_text(encoding="utf-8")
        for required in (
            "Vaultwarden",
            "project-root `.env`",
            "credential-free example",
            "without printing values",
            "remote-root identity",
            "FTP PWD",
            "public-origin proof",
            "cache purge",
        ):
            self.assertIn(required, text)

    def test_deploy_skill_does_not_globalize_atomic_release_policy(self):
        text = DEPLOY.read_text(encoding="utf-8")
        self.assertIn("project-specific sequential/atomic policy", text)
        self.assertIn("Do not globalize atomic", text)

    def test_sync_owns_deploy_skill(self):
        text = SYNC.read_text(encoding="utf-8")
        self.assertIn('".agents/skills/vaoferi-deploy/SKILL.md"', text)


if __name__ == "__main__":
    unittest.main()
