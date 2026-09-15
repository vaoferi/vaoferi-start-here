from pathlib import Path
import sys

MAX_BYTES = 12 * 1024
FORBIDDEN = (
    "nlm.help",
    "admin.nlm.help",
    "storage.nlm.help",
    "BodyRes",
    "Miami Vero",
    "\\\\NAS\\",
    "18083",
)
REQUIRED = (
    "PROJECT_RULES.md",
    "vaoferi-design-skill",
    "vaoferi-security",
    "vaoferi-dependencies",
    "Linear",
    "Trello",
)


def check(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = path.read_bytes()
    except OSError as exc:
        return [f"cannot read {path}: {exc}"]

    if len(data) > MAX_BYTES:
        errors.append(f"AGENTS.md is {len(data)} bytes; max is {MAX_BYTES}")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"AGENTS.md is not valid UTF-8: {exc}"]

    for token in FORBIDDEN:
        if token in text:
            errors.append(f"project-specific token found: {token}")
    for token in REQUIRED:
        if token not in text:
            errors.append(f"required routing token missing: {token}")
    return errors


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "AGENTS.md")
    errors = check(path)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {path} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
