"""Read-only decision helper for stage-scoped, durable verification receipts.

No claim of PASS is made here; provenance and input hashes must be measured
and independently checked by the agent before this deterministic comparison.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    pass


def _when(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ContractError("expires_at requires an RFC3339 timestamp")
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError("invalid expires_at timestamp") from exc
    if stamp.tzinfo is None:
        raise ContractError("expires_at must be timezone-aware")
    return stamp


def evaluate(ledger: dict, observed: dict, now: datetime | None = None) -> dict[str, dict[str, str]]:
    """Classify gates as REUSE, RERUN, FIX_FOCUSED, WAIVED, or BLOCKED.

    Source SHA is provenance, not a blanket invalidator: a changed commit
    requires measured unchanged stage inputs AND explicit impact evidence.
    A dependency's receipt_id pins the exact successful prerequisite revision.
    """
    if ledger.get("schema") != 1 or observed.get("schema") != 1:
        raise ContractError("unsupported or missing schema")
    gates, current = ledger.get("gates"), observed.get("gates")
    if not isinstance(gates, dict) or not gates or not isinstance(current, dict):
        raise ContractError("gates must be nonempty objects")
    instant = now or datetime.now(timezone.utc)
    if instant.tzinfo is None:
        raise ContractError("evaluation time must be timezone-aware")
    states: dict[str, dict[str, str]] = {}
    visiting: set[str] = set()

    def visit(name: str) -> dict[str, str]:
        if name in states:
            return states[name]
        if name in visiting:
            raise ContractError("dependency cycle at " + name)
        if name not in gates:
            raise ContractError("unknown dependency: " + name)
        visiting.add(name)
        gate = gates[name]
        if not isinstance(gate, dict):
            raise ContractError("invalid gate: " + name)
        dependencies = gate.get("depends_on")
        if not isinstance(dependencies, list) or not all(isinstance(x, str) and x for x in dependencies) or len(set(dependencies)) != len(dependencies):
            raise ContractError("invalid dependencies: " + name)
        upstream = {dep: visit(dep) for dep in dependencies}
        visiting.remove(name)

        def decide(action: str, reason: str) -> dict[str, str]:
            states[name] = {"action": action, "reason": reason}
            return states[name]

        actual, receipt = current.get(name), gate.get("receipt")
        if not isinstance(actual, dict) or not isinstance(actual.get("inputs"), dict) or not actual["inputs"]:
            return decide("BLOCKED", "missing verified current inputs")
        if actual.get("verified") is not True or not isinstance(actual.get("source_sha"), str) or not actual["source_sha"]:
            return decide("BLOCKED", "missing current provenance")
        if any(v["action"] != "REUSE" for v in upstream.values()):
            return decide("BLOCKED", "prerequisite lacks a reusable PASS")
        if receipt is None:
            return decide("RERUN", "no successful receipt")
        if not isinstance(receipt, dict):
            return decide("BLOCKED", "malformed receipt")
        status = receipt.get("status")
        if status == "WAIVED":
            return decide("WAIVED", "waiver is not PASS")
        if status == "BLOCKED":
            return decide("BLOCKED", "earlier stage blocked")
        if status == "FAIL":
            return decide("FIX_FOCUSED", "repair this failed gate first")
        if status != "PASS":
            return decide("BLOCKED", "unknown receipt status")
        if not isinstance(receipt.get("receipt_id"), str) or not receipt["receipt_id"]:
            return decide("BLOCKED", "receipt identity missing")
        if not isinstance(receipt.get("evidence"), str) or not receipt["evidence"]:
            return decide("BLOCKED", "evidence pointer missing")
        try:
            expiry = _when(receipt.get("expires_at"))
        except ContractError as exc:
            return decide("BLOCKED", str(exc))
        if instant >= expiry:
            return decide("RERUN", "receipt expired")
        if not isinstance(receipt.get("inputs"), dict) or receipt["inputs"] != actual["inputs"]:
            return decide("RERUN", "stage inputs changed")
        claimed_deps = receipt.get("dependency_receipts")
        if not isinstance(claimed_deps, dict) or set(claimed_deps) != set(dependencies):
            return decide("BLOCKED", "missing dependency binding")
        for dep in dependencies:
            dependency_receipt = gates[dep].get("receipt") or {}
            if not isinstance(dependency_receipt, dict) or claimed_deps[dep] != dependency_receipt.get("receipt_id"):
                return decide("RERUN", "prerequisite receipt changed")
        if not isinstance(receipt.get("source_sha"), str) or not receipt["source_sha"]:
            return decide("BLOCKED", "receipt source SHA missing")
        if receipt["source_sha"] != actual["source_sha"]:
            if actual.get("source_impact") != "unaffected" or not isinstance(actual.get("impact_evidence"), str) or not actual["impact_evidence"]:
                return decide("RERUN", "changed source without scoped impact proof")
        return decide("REUSE", "same stage inputs and successful evidence")

    for key in gates:
        visit(key)
    return states


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only durable gate receipt evaluator")
    parser.add_argument("ledger", type=Path)
    parser.add_argument("observed", type=Path)
    args = parser.parse_args()
    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
        observed = json.loads(args.observed.read_text(encoding="utf-8"))
        decision = evaluate(ledger, observed)
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if all(x["action"] == "REUSE" for x in decision.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
