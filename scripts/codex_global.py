from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "provider" / "codex.md"
BEGIN_MARKER = "<!-- VAOFERI_START_HERE_CODEX:BEGIN -->"
END_MARKER = "<!-- VAOFERI_START_HERE_CODEX:END -->"


class CodexGlobalError(RuntimeError):
    pass


def resolve_home(env: dict[str, str] | None = None) -> Path:
    source = os.environ if env is None else env
    raw = source.get("CODEX_HOME")
    if raw:
        return Path(raw).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def canonical_body() -> str:
    return TEMPLATE.read_text(encoding="utf-8").strip()


def managed_block() -> str:
    return f"{BEGIN_MARKER}\n{canonical_body()}\n{END_MARKER}"


def target_path(home: Path) -> Path:
    return home / "AGENTS.md"


def _split_managed(text: str) -> tuple[str, str, str] | None:
    begin = text.find(BEGIN_MARKER)
    end = text.find(END_MARKER)
    if begin < 0 and end < 0:
        return None
    if begin < 0 or end < 0 or end < begin:
        raise CodexGlobalError("invalid managed Codex block markers")
    if text.find(BEGIN_MARKER, begin + len(BEGIN_MARKER)) >= 0:
        raise CodexGlobalError("duplicate managed Codex block begin marker")
    if text.find(END_MARKER, end + len(END_MARKER)) >= 0:
        raise CodexGlobalError("duplicate managed Codex block end marker")
    end_after = end + len(END_MARKER)
    return text[:begin], text[begin:end_after], text[end_after:]


def install(home: Path) -> Path:
    home = home.expanduser().resolve()
    home.mkdir(parents=True, exist_ok=True)
    target = target_path(home)
    block = managed_block()

    if not target.exists():
        target.write_text(block + "\n", encoding="utf-8")
        return target

    current = target.read_text(encoding="utf-8")
    if not current.strip():
        target.write_text(block + "\n", encoding="utf-8")
        return target

    parts = _split_managed(current)
    if parts is None:
        raise CodexGlobalError(
            f"unmanaged existing Codex global instructions: {target}; "
            "refusing to overwrite. Reconcile the existing file first."
        )

    before, _old_block, after = parts
    updated = before + block + after
    if updated != current:
        target.write_text(updated, encoding="utf-8")
    return target


def verify(home: Path) -> Path:
    home = home.expanduser().resolve()
    target = target_path(home)
    if not target.is_file():
        raise CodexGlobalError(f"Codex global instructions missing: {target}")

    current = target.read_text(encoding="utf-8")
    parts = _split_managed(current)
    if parts is None:
        raise CodexGlobalError(f"managed Vaoferi Codex block missing: {target}")

    _before, actual_block, _after = parts
    if actual_block != managed_block():
        raise CodexGlobalError(f"managed Vaoferi Codex block drift: {target}")
    return target


def status(home: Path) -> str:
    target = target_path(home.expanduser().resolve())
    if not target.exists():
        return f"MISSING: {target}"
    try:
        verify(home)
    except CodexGlobalError as exc:
        return f"DRIFT_OR_UNMANAGED: {exc}"
    return f"OK: {target}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install or verify the Vaoferi critical global Codex AGENTS block"
    )
    parser.add_argument("action", choices=("install", "verify", "status", "print"))
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=None,
        help="Override CODEX_HOME for this command",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    home = args.codex_home.expanduser().resolve() if args.codex_home else resolve_home()
    try:
        if args.action == "install":
            print(f"Installed/updated managed Codex block: {install(home)}")
        elif args.action == "verify":
            print(f"Verified managed Codex block: {verify(home)}")
        elif args.action == "status":
            print(status(home))
        else:
            print(managed_block())
    except (OSError, UnicodeError, CodexGlobalError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
