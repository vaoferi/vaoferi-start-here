from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENTS = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
DEPLOY = (ROOT / ".agents/skills/vaoferi-deploy/SKILL.md").read_text(encoding="utf-8")
SECURITY = (ROOT / ".agents/skills/vaoferi-security/SKILL.md").read_text(encoding="utf-8")
SYNC = (ROOT / "scripts/vaoferi_sync.py").read_text(encoding="utf-8")

class MultiAccountProviderIsolationTest(unittest.TestCase):
    def test_bounded_agent_core_routes_provider_writes_to_deploy_skill(self):
        self.assertIn("vaoferi-deploy", AGENTS)
        self.assertIn("production deploy/release", AGENTS)
        self.assertIn("vaoferi-security", AGENTS)
    def test_project_keeps_a_nonsecret_account_site_binding(self):
        for value in ("Project-owned non-secret binding", "provider_account_id", "website_id",
                      "production_domain", "document_root", "credential_profile_ref",
                      "temporary_preview_url", "verification_evidence"):
            self.assertIn(value, DEPLOY)
    def test_prewrite_account_and_parked_checks_are_required(self):
        for value in ("Mandatory release preflight", "current session/account identity",
                      "after every account/session/credential switch", "Detect conflicting domain claims",
                      "Parked Domain", "Mechanical requirement", "hard pre-write blocker"):
            self.assertIn(value, DEPLOY)
    def test_cross_account_migrations_do_not_silently_run(self):
        for value in ("Serialize production writes per provider account + website and domain",
                      "explicit owner-approved migration/rebinding", "mailboxes",
                      "BLOCKED before writes"):
            self.assertIn(value, DEPLOY)
    def test_credentials_are_account_specific_not_shared(self):
        for value in ("Provider account and credential affinity", "not authorization to write to account B",
                      "Vaultwarden + project-root", "currently authenticated"):
            self.assertIn(value, SECURITY)
    def test_sync_will_ship_provider_guardrails(self):
        for value in ('".agents/skills/vaoferi-deploy/SKILL.md"',
                      '".agents/skills/vaoferi-security/SKILL.md"'):
            self.assertIn(value, SYNC)

if __name__ == "__main__":
    unittest.main()
