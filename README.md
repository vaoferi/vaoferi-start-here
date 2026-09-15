# Vaoferi Start Here

Public canonical source for Vaoferi-wide AI-agent behavior, conditional local skills and repository bootstrap/sync rules.

## Source-of-truth model

- `AGENTS.md` — compact universal owner/agent contract copied byte-for-byte into participating repositories.
- `PROJECT_RULES.md` — rules for this repository only; each target repository owns its own `PROJECT_RULES.md`.
- `.agents/skills/vaoferi-*` — conditional procedures loaded only when relevant.
- `vaoferi-design-skill` — separate canonical design source, vendored here later for local/offline use.
- Linear — active work tracker. Trello — legacy read-and-retire input only.

The target architecture is intentionally local-first: after bootstrap, ordinary work in a target repository must not depend on network access to this repository.

## Development

Requires Python 3.11+ and no runtime dependencies for the core tooling.

```bash
python -m unittest discover -s tests -v
python scripts/check_agents_contract.py AGENTS.md
```

## Reusable GitHub checks

Target repositories can call the shared verification workflow from a reviewed Start Here release/tag:

```yaml
jobs:
  vaoferi:
    uses: vaoferi/vaoferi-start-here/.github/workflows/vaoferi-checks.yml@v0.1.0
    with:
      require-project-checks: true
      project-check-command: npm test
```

`project-check-command` is project-owned: Start Here never guesses a repo's lint/test/build command. Set `require-project-checks: true` when the repository must fail closed if that command is missing. Universal checks always run first and cover manifest/hash drift, UTF-8/BOM hygiene, tracked real `.env` files and a deliberately narrow set of high-confidence secret patterns.
