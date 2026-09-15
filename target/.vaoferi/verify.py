from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ALLOWED_ENV = {".env.example", ".env.sample", ".env.template"}
TEXT_SUFFIXES = {".md", ".py", ".json", ".toml", ".yml", ".yaml", ".txt"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest(root: Path) -> dict:
    path = root / ".vaoferi/manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != 1:
        raise ValueError(f"unsupported manifest schema: {data.get('schema')!r}")
    return data


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        capture_output=True,
    )
    if result.returncode != 0:
        return []
    return [p.decode("utf-8", errors="strict") for p in result.stdout.split(b"\0") if p]


def is_real_env(path: str) -> bool:
    name = Path(path).name
    if name in ALLOWED_ENV:
        return False
    return name == ".env" or name.startswith(".env.")


def verify(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load_manifest(root)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        return [f"manifest error: {exc}"]

    owned = manifest.get("owned_files", {})
    if not isinstance(owned, dict):
        return ["manifest error: owned_files must be an object"]

    for rel, expected in owned.items():
        path = root / rel
        if not path.is_file():
            errors.append(f"hash check failed: missing {rel}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(f"hash check failed: {rel}")
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            data = path.read_bytes()
            try:
                data.decode("utf-8")
            except UnicodeDecodeError:
                errors.append(f"utf8 check failed: {rel}")
            if path.suffix.lower() == ".md" and data.startswith(b"\xef\xbb\xbf"):
                errors.append(f"bom check failed: {rel}")

    for rel in tracked_files(root):
        if is_real_env(rel):
            errors.append(f"tracked env forbidden: {rel}")

    return errors


def main() -> int:
    root = repo_root()
    errors = verify(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("OK: Start Here manifest and centrally-owned files verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
