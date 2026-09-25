from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEPLOY = ROOT / ".agents" / "skills" / "vaoferi-deploy" / "SKILL.md"
TRACKING = ROOT / ".agents" / "skills" / "vaoferi-task-tracking" / "SKILL.md"
AGENTS = ROOT / "AGENTS.md"


class DeployOwnershipBoundaryTest(unittest.TestCase):
    """NLM-148: the deploy/product ownership line must be mechanical, not prose."""

    def test_deploy_may_only_fix_deploy_layer_defects(self):
        text = DEPLOY.read_text(encoding="utf-8")
        for required in (
            "DEPLOY-LAYER",
            "deploy adapter",
            "candidate packaging",
            "transport/target mapping",
            "rollback/preimage",
            "publication/origin verifier",
        ):
            self.assertIn(required, text)

    def test_emergency_fix_must_be_smallest_and_shipped(self):
        text = DEPLOY.read_text(encoding="utf-8")
        self.assertIn("smallest-possible", text)
        self.assertIn("committed and pushed", text)

    def test_outside_deploy_ownership_is_an_explicit_list(self):
        text = DEPLOY.read_text(encoding="utf-8")
        for required in (
            "product/UI/business logic",
            "media quality/performance",
            "responsive/layout/typography",
            "browser test harness",
            "CI/environment/browser-installation debt",
        ):
            self.assertIn(required, text)

    def test_outside_layer_requires_explicit_owner_scope_change(self):
        text = DEPLOY.read_text(encoding="utf-8")
        self.assertIn("explicit owner scope change", text)
        self.assertIn("fail fast", text)

    def test_already_accepted_candidate_does_not_replay_broad_regression(self):
        text = DEPLOY.read_text(encoding="utf-8")
        self.assertIn("does not re-run the broad pre-deploy regression", text)
        self.assertIn("implementation/CI task owns", text)

    def test_post_deploy_smoke_stays_mandatory(self):
        text = DEPLOY.read_text(encoding="utf-8")
        self.assertIn("post-deploy smoke", text)
        self.assertIn("mandatory", text)

    def test_discovered_debt_becomes_a_follow_up_without_blocking_release(self):
        text = DEPLOY.read_text(encoding="utf-8")
        self.assertIn("Linear follow-up task", text)
        self.assertIn("release continues", text)

    def test_routing_reference_states_the_same_boundary(self):
        tracking = TRACKING.read_text(encoding="utf-8")
        self.assertIn("DEPLOY-LAYER", tracking)
        self.assertIn("explicit owner scope change", tracking)
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("DEPLOY-LAYER", agents)

    def test_boundary_is_not_duplicated_into_the_done_definition(self):
        done = (ROOT / "DEFINITION_OF_DONE.md").read_text(encoding="utf-8")
        self.assertNotIn("DEPLOY-LAYER", done)


if __name__ == "__main__":
    unittest.main()
