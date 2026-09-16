# nlm.help Rule Review Addendum — 2026-09-16

This addendum records evidence discovered after `migration/rule-ledger/nlm.help.md`. It is migration evidence, not normal agent prompt material.

## Additional active/stale source discovered

`vaoferi/nlm.help@master:docs/core/PROJECT_RULES.md`, blob `693d84c7592e5f5183a1846a33830d3b3adaafd6`.

Disposition: `DUPLICATE + STALE_SOURCE + CONFLICT_REQUIRES_REVIEW`, with a future `DELETE_CANDIDATE` gate only after its unique useful content is migrated or explicitly rejected.

Why it cannot remain an active rules source:

- it duplicates large parts of root `PROJECT_RULES.md`;
- it mandates every useful MCP, a fixed Context7→Sequential Sync→Cloud Context→Memory pipeline, Chrome DevTools + Playwright for every code task, and a checklist for every task; these conflict with the approved proportional/conditional-loading architecture;
- it contains old provider/tool names and paths that are version-sensitive;
- it contains the same over-broad `View Transition API` mandate and 44px touch target;
- most importantly, its environment topology says NAS is only a backup mirror and development is Windows→GitHub→NAS, while current root `PROJECT_RULES.md` and `DOCUMENTATION_MAP.md` define `\\NAS\homes\vaoferi\Work\nlm\public_html` as the canonical working Yii2 tree and GitHub as versioned remote/history.

Ruling for topology: current root `PROJECT_RULES.md` + `DOCUMENTATION_MAP.md` win. `docs/core/PROJECT_RULES.md` is not listed by the current documentation map as an active source and must not override current project rules.

Useful content that must not be silently lost before retirement:

- `ru == ua` / `/ru` and `/uk` redirect behavior;
- Yii2/Hyper/Bootstrap facts and frontend/backend separation;
- HTML/CSS/PHP/security guidance that is either project-specific or already covered by canonical engineering/security/design skills;
- historical technical-debt candidates: Composer 2, `facebook/graph-sdk`, `yiisoft/yii2-bootstrap5`, external team styles. These are **not** active requirements until revalidated against current dependency state;
- documentation/history and backup-suffix conventions where still current;
- responsive intent, after reconciliation with canonical Design Skill and the owner-wide 48px target.

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

Disposition: old 44px rule = `SUPERSEDED`; future NLM project rules/design references should say 48px.

## CLAUDE.md comparison checkpoint

Windowed comparison of current `AGENTS.md` and `CLAUDE.md` shows:

- lines through the generic deploy section are identical in the inspected ranges;
- `AGENTS.md` contains an NLM-only subsection `16.1. Буквальний порядок команд для Windows, NAS і production` with exact NAS/deploy/migration commands and local secret-loader paths;
- `CLAUDE.md` jumps directly from generic deploy rules to section 17;
- the later sections (17–23, MCP inventory, related files) match in the inspected ranges apart from the line shift caused by that insertion.

Repository search for the `16.1` heading returns `AGENTS.md`, not `CLAUDE.md`.

Current conclusion: the only **substantive delta found** is the NLM deploy subsection. Do not call the files byte-identical; exact byte-level parity has not been proven by a local diff. The missing subsection is project-specific and already belongs in NLM deploy/project rules, not in a future Claude overlay.

## Trello cards encountered during NLM-43

No board sweep was performed.

- `[00][BOARD-RULES]`: full description + its one comment read; no checklists/attachments. Unique useful behavior mapped into canonical Start Here/NLM rules and recorded in Linear NLM-43. Card archived because the current connector has no hard-delete action; archive is pending-delete, not a permanent archive.
- `[CLI S] [Процес/Lightrack]`: full card read; no comments/checklists/attachments. Active work and all unique requirements are in Linear NLM-36. Card archived for the same connector limitation.

No other Trello card enters scope merely because it exists on the board.
