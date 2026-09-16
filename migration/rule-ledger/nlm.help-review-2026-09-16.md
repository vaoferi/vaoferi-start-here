# nlm.help Rule Review Addendum — 2026-09-16

This addendum records evidence discovered after `migration/rule-ledger/nlm.help.md`. It is migration evidence, not normal agent prompt material.

## Additional active/stale source discovered

`vaoferi/nlm.help@master:docs/core/PROJECT_RULES.md`, blob `693d84c7592e5f5183a1846a33830d3b3adaafd6`.

Disposition: `DUPLICATE + STALE_SOURCE + CONFLICT_REQUIRES_REVIEW`, then `DELETE_CANDIDATE` after its unique useful content was classified.

Why it cannot remain an active rules source:

- it duplicates large parts of root `PROJECT_RULES.md`;
- it mandates every useful MCP, a fixed Context7→Sequential Sync→Cloud Context→Memory pipeline, Chrome DevTools + Playwright for every code task, and a checklist for every task; these conflict with the approved proportional/conditional-loading architecture;
- it contains old provider/tool names and paths that are version-sensitive;
- it contains the same over-broad `View Transition API` mandate and 44px touch target;
- most importantly, its environment topology says NAS is only a backup mirror and development is Windows→GitHub→NAS, while current root `PROJECT_RULES.md` and `DOCUMENTATION_MAP.md` define `\\NAS\homes\vaoferi\Work\nlm\public_html` as the canonical working Yii2 tree and GitHub as versioned remote/history.

Ruling for topology: current root `PROJECT_RULES.md` + `DOCUMENTATION_MAP.md` win. `docs/core/PROJECT_RULES.md` is not listed by the current documentation map as an active source and must not override current project rules.

Useful content was classified before retirement:

- `ru == ua` / `/ru` and `/uk` redirect behavior stays project-specific;
- Yii2/Hyper/Bootstrap facts and frontend/backend separation stay project-specific;
- generic HTML/CSS/PHP/security guidance is covered by canonical engineering/security/design skills where appropriate;
- historical technical-debt candidates such as Composer 2, `facebook/graph-sdk`, `yiisoft/yii2-bootstrap5`, and external team styles are not active requirements until revalidated against current dependency state;
- documentation/history and backup-suffix conventions remain project-owned where current;
- responsive intent is reconciled with canonical Design Skill and the owner-wide 48px target.

Pilot ruling: the stale duplicate was removed from `nlm-43-start-here-pilot` after classification so agents cannot accidentally load contradictory topology.

## Conflict resolutions

### 1. View Transition API

Evidence: current code uses `document.startViewTransition` in `backend/web/js/theme-manager/ThemeManager.js` behind a support/enablement check. Repository search did not show it as a general site-wide page-navigation contract.

Resolution:

- **do not keep** `Use View Transition API` as a mandatory universal or NLM-wide rule;
- preserve existing working use where a component already supports it and it improves the interaction;
- new UI may use it when appropriate and supported, with graceful fallback;
- do not add it merely to satisfy an instruction file.

Disposition of old mandatory sentence: `DELETE_CANDIDATE`, evidence-backed and superseded by the design/engineering rule above.

### 2. Mandatory checklist for every task

Resolution: superseded by approved proportional workflow.

- small safe task: inspect → minimal change → smallest useful verification → report;
- risky/architectural work: explicit plan/checklist/SPEC when useful;
- do not create ceremony solely to satisfy a checklist rule.

Disposition: old always-checklist mandate = `DELETE_CANDIDATE`; useful intent (do not lose steps on complex work) is preserved by canonical Work Proportionally / engineering workflows.

### 3. 44px vs 48px touch targets

Owner-wide project instruction is 48px minimum for important touch targets. Therefore NLM's old 44px rule is stale.

Resolution: use **48px preferred minimum** for interactive touch targets; a smaller platform/library standard is only an explicit exception when the existing component/system requires it and usability remains acceptable.

Disposition: old 44px rule = `SUPERSEDED`; canonical Design Skill now carries the 48px preference.

## Provider files

### CLAUDE.md

Windowed comparison of the old `AGENTS.md` and `CLAUDE.md` showed the only substantive delta found was the NLM-only deploy subsection `16.1. Буквальний порядок команд для Windows, NAS і production`; later sections matched apart from the line shift.

That subsection is project-specific and belongs in NLM deploy/project rules, not in a provider file. Pilot `CLAUDE.md` is therefore reduced to a thin router to root/project rules rather than retaining a second giant copy.

### .gemini_rules.md

Pilot overlay is reduced to provider/runtime quirks only:

- native file/search tools preferred for simple file work when available;
- terminal actions may wait for Gemini/Antigravity approval;
- verify actual tool availability before declaring MCP unavailable;
- do not rewrite IDE/MCP config merely because a tool is not visible in one context;
- preserve UTF-8/no-BOM and avoid diagnosing mojibake from one bad terminal rendering.

Universal engineering/design/security/dependency/task-tracking and NLM project rules are no longer duplicated there.

## Trello cards encountered during NLM-43

No board sweep was performed.

- `[00][BOARD-RULES]`: full description + its one comment read; no checklists/attachments. Unique useful behavior mapped into canonical Start Here/NLM rules and recorded in Linear NLM-43. Card archived/closed after parity because the current connector has no hard-delete action.
- `[CLI S] [Процес/Lightrack]`: full card read; no comments/checklists/attachments. Active work and all unique requirements are in Linear NLM-36. Card archived/closed after parity for the same connector limitation.

Current owner rule: hard-delete after parity when supported; otherwise archive/close and continue. Physical delete is not a separate blocker. No other Trello card enters scope merely because it exists on the board.

## Pilot rollout evidence

Pilot branch: `vaoferi/nlm.help@nlm-43-start-here-pilot`.

The real repository was bootstrapped against `vaoferi-start-here` source commit `a73f1de71e13a0b2676d4811c23c1bd994e4b328`, version `0.1.0`. `.vaoferi/manifest.json` records exact hashes for:

- canonical root `AGENTS.md`;
- five conditional skills;
- the full pinned/vendored `vaoferi-design-skill` snapshot;
- `.vaoferi/verify.py`.

The pilot exposed one universal verifier bug: safe named templates such as `.env.vault.example` were incorrectly treated as real env files. A failing central test was added first, then the canonical verifier was fixed to allow `.example`, `.sample`, and `.template` suffixes while still rejecting real `.env` / `.env.*` files. Central `Start Here self-test` passed on commit `a73f1de71e13a0b2676d4811c23c1bd994e4b328`.

NLM pilot sync/verify then passed against that same canonical commit. The generated manifest was committed by the pilot automation. The temporary self-mutating sync workflow is removed before merge, and NLM now has a permanent reusable verification workflow pinned to the exact reviewed canonical SHA.
