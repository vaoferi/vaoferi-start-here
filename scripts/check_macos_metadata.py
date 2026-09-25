#!/usr/bin/env python3
"""Report macOS AppleDouble siblings that Git still sees in the given repos.

Editing canonical NAS source from a Mac leaves a `._<name>` sibling next to every
written file. Git shows those as untracked, so they break the zero-dirty gate in
every repository at once. The remedy is an ignore rule, not a manual delete.
"""

from pathlib import Path
import subprocess
import sys


def violations(root: Path):
    """Return untracked paths under `root` whose name is an AppleDouble sibling."""
    proc = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git status failed in {root}")
    found = []
    for line in proc.stdout.splitlines():
        if not line.startswith("?? "):
            continue
        rel = line[3:].strip().strip('"')
        if Path(rel).name.startswith("._"):
            found.append(rel)
    return found


def main(argv):
    if not argv:
        print("usage: check_macos_metadata.py <repo-root> [...]", file=sys.stderr)
        return 2
    bad = 0
    for raw in argv:
        root = Path(raw).resolve()
        try:
            found = violations(root)
        except (RuntimeError, OSError) as error:
            print(f"{root}: BLOCKED {error}")
            bad += 1
            continue
        if found:
            bad += 1
            print(f"{root}: BLOCKED {len(found)} macOS metadata file(s)")
            for item in found:
                print(f"  {item}")
            print("  remedy: add a '._*' line to this repository's .gitignore")
        else:
            print(f"{root}: clean")
    if bad:
        print(f"MACOS METADATA: BLOCKED ({bad} repo(s))")
        return 1
    print("MACOS METADATA: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
