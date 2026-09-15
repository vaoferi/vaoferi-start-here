from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = ROOT / "vendor" / "vaoferi-design-skill"
LOCK_PATH = ROOT / "vendor" / "design-skill.lock.json"
REPOSITORY = "vaoferi/vaoferi-design-skill"
GIT_PATHS = ("SKILL.md", "references", "scripts", "config/component-libraries.json")
REQUIRED = {
    "SKILL.md",
    "references/action-contract.md",
    "references/component-sources.md",
    "references/quality-gates.md",
    "references/skillopt-and-architecture.md",
    "scripts/check_skill_structure.py",
    "scripts/get_component_snippet.py",
    "scripts/validate_snippets_source.py",
    "config/component-libraries.json",
}
BLOCKED_PARTS = {".env", ".skillopt", "__pycache__", ".git", "outputs", "cache", "caches"}
SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "openai-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}


class VendorError(RuntimeError):
    pass


def run_git(source: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=source,
        text=True,
        capture_output=True,
        check=False,
    )


def verify_source(source: Path, commit: str, version: str) -> list[str]:
    if not source.is_dir():
        raise VendorError(f"source directory missing: {source}")

    head = run_git(source, "rev-parse", "HEAD")
    if head.returncode != 0:
        raise VendorError("design source must be a Git checkout")
    if head.stdout.strip() != commit:
        raise VendorError(f"design source HEAD mismatch: expected {commit}, got {head.stdout.strip()}")

    for args, label in ((["diff", "--quiet", "--", *GIT_PATHS], "working tree"), (["diff", "--cached", "--quiet", "--", *GIT_PATHS], "index")):
        result = run_git(source, *args)
        if result.returncode != 0:
            raise VendorError(f"design source {label} has changes in vendored paths")

    tracked = run_git(source, "ls-files", "-z", "--", *GIT_PATHS)
    if tracked.returncode != 0:
        raise VendorError(tracked.stderr.strip() or "git ls-files failed")
    rels = sorted(filter(None, tracked.stdout.split("\0")))
    missing = sorted(REQUIRED - set(rels))
    if missing:
        raise VendorError("required design files are not tracked: " + ", ".join(missing))

    skill = (source / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"(?m)^  version: ([^\s]+)$", skill)
    actual_version = match.group(1) if match else None
    if actual_version != version:
        raise VendorError(f"design skill version mismatch: expected {version}, got {actual_version!r}")
    return rels


def validate_file(source: Path, rel: str) -> bytes:
    parts = {part.lower() for part in Path(rel).parts}
    if parts & BLOCKED_PARTS or Path(rel).name.lower().startswith(".env"):
        raise VendorError(f"blocked vendor path: {rel}")
    path = source / rel
    if path.is_symlink() or not path.is_file():
        raise VendorError(f"vendored path must be a regular file: {rel}")
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise VendorError(f"UTF-8 BOM is not allowed in vendored file: {rel}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VendorError(f"vendored file is not UTF-8 text: {rel}") from exc
    for rule, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            raise VendorError(f"secret pattern {rule} found in {rel}")
    return data


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def vendor(source: Path, commit: str, version: str) -> None:
    rels = verify_source(source, commit, version)
    staged: dict[str, bytes] = {rel: validate_file(source, rel) for rel in rels}

    if VENDOR_ROOT.exists():
        shutil.rmtree(VENDOR_ROOT)
    VENDOR_ROOT.mkdir(parents=True, exist_ok=True)
    for rel, data in staged.items():
        dest = VENDOR_ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    lock = {
        "schema": 1,
        "repository": REPOSITORY,
        "commit": commit,
        "version": version,
        "files_sha256": {rel: sha256(data) for rel, data in sorted(staged.items())},
    }
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOCK_PATH.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Vendored {len(staged)} files from {REPOSITORY}@{commit} ({version})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Vendor the reviewed canonical Vaoferi design skill")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--version", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        vendor(args.source.resolve(), args.commit, args.version)
    except (OSError, VendorError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
