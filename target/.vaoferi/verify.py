from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

SAFE_ENV_TEMPLATE_SUFFIXES = (".example", ".sample", ".template")
TEXT_SUFFIXES = {".md", ".py", ".json", ".toml", ".yml", ".yaml", ".txt"}
MAX_SECRET_SCAN_BYTES = 2 * 1024 * 1024
SECRET_PATTERNS = (
    ("AWS_ACCESS_KEY_ID", re.compile(rb"\bAKIA[0-9A-Z]{16}\b")),
    ("GITHUB_CLASSIC_TOKEN", re.compile(rb"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b")),
    ("GITHUB_FINE_GRAINED_TOKEN", re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{50,}\b")),
    ("PRIVATE_KEY", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("SLACK_TOKEN", re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
)
MOJIBAKE_MARKERS = ("\ufffd",)

# Trusted central identity. This is the only source allowed to establish
# "central latest"; a local checkout or cached ref is not.
CENTRAL_URL = "https://github.com/vaoferi/vaoferi-start-here.git"
CENTRAL_REF = "refs/heads/main"
CENTRAL_URL_ENV = "VAOFERI_START_HERE_CENTRAL_URL"
CENTRAL_REF_ENV = "VAOFERI_START_HERE_CENTRAL_REF"
CENTRAL_TIMEOUT_SECONDS = 60

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_UNKNOWN = 2


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
    if name == ".env":
        return True
    if not name.startswith(".env."):
        return False
    return not name.endswith(SAFE_ENV_TEMPLATE_SUFFIXES)


def check_owned_text(rel: str, path: Path, data: bytes) -> list[str]:
    errors: list[str] = []
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return errors
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [f"utf8 check failed: {rel}"]
    if path.suffix.lower() == ".md" and data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"bom check failed: {rel}")
    if any(marker in text for marker in MOJIBAKE_MARKERS):
        errors.append(f"mojibake check failed: {rel}")
    return errors


def check_tracked_secret_patterns(root: Path, rel: str) -> list[str]:
    path = root / rel
    try:
        if not path.is_file() or path.stat().st_size > MAX_SECRET_SCAN_BYTES:
            return []
        data = path.read_bytes()
    except OSError:
        return []
    errors: list[str] = []
    for rule_id, pattern in SECRET_PATTERNS:
        if pattern.search(data):
            errors.append(f"secret pattern {rule_id}: {rel}")
    return errors


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
        data = path.read_bytes()
        errors.extend(check_owned_text(rel, path, data))
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            errors.append(f"hash check failed: {rel}")

    for rel in tracked_files(root):
        if is_real_env(rel):
            errors.append(f"tracked env forbidden: {rel}")
        errors.extend(check_tracked_secret_patterns(root, rel))

    return errors


def installed_identity(root: Path):
    start_here = load_manifest(root).get("start_here", {})
    version = str(start_here.get("version", ""))
    commit = str(start_here.get("source_commit", ""))
    if not version or not commit:
        raise ValueError("manifest start_here must carry version and source_commit")
    return version, commit


def remote_head(url: str, ref: str):
    """Fresh remote lookup; None means central could not be established.

    ls-remote is used rather than a cached local ref so that a stale checkout
    can never answer the central-freshness question.
    """
    try:
        result = subprocess.run(
            ["git", "ls-remote", url, ref],
            capture_output=True,
            text=True,
            timeout=CENTRAL_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] == ref:
            return parts[0]
    return None


def check_central(root: Path) -> int:
    url = os.environ.get(CENTRAL_URL_ENV) or CENTRAL_URL
    ref = os.environ.get(CENTRAL_REF_ENV) or CENTRAL_REF
    try:
        version, installed = installed_identity(root)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(
            "CENTRAL STATUS: UNKNOWN\n"
            f"reason: installed identity unreadable: {exc}",
            file=sys.stderr,
        )
        return EXIT_UNKNOWN

    central = remote_head(url, ref)
    if central is None:
        # UNKNOWN is blocking, never a synonym for current.
        print(
            "CENTRAL STATUS: UNKNOWN\n"
            f"installed: {version} @ {installed}\n"
            f"central: could not be established from {url} {ref}\n"
            "consequence: central freshness unproven; do not report central drift: none",
            file=sys.stderr,
        )
        return EXIT_UNKNOWN

    if central == installed:
        print(
            "CENTRAL STATUS: CURRENT\n"
            f"installed: {version} @ {installed}\n"
            f"central: {central} ({url} {ref})"
        )
        return EXIT_OK

    print(
        "CENTRAL STATUS: OUTDATED\n"
        f"installed: {version} @ {installed}\n"
        f"central: {central} ({url} {ref})\n"
        "consequence: installed baseline lags central main",
        file=sys.stderr,
    )
    return EXIT_FAILED


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    action = args[0] if args else "local"
    root = repo_root()
    if action == "check-central":
        return check_central(root)
    if action != "local":
        print(f"unknown action: {action}", file=sys.stderr)
        return EXIT_FAILED
    errors = verify(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return EXIT_FAILED
    # A local pass proves hashes/hygiene only. Central freshness requires the
    # explicit check-central action, so a stale installation can never read as
    # central-current.
    print("OK: Start Here manifest and repository hygiene verified")
    print("central freshness not established; run 'check-central' for that claim")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())


