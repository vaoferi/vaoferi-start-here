from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_REL = Path(".vaoferi/manifest.json")
PROJECT_OWNED = ["PROJECT_RULES.md", "DESIGN.md", "docs/", "tests/"]
DESIGN_LOCK = ROOT / "vendor" / "design-skill.lock.json"
DESIGN_VENDOR = ROOT / "vendor" / "vaoferi-design-skill"
BASE_OWNED_SOURCES = {
    "AGENTS.md": ROOT / "AGENTS.md",
    "DEFINITION_OF_DONE.md": ROOT / "DEFINITION_OF_DONE.md",
    ".agents/skills/vaoferi-bootstrap/SKILL.md": ROOT / ".agents/skills/vaoferi-bootstrap/SKILL.md",
    ".agents/skills/vaoferi-engineering/SKILL.md": ROOT / ".agents/skills/vaoferi-engineering/SKILL.md",
    ".agents/skills/vaoferi-dependencies/SKILL.md": ROOT / ".agents/skills/vaoferi-dependencies/SKILL.md",
    ".agents/skills/vaoferi-deploy/SKILL.md": ROOT / ".agents/skills/vaoferi-deploy/SKILL.md",
    ".agents/skills/vaoferi-security/SKILL.md": ROOT / ".agents/skills/vaoferi-security/SKILL.md",
    ".agents/skills/vaoferi-task-tracking/SKILL.md": ROOT / ".agents/skills/vaoferi-task-tracking/SKILL.md",
    ".agents/skills/vaoferi-project-adaptation/SKILL.md": ROOT / ".agents/skills/vaoferi-project-adaptation/SKILL.md",
    ".vaoferi/verify.py": ROOT / "target/.vaoferi/verify.py",\n    ".vaoferi/check_worktree_clean.py": ROOT / "target/.vaoferi/check_worktree_clean.py",
}


class SyncError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def design_vendor_sources() -> dict[str, Path]:
    try:
        lock = json.loads(DESIGN_LOCK.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SyncError(f"canonical design lock missing: {DESIGN_LOCK}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SyncError(f"canonical design lock invalid: {DESIGN_LOCK}: {exc}") from exc
    if lock.get("schema") != 1:
        raise SyncError(f"unsupported design lock schema: {lock.get('schema')!r}")
    hashes = lock.get("files_sha256")
    if not isinstance(hashes, dict) or not hashes:
        raise SyncError("design lock files_sha256 must be a non-empty object")

    sources: dict[str, Path] = {}
    for rel, expected in sorted(hashes.items()):
        if not isinstance(rel, str) or not isinstance(expected, str):
            raise SyncError("design lock paths and hashes must be strings")
        source = DESIGN_VENDOR / rel
        if not source.is_file():
            raise SyncError(f"canonical design vendor file missing: {rel}")
        actual = sha256_file(source)
        if actual != expected:
            raise SyncError(f"canonical design vendor drift: {rel}")
        target_rel = (Path(".agents/skills/vaoferi-design-skill") / rel).as_posix()
        sources[target_rel] = source
    return sources


def owned_sources() -> dict[str, Path]:
    sources = dict(BASE_OWNED_SOURCES)
    sources.update(design_vendor_sources())
    return sources


def read_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        return tomllib.load(fh)["project"]["version"]


def source_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return "unresolved-local"


def manifest_path(target: Path) -> Path:
    return target / MANIFEST_REL


def load_manifest(target: Path) -> dict:
    path = manifest_path(target)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SyncError(f"manifest missing: {path}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SyncError(f"manifest invalid: {path}: {exc}") from exc
    if data.get("schema") != 1:
        raise SyncError(f"unsupported manifest schema: {data.get('schema')!r}")
    if not isinstance(data.get("owned_files"), dict):
        raise SyncError("manifest owned_files must be an object")
    return data


def write_manifest(target: Path, installed_at: str, sources: dict[str, Path]) -> bytes:
    owned = {rel: sha256_file(target / rel) for rel in sorted(sources)}
    data = {
        "schema": 1,
        "start_here": {
            "version": read_version(),
            "source_commit": source_commit(),
        },
        "owned_files": owned,
        "project_owned": PROJECT_OWNED,
        "installed_at": installed_at,
    }
    payload = (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path = manifest_path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return payload


def copy_owned(target: Path, previous_owned: dict[str, str] | None, sources: dict[str, Path]) -> None:
    for rel, source in sources.items():
        if not source.is_file():
            raise SyncError(f"canonical source missing: {source}")
        dest = target / rel
        source_data = source.read_bytes()
        if dest.exists() and previous_owned is None and dest.read_bytes() != source_data:
            raise SyncError(f"bootstrap conflict at centrally-owned path: {rel}")
        if dest.exists() and previous_owned is not None and rel not in previous_owned:
            if dest.read_bytes() != source_data:
                raise SyncError(f"update conflict at newly-owned path: {rel}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.read_bytes() != source_data:
            dest.write_bytes(source_data)


def assert_no_drift(target: Path, manifest: dict) -> None:
    errors: list[str] = []
    for rel, expected in manifest["owned_files"].items():
        path = target / rel
        if not path.is_file():
            errors.append(f"drift: missing centrally-owned file: {rel}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(f"drift: centrally-owned file changed: {rel}")
    if errors:
        raise SyncError("\n".join(errors))


def retire_removed_owned_files(target: Path, previous_owned: dict[str, str], sources: dict[str, Path]) -> None:
    for rel in sorted(set(previous_owned) - set(sources)):
        path = target / rel
        if path.exists():
            path.unlink()


def bootstrap(target: Path) -> None:
    sources = owned_sources()
    target.mkdir(parents=True, exist_ok=True)
    if manifest_path(target).exists():
        raise SyncError("bootstrap conflict: manifest already exists; use update")
    copy_owned(target, previous_owned=None, sources=sources)
    installed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    write_manifest(target, installed_at, sources)
    print(f"Bootstrapped Start Here into {target}")


def update(target: Path) -> None:
    sources = owned_sources()
    manifest = load_manifest(target)
    assert_no_drift(target, manifest)
    previous_owned = dict(manifest["owned_files"])
    copy_owned(target, previous_owned=previous_owned, sources=sources)
    retire_removed_owned_files(target, previous_owned, sources)
    before = manifest_path(target).read_bytes()
    after = write_manifest(target, manifest["installed_at"], sources)
    if before == after:
        print(f"Start Here already current in {target}")
    else:
        print(f"Updated Start Here in {target}")


def verify(target: Path) -> None:
    manifest = load_manifest(target)
    assert_no_drift(target, manifest)
    for rel in manifest["owned_files"]:
        for project_path in manifest.get("project_owned", []):
            if rel == project_path or (project_path.endswith("/") and rel.startswith(project_path)):
                raise SyncError(f"ownership conflict: {rel} is both central and project-owned")
    verifier = target / ".vaoferi/verify.py"
    result = subprocess.run([sys.executable, str(verifier)], cwd=target)
    if result.returncode != 0:
        raise SyncError(f"target verifier failed with exit {result.returncode}")
    print(f"Verified Start Here in {target}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap, update, or verify Vaoferi Start Here in a repository")
    parser.add_argument("action", choices=("bootstrap", "update", "verify"))
    parser.add_argument("--target", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = args.target.resolve()
    try:
        {"bootstrap": bootstrap, "update": update, "verify": verify}[args.action](target)
    except (OSError, SyncError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
