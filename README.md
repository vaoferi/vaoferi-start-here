# Vaoferi Start Here

**Current release: 0.2.5**

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

## 0.2.5: Fail-closed production deployment

This release turns production publication into a centrally-routed conditional workflow via `vaoferi-deploy`.

The contract is based on repeated real deployment failure modes and separates evidence into explicit layers:

`candidate → preview parity → target identity → rollback → upload → remote read-back → effective origin → CDN/cache → browser/user behavior`.

Key rules:

- verify required tooling, browser runtime, Git push path, provider access and deploy-config schema before spending hours on a release;
- never deploy an unidentified “latest” branch/build: record the exact pushed SHA, artifact/release identity and included/excluded work;
- prove the transport target maps to the intended effective production root before mutation;
- FTP/transport upload or read-back is not public-origin proof;
- a DEV/HMR page is not evidence for a reviewed static candidate;
- rollback evidence must cover the production content that can actually be overwritten; a local candidate snapshot is not a production preimage;
- upload/read-back, origin, CDN/cache and browser behavior are distinct verification layers;
- cache purge is not a fix for an origin that still serves the wrong artifact;
- public `HTTP 200` or an application root does not prove the reviewed candidate is live;
- after a failed deploy attempt, record the hypothesis, result, what was ruled out and the changed precondition required before repeating the same write-capable action;
- the next executor resumes from the last proven frontier instead of restarting deployment archaeology;
- sequential/atomic/multi-root behavior remains project-specific; the universal contract does not impose one release topology.

Each deployable repository keeps its own canonical deploy/runbook facts. Start Here owns the process; the repository owns domains, provider, transport, roots, config names, preview identity, rollback and provider-specific publication behavior.

## 0.2.4: Remote handoff + durable credential redundancy

This release makes review freshness and credential availability hard workflow invariants.

- every repository-scoped Linear task requires **commit + push** before `In Review` or `Done`;
- the Linear handoff records the exact **pushed SHA** and reviewer verifies that remote commit/diff independently;
- a local-only commit is never review-ready evidence;
- if a repository-scoped task has no file delta, it still uses an explicit pushed task-evidence commit so the reviewer has remote traceability;
- validated credentials use two controlled canonical copies:
  - **Vaultwarden** is the global inventory/backup for all projects and infrastructure;
  - project-root `.env` contains only credentials required by that project;
- when an agent discovers and actually validates a working credential, it persists it without waiting for the owner to re-enter it:
  - current project needs it → BOTH Vaultwarden + project-root `.env`;
  - current project does not need it → Vaultwarden only;
- `.env.example`/docs contain variable names and non-secret references only;
- real `.env` remains private/gitignored and secret values are never echoed to Linear/chat/docs/logs;
- if Vaultwarden write access is unavailable, the agent must report the persistence gap instead of pretending the backup succeeded;
- a secret found in tracked/shared/public code is still an exposure: preserve availability first, then flag rotation/remediation without silently destroying the working credential.

The sync package already centrally owns:
- `AGENTS.md`;
- `.agents/skills/vaoferi-security/SKILL.md`;
- `.agents/skills/vaoferi-task-tracking/SKILL.md`.

Therefore the next canonical `vaoferi_sync.py update` propagates these rules into participating repositories.

## 0.2.3: Executor ↔ Reviewer protocol

This release makes independent review a first-class part of the universal workflow.

- `In Review` means **Ready for Review**, never “the executor got stuck”.
- blocked/failed work stays `In Progress` with a detailed blocked handoff;
- blocked handoff preserves expected vs actual behavior, exact reproduction, failed attempts, errors/evidence, inspected files/functions/commits, what was ruled out, and the next recommended experiment;
- reviewer selection is **blocked-first**, then ordinary `In Review`; one issue per run;
- reviewer independently checks Linear + GitHub + Opera Browser Connector + Context7 relevance + Superpowers instead of trusting executor summaries;
- owner-requested `Wayfinder` and `I have ADHD` helpers are explicit preflight items: use them when the harness exposes them, otherwise report them unavailable rather than pretending;
- review FAIL returns/keeps the issue in `In Progress`; full independent PASS with no owner-only gate may move to `Done`; owner-only visual/business acceptance keeps the issue in `In Review`;
- Linear history is never auto-deleted by the reviewer loop.

Canonical reviewer prompt:
`templates/reviewer/linear-reviewer.md`

The prompt is cadence-neutral. ChatGPT scheduled tasks currently support a maximum recurring frequency of once per hour, so a 30-minute reviewer cadence cannot be created directly by ChatGPT Tasks.

## 0.2.2: Fail-closed acceptance and Codex global guardrails

This release hardens the boundary between “code exists” and “user-facing work is actually verified”.

Key rules now fail closed:

- every relevant acceptance criterion needs its own evidence before `In Review` / `Done`;
- user-action criteria must be exercised on the real topmost user-facing target in a rendered/runtime surface;
- source/string/DOM-presence checks are supplementary, not substitutes for behavioral proof;
- required browser/runtime unavailable means `BLOCKED`, not a soft warning;
- behavior changes and bug fixes use TDD RED → minimal GREEN → regressions;
- reviewer-facing UI/runtime work must point to the exact SHA/version on a current reviewer-accessible artifact;
- `VISUAL APPROVAL`, browser verification and authored-UI `!important` hard-stop rules are mirrored in the compact Codex global guardrails.

### Codex global instructions

Codex reads global instructions from `$CODEX_HOME/AGENTS.md`; when `CODEX_HOME` is unset, the default home is `~/.codex`. Repository `AGENTS.md` / `PROJECT_RULES.md` are then layered with the project context.

The canonical compact Vaoferi mirror is `templates/provider/codex.md`. Install and verify its managed block with:

```bash
python scripts/codex_global.py status
python scripts/codex_global.py install
python scripts/codex_global.py verify
```

The installer is fail-closed:

- missing/empty global file → create the managed block;
- existing managed Vaoferi block → update only that block and preserve surrounding personal content;
- existing non-empty unmanaged `AGENTS.md` → refuse to overwrite so an agent/owner can reconcile it intentionally;
- `verify` fails on missing/drifted managed content.

Use `--codex-home /path/to/home` for an explicit profile. The global block stays small and universal; project-specific paths, ports and product facts stay out of it.

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
