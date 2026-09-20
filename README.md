# Vaoferi Start Here

**Current release: 0.2.1**

Public canonical source for Vaoferi-wide AI-agent behavior, conditional local skills and repository bootstrap/sync rules.

## Source-of-truth model

- `AGENTS.md` — compact universal owner/agent contract copied byte-for-byte into participating repositories.
- `PROJECT_RULES.md` — rules for this repository only; each target repository owns its own `PROJECT_RULES.md`.
- `.agents/skills/vaoferi-*` — conditional procedures loaded only when relevant.
- `vaoferi-design-skill` — separate canonical design source; a reviewed snapshot is vendored here and synced into target repositories for local/offline use.
- Linear — active work tracker. Trello — incremental legacy input only: migrate relevant cards as they are encountered; delete when supported, otherwise archive/close after parity.

The architecture is intentionally local-first: after bootstrap/update, ordinary work in a target repository must not depend on network access to this repository.

## 0.2.0: Project Adaptation

Installing the universal baseline into an existing repository is **not permission to erase its local knowledge**.

For a repo that already has legacy, nested, duplicated, stale or conflicting instructions/docs, load `vaoferi-project-adaptation` after bootstrap discovery. Its canonical lifecycle is:

```text
inventory -> classify -> conflicts -> owner decisions -> migrate -> machine-enforce -> parity -> cleanup -> verify
```

The adaptation pass recursively inspects the relevant tracked tree, classifies each meaningful rule, preserves project-only facts in project-owned documentation, routes reusable design/engineering/security/task knowledge to the correct canonical skill, surfaces meaningful conflicts to the owner, and retires old sources only after destination + parity + reference verification.

A clean/new repository does not need the full legacy-adaptation ceremony when there is no existing knowledge to reconcile.

## Development

Requires Python 3.11+ and no runtime dependencies for the core tooling.

```bash
python -m unittest discover -s tests -v
python scripts/check_agents_contract.py AGENTS.md
```

`Start Here self-test` runs these checks on every push and pull request to `main`.

## Bootstrap / update / verify

The canonical sync entrypoint is `scripts/vaoferi_sync.py`:

```bash
python scripts/vaoferi_sync.py bootstrap --target /path/to/repository
python scripts/vaoferi_sync.py update --target /path/to/repository
python scripts/vaoferi_sync.py verify --target /path/to/repository
```

Bootstrap/update copies centrally-owned rules and skills into the target repository and records exact hashes/source version in `.vaoferi/manifest.json`. Project-owned files such as `PROJECT_RULES.md`, `DESIGN.md`, `docs/` and `tests/` are not silently overwritten.

The synced package includes the reviewed Vaoferi Design Skill snapshot, currently **0.4.2 / contract architecture 1.2**, pinned by exact Git commit and SHA-256 hashes.

## Reusable GitHub checks

Target repositories should pin the shared verification workflow to a reviewed **exact commit SHA** (or an intentionally created release tag once one exists), rather than assuming a tag name exists:

```yaml
jobs:
  vaoferi:
    uses: vaoferi/vaoferi-start-here/.github/workflows/vaoferi-checks.yml@<reviewed-commit-sha>
```

`project-check-command` is project-owned: Start Here never guesses a repo's lint/test/build command. Set `require-project-checks: true` when the repository must fail closed if that command is missing. Universal checks always run first and cover manifest/hash drift, UTF-8/BOM hygiene, tracked real `.env` files and a deliberately narrow set of high-confidence secret patterns.

Local gitignored `.env`, `.env.local` and project-equivalent secret/config stores remain a supported practical workflow. The guard is against accidental tracking/publication/exposure, not against local private credential storage itself.
