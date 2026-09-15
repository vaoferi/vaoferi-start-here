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
