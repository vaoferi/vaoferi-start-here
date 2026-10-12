"""NLM-234 machine regression: stage-aware receipts and invalidation."""
from datetime import datetime, timezone
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "target" / ".vaoferi" / "gate_resume.py"
spec = spec_from_file_location("gate_resume", SOURCE)
engine = module_from_spec(spec)
spec.loader.exec_module(engine)
NOW = datetime(2026, 10, 12, 12, tzinfo=timezone.utc)


def scenario():
    gates, current = {}, {}
    for n in range(1, 7):
        name = f"gate{n}"
        dep = [f"gate{n-1}"] if n > 1 else []
        rid = f"receipt-{n}"
        inp = {"relevant_hash": f"sha256:content-{n}", "environment": "stage-target"}
        gates[name] = {
            "depends_on": dep,
            "receipt": {
                "status": "PASS", "receipt_id": rid, "source_sha": "git-sha-old",
                "inputs": inp.copy(), "expires_at": "2026-11-12T00:00:00Z",
                "evidence": f"https://example.invalid/evidence/{n}",
                "dependency_receipts": {d: f"receipt-{n-1}" for d in dep},
            },
        }
        current[name] = {"verified": True, "source_sha": "git-sha-old", "inputs": inp.copy()}
    return {"schema": 1, "gates": gates}, {"schema": 1, "gates": current}


class GateReceiptTests(unittest.TestCase):
    def eval(self, ledger, observed):
        return engine.evaluate(ledger, observed, NOW)

    def test_later_failed_gate_does_not_repeat_unchanged_visual_gate(self):
        ledger, observed = scenario()
        ledger["gates"]["gate5"]["receipt"]["status"] = "FAIL"
        r = self.eval(ledger, observed)
        self.assertEqual([r[f"gate{i}"]["action"] for i in range(1, 7)],
                         ["REUSE", "REUSE", "REUSE", "REUSE", "FIX_FOCUSED", "BLOCKED"])

    def test_fix_fifth_gate_with_proven_unaffected_prior_inputs(self):
        ledger, observed = scenario()
        ledger["gates"]["gate5"]["receipt"]["status"] = "FAIL"
        for i in range(1, 7):
            observed["gates"][f"gate{i}"].update(source_sha="git-sha-new")
        for i in range(1, 5):
            observed["gates"][f"gate{i}"].update(source_impact="unaffected", impact_evidence=f"diff-check:{i}")
        before = self.eval(ledger, observed)
        self.assertEqual(before["gate4"]["action"], "REUSE")
        self.assertEqual(before["gate5"]["action"], "FIX_FOCUSED")
        ledger["gates"]["gate5"]["receipt"].update(status="PASS", source_sha="git-sha-new", receipt_id="receipt-5-fixed")
        ledger["gates"]["gate6"]["receipt"].update(dependency_receipts={"gate5": "receipt-5"})
        after = self.eval(ledger, observed)
        self.assertEqual([after[f"gate{i}"]["action"] for i in range(1, 7)],
                         ["REUSE", "REUSE", "REUSE", "REUSE", "REUSE", "RERUN"])

    def test_changed_database_invalidates_dependent_visual_and_not_unrelated(self):
        ledger, observed = scenario()
        observed["gates"]["gate2"]["inputs"]["relevant_hash"] = "sha256:new-db"
        first = self.eval(ledger, observed)
        self.assertEqual(first["gate1"]["action"], "REUSE")
        self.assertEqual(first["gate2"]["action"], "RERUN")
        self.assertEqual(first["gate3"]["action"], "BLOCKED")
        db = ledger["gates"]["gate2"]["receipt"]
        db.update(receipt_id="receipt-2-refreshed", inputs=observed["gates"]["gate2"]["inputs"].copy())
        second = self.eval(ledger, observed)
        self.assertEqual(second["gate2"]["action"], "REUSE")
        self.assertEqual(second["gate3"]["action"], "RERUN")

    def test_waived_is_never_pass(self):
        ledger, observed = scenario()
        ledger["gates"]["gate2"]["receipt"]["status"] = "WAIVED"
        r = self.eval(ledger, observed)
        self.assertEqual(r["gate2"]["action"], "WAIVED")
        self.assertEqual(r["gate3"]["action"], "BLOCKED")

    def test_missing_provenance_or_unknown_input_fails_closed(self):
        ledger, observed = scenario()
        observed["gates"]["gate1"].pop("verified")
        self.assertEqual(self.eval(ledger, observed)["gate1"]["action"], "BLOCKED")
        ledger, observed = scenario()
        observed["gates"]["gate1"]["source_sha"] = "other-sha"
        self.assertEqual(self.eval(ledger, observed)["gate1"]["action"], "RERUN")

    def test_expired_and_missing_evidence_are_not_reusable(self):
        ledger, observed = scenario()
        ledger["gates"]["gate1"]["receipt"]["expires_at"] = "2026-10-11T11:00:00Z"
        self.assertEqual(self.eval(ledger, observed)["gate1"]["action"], "RERUN")
        ledger, observed = scenario()
        ledger["gates"]["gate1"]["receipt"]["evidence"] = ""
        self.assertEqual(self.eval(ledger, observed)["gate1"]["action"], "BLOCKED")

    def test_cycles_and_unknown_dependencies_rejected(self):
        ledger, observed = scenario()
        ledger["gates"]["gate1"]["depends_on"] = ["gate6"]
        with self.assertRaisesRegex(engine.ContractError, "cycle"):
            self.eval(ledger, observed)
        ledger, observed = scenario()
        ledger["gates"]["gate1"]["depends_on"] = ["does-not-exist"]
        with self.assertRaisesRegex(engine.ContractError, "unknown dependency"):
            self.eval(ledger, observed)

    def test_receipt_dependencies_required(self):
        ledger, observed = scenario()
        del ledger["gates"]["gate2"]["receipt"]["dependency_receipts"]
        self.assertEqual(self.eval(ledger, observed)["gate2"]["action"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
