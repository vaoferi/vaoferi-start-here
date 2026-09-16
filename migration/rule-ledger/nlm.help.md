# nlm.help Rule Ledger — NLM-43

Primary sources under review:

- `vaoferi/nlm.help@master:AGENTS.md` — blob `9581780cf8fe376ead6efa3662b6a9808ae12550`.
- `vaoferi/nlm.help@master:CLAUDE.md` — blob `2fa6efd0cd04639af5bd5e4c28a61e5aaeee0d56`.
- `vaoferi/nlm.help@master:PROJECT_RULES.md` — blob `34a16455b90464d1ebf92667ab7c09c411309323`.
- `vaoferi/nlm.help@master:.gemini_rules.md` — blob `a597b59ecf8609a6721741b337c8326b82392f2c`.
- `vaoferi/nlm.help@master:DOCUMENTATION_MAP.md` — project-owned source map; Trello policy corrected by commit `f0cc6171d022c6fb0d02851564b77ec4c0e57b3c`.

Purpose: separate universal Vaoferi behavior from NLM-only Yii2/NAS/deploy/business constraints without silently dropping a rule. This ledger is migration evidence only; it is not normal prompt material.

Allowed dispositions: `UNIVERSAL_CORE`, `UNIVERSAL_CONDITIONAL`, `PROJECT_SPECIFIC`, `DESIGN`, `PROVIDER_OVERLAY`, `MACHINE_ENFORCEABLE`, `DUPLICATE`, `CONFLICT_REQUIRES_REVIEW`, `DELETE_CANDIDATE`. A delete candidate is not deleted until its useful meaning is proven covered or explicitly rejected.

`safe_to_retire` remains `NO` for old instruction files until the target repository has the synced Start Here package, project-owned replacement rules, provider overlay(s), reference parity and verification evidence.

## AGENTS.md

| Old rule group | Disposition | Destination / ruling | safe_to_retire |
|---|---|---|---|
| 1.1 use available tools; do not delegate avoidable work; explicit blocker/fallback | UNIVERSAL_CORE / DUPLICATE | canonical `AGENTS.md` Autonomy + Honesty | pending |
| 1.2 owner-facing Ukrainian; keep technical identifiers original | UNIVERSAL_CORE / DUPLICATE | canonical `AGENTS.md` Communication | pending |
| 1.3 explain user/process outcome before internals | UNIVERSAL_CORE / DUPLICATE | canonical Communication | pending |
| 2 small-safe vs serious-risky workflow; no mandatory SPEC for tiny work | UNIVERSAL_CORE / DUPLICATE | canonical Work Proportionally | pending |
| 3 Context Load | UNIVERSAL_CORE + UNIVERSAL_CONDITIONAL | canonical risky workflow + `vaoferi-bootstrap` / `vaoferi-engineering`; project-specific files are supplied by `PROJECT_RULES.md` / source map | pending |
| 4 Task Diagnosis; do not present guesses as facts | UNIVERSAL_CORE / DUPLICATE | canonical Honesty + risky workflow | pending |
| 5 proportional SPEC | UNIVERSAL_CORE + UNIVERSAL_CONDITIONAL | canonical Work Proportionally + engineering skill | pending |
| 6.1 reuse existing/native/dependency before new code | UNIVERSAL_CORE / DUPLICATE | canonical Engineering Defaults | pending |
| 6.2 SOLID without ceremony | UNIVERSAL_CONDITIONAL / DUPLICATE | `vaoferi-engineering` | pending |
| 6.3 root cause; workaround only as explicit emergency measure | UNIVERSAL_CORE + UNIVERSAL_CONDITIONAL | canonical Engineering Defaults + engineering skill | pending |
| 7 preserve admin→frontend, service→DB, API/auth/routes/media/config contracts; do not hardcode admin-owned content | UNIVERSAL_CORE + UNIVERSAL_CONDITIONAL + PROJECT_SPECIFIC | generic contract preservation in Start Here; exact NLM data flows remain project docs/tests | pending |
| 8.1 tests are durable; do not weaken/delete to hide failure | UNIVERSAL_CONDITIONAL / DUPLICATE | `vaoferi-engineering` | pending |
| 8.2 `TESTING.md`, Yii2 `tests/` location | PROJECT_SPECIFIC | NLM `TESTING.md` / project rules | pending |
| 8.3 critical flow ↔ test ↔ repeatable command | UNIVERSAL_CONDITIONAL + PROJECT_SPECIFIC | engineering skill + NLM `TESTING.md` / `docs/critical-flows.md` | pending |
| 8.4 pre-commit status/diff/relevant tests/honest gaps | UNIVERSAL_CORE / DUPLICATE | canonical Verification + Git | pending |
| 8.5 respect CI; add minimal repeatable automation when absent | UNIVERSAL_CONDITIONAL + MACHINE_ENFORCEABLE | engineering skill + project CI | pending |
| 9 comments protect non-obvious risky invariants, not obvious syntax | UNIVERSAL_CONDITIONAL / DUPLICATE | engineering skill | pending |
| 10 durable architecture decisions; no daily duplicate log | UNIVERSAL_CONDITIONAL + PROJECT_SPECIFIC | engineering docs rule; NLM ADR/project-log policy stays local | pending |
| 11 UI requires render/Console/Network/interaction/responsive evidence; HTTP 200 insufficient | UNIVERSAL_CORE + DESIGN | canonical Verification + `vaoferi-design-skill` | pending |
| 12 backend/API/DB tests, consumers, validation, permissions, migration/rollback | UNIVERSAL_CONDITIONAL + PROJECT_SPECIFIC | engineering/security generic rules; NLM DB migration procedure local | pending |
| 13 UTF-8/no BOM/mojibake; avoid legacy `powershell.exe` for encoding-sensitive text | UNIVERSAL_CONDITIONAL + MACHINE_ENFORCEABLE | engineering skill + verifier where practical | pending |
| 14 mass changes need target list/diff/tests | UNIVERSAL_CORE / DUPLICATE | canonical Verification | pending |
| 15 Git status/diff, no secrets/junk, one logical change | UNIVERSAL_CORE / DUPLICATE | canonical Git | pending |
| 16 generic production authorization, diff/tests/backup/rollback/smoke | UNIVERSAL_CORE + PROJECT_SPECIFIC | authorization boundary in canonical core; NLM deploy sequence stays local | pending |
| 16.1 exact Windows/NAS/deploy/migration commands and secret-loader paths | PROJECT_SPECIFIC | NLM deploy/migration skills/runbooks, not universal `AGENTS.md` | pending |
| 17 clarify/stop on destructive risk, missing critical context, unavailable verification | UNIVERSAL_CORE / DUPLICATE | canonical Honesty + Autonomy | pending |
| 18 hard-stop summary | DUPLICATE | covered by canonical core/skills + NLM project rules | pending |
| 19 Definition of Done | UNIVERSAL_CORE + DESIGN + PROJECT_SPECIFIC | canonical Verification + design skill + NLM runtime gates | pending |
| 20 Diagnosis Report | UNIVERSAL_CORE / DUPLICATE | canonical Communication/Honesty/Verification; no need to preserve exact long template | pending |
| 21 short work formula | DUPLICATE | summary of prior rows | pending |
| 22 MCP server inventory, Codebuff startup/config locations | PROVIDER_OVERLAY + PROJECT_SPECIFIC | thin provider/tool overlay or NLM MCP docs; do not place in universal core | pending |
| 23 related-files list | PROJECT_SPECIFIC / DUPLICATE | `DOCUMENTATION_MAP.md` should be the concise routing source | pending |

## PROJECT_RULES.md

| Current rule group | Disposition | Destination / ruling | safe_to_retire |
|---|---|---|---|
| Pre-flight: read rules; UI reuse existing snippets/components | PROJECT_SPECIFIC + DESIGN | NLM project routing + design skill; exact `snippets`/legacy path local | keep/project |
| `ru == ua`; Ukrainian DB content under legacy `ru`; no parallel `ua` data logic | PROJECT_SPECIFIC + MACHINE_ENFORCEABLE | NLM hard invariant in `PROJECT_RULES.md`, localization tests/URL manager | keep/project |
| autonomy, Ukrainian owner communication, root cause, architecture safety, reuse existing logic | UNIVERSAL_CORE / DUPLICATE | canonical Start Here | migrate out of project file after target sync |
| UTF-8/mojibake | UNIVERSAL_CONDITIONAL + MACHINE_ENFORCEABLE | Start Here engineering/verifier; NLM-specific encoding incidents may remain in project docs | pending |
| Caveman comments / no AI traces | UNIVERSAL_CONDITIONAL + PROJECT_SPECIFIC | concise-comment principle is universal; exact stylistic wording can be dropped after parity | pending |
| CSS layering, no `!important`, mobile-first, no horizontal scroll | DESIGN + PROJECT_SPECIFIC | design skill + NLM frontend facts | pending |
| pre-command time/volume estimate and chunking for timeout risk | UNIVERSAL_CONDITIONAL | engineering skill; preserve only concise behavior | pending |
| code priority readable→safe→minimal | UNIVERSAL_CONDITIONAL | engineering skill; security remains hard boundary in core | pending |
| owner/site texts are source-controlled; do not invent copy | PROJECT_SPECIFIC | NLM content/editorial rule | keep/project |
| charity visual style: restrained/informational/not cartoonish | PROJECT_SPECIFIC + DESIGN | local design/product constraint | keep/project |
| mandatory `View Transition API` for page transitions | CONFLICT_REQUIRES_REVIEW | over-broad technology mandate; verify actual support/usage before retaining, moving, or deleting | NO |
| mandatory checklist before every task | CONFLICT_REQUIRES_REVIEW | conflicts with approved proportional-work rule for tiny safe tasks; likely replace with proportional checklist, but do not delete silently | NO |
| post-update cache/CDN recommendations | PROJECT_SPECIFIC / CONDITIONAL | keep only where release/cache behavior actually requires it | pending |
| Context7 for current external docs; GitHub/history for project history; web when facts missing | UNIVERSAL_CONDITIONAL + PROJECT_SPECIFIC | bootstrap/engineering routing; exact project history paths stay local | pending |
| up to 3 clarification questions before risky changes | UNIVERSAL_CORE / DUPLICATE | canonical Autonomy/Risk already asks only true missing decisions; exact numeric cap is not necessary unless owner reaffirms | pending |
| Chrome DevTools + Playwright after code | DESIGN/TESTING + PROJECT_SPECIFIC | require proportional real browser evidence; do not force both tools for every non-UI change | pending |
| `docs/history/project_log.md`, `.kiro/specs/` active-only, history not active instructions, suffix `_` backups | PROJECT_SPECIFIC | NLM documentation lifecycle | keep/project |
| deploy chain `push master → preview → visual verify → explicit prod` and external preview URLs | PROJECT_SPECIFIC + MACHINE_ENFORCEABLE | NLM deploy runbooks/skills/CI | keep/project |
| local/preview/prod URL restrictions; HTTP 200/curl not enough | PROJECT_SPECIFIC + DESIGN | project environment + canonical verification | keep/project |
| migration gate: fresh prod DB pull + media sync → local migrate → real DB/browser → prod migrate | PROJECT_SPECIFIC + MACHINE_ENFORCEABLE | NLM migration skill/scripts/tests | keep/project |
| NotebookLM archive-only, never a documentation blocker | PROJECT_SPECIFIC | NLM source map/project rules | keep/project |
| NAS-only existing containers; no replacement local Docker stacks | PROJECT_SPECIFIC + MACHINE_ENFORCEABLE | NLM infra rules/checks | keep/project |
| PORT_BAN 8083 and only external 18083 route | PROJECT_SPECIFIC + MACHINE_ENFORCEABLE | NLM project rule + grep/test gate | keep/project |
| DoD visual/backend/runtime checks | UNIVERSAL_CORE + DESIGN + PROJECT_SPECIFIC | canonical Verification + design skill + NLM TESTING/runtime | pending |
| development goals: root cause, backward compatibility, modern stack, minimal change | UNIVERSAL_CORE + PROJECT_SPECIFIC | generic pieces canonical; exact stack local | pending |
| Yii2 Starter Kit; Hyper BS5 admin; mixed BS3/CSS front | PROJECT_SPECIFIC | NLM stack facts | keep/project |
| HTML semantics/Bootstrap discipline | DESIGN + PROJECT_SPECIFIC | design skill generic principles + NLM Bootstrap facts | pending |
| CSS discipline/component organization | DESIGN + PROJECT_SPECIFIC | design skill/local frontend rules | pending |
| JS/TS service layer, error handling, no sensitive LocalStorage | UNIVERSAL_CONDITIONAL + SECURITY + PROJECT_SPECIFIC | engineering/security skill; exact stack conventions local | pending |
| PHP validation/prepared SQL/XSS/CSRF/file validation | UNIVERSAL_CONDITIONAL + SECURITY + PROJECT_SPECIFIC | security/engineering generic rules + Yii2 local conventions | pending |
| Yii2 controller/service/model/view separation | PROJECT_SPECIFIC + UNIVERSAL_CONDITIONAL | NLM Yii2 conventions; consult project Yii2 documentation before implementation changes | keep/project |
| security: hashing/tokens/log hygiene/.env/RBAC hostile input | UNIVERSAL_CONDITIONAL + SECURITY | `vaoferi-security`; NLM exact auth/RBAC sources stay local | pending |
| locale/URL map `ua/en/de`, internal `ru`, redirects, helpers/params sync | PROJECT_SPECIFIC + MACHINE_ENFORCEABLE | NLM localization rules/tests | keep/project |
| frontend view paths, inline asset limits, cache-busting, Masonry dependency caution | PROJECT_SPECIFIC | local frontend constraints | keep/project |
| backend Hyper asset/layout and Bootstrap5 widgets | PROJECT_SPECIFIC | local backend constraints | keep/project |
| MCP proxy topology, credential catalog/helper, Hostinger-only prod change path | PROJECT_SPECIFIC + PROVIDER_OVERLAY + SECURITY | NLM MCP docs/runbooks/provider overlays; never copy credential values | keep/project |
| responsive charter 200–7680, breakpoints/layout examples | DESIGN + PROJECT_SPECIFIC | review against canonical `vaoferi-design-skill`; retain NLM-specific facts only | pending |
| 44px touch target | CONFLICT_REQUIRES_REVIEW | owner-wide preferred target is 48px; NLM should not silently lower it to 44px | NO |
| environment topology: NAS working tree + GitHub versioned history; reconcile drift explicitly | PROJECT_SPECIFIC | NLM `PROJECT_RULES.md` / `DOCUMENTATION_MAP.md` | keep/project |
| NAS workspace roles and sync exclusions | PROJECT_SPECIFIC + MACHINE_ENFORCEABLE | NLM project/infra docs | keep/project |

## CLAUDE.md

Current file starts as a copy of the old `AGENTS.md`, but has a different blob SHA. Treat it as `DUPLICATE_CANDIDATE`, not proven byte-identical.

Required migration before retirement:

1. compare complete `CLAUDE.md` against `AGENTS.md` and identify every delta;
2. universal behavior must come from synced root `AGENTS.md` / conditional skills;
3. genuine Claude-only tool/approval quirks move to a thin provider overlay;
4. NLM-only facts stay in project rules/runbooks;
5. only then replace the giant copy with a thin adapter/router or delete it if the provider no longer needs it.

`safe_to_retire = NO` until exact diff parity exists.

## .gemini_rules.md

| Rule | Disposition | Destination / ruling |
|---|---|---|
| overlay does not replace project/root rules; stop on conflict | PROVIDER_OVERLAY | canonical `templates/provider/gemini.md` already establishes this contract |
| avoid `run_command` for simple file read/search/edit; prefer Gemini native file tools | PROVIDER_OVERLAY | retain only if still true for current Gemini/Antigravity environment; provider-version-sensitive |
| warn that terminal may await approval | PROVIDER_OVERLAY | retain if current provider UX still behaves this way |
| do not rewrite MCP/IDE config merely because tool is not visible; verify availability first | UNIVERSAL_CORE + PROVIDER_OVERLAY | Honesty/capability + Gemini-specific discovery |
| do not rewrite `.vscode/.gemini/mcp_config` without direct permission | PROVIDER_OVERLAY + PROJECT_SPECIFIC | provider config safety; exact project files local |
| UTF-8/no BOM; native file tools before shell mass replace; do not infer mojibake from one terminal output | UNIVERSAL_CONDITIONAL + PROVIDER_OVERLAY | engineering hygiene + provider preference |
| Diagnosis Report template | DUPLICATE | canonical concise report behavior; no separate full template required |

Before changing this overlay, verify current Gemini/Antigravity tool names and approval behavior. Do not preserve obsolete tool names as universal doctrine.

## DOCUMENTATION_MAP.md

Disposition: `PROJECT_SPECIFIC` and **keep**. It is the concise NLM routing map, not a universal rules file.

Key invariants that must survive:

- NLM working tree/domain/deploy routing and project sources;
- Linear is the only active task source of truth;
- Trello is incremental legacy input only, not planner/archive; no standalone board sweep unless explicitly requested; relevant cards are read → migrated/used → parity → deleted;
- identity/staff/recipient/public-team/CarePerson boundaries;
- aid invitation current source chain and campaign #14 guard;
- face-recognition canonical sources and CompreFace tombstone behavior;
- mercy-case current sources;
- specs/history lifecycle hygiene;
- UI `ua/en/de` + legacy data `ru == ua`.

## Trello cards encountered by this migration

Do not sweep the board. Only cards directly encountered by the current work are eligible for retirement after parity.

- `[00][BOARD-RULES] Послідовність роботи агентів і Trello MCP`: useful owner/process principles are either represented by canonical Start Here (outcome-first, simple main workflow, proportional work) or are superseded by later approved architecture (branches/worktrees allowed when justified; Linear is active truth). Before archive/delete, do one final full-card read and record parity in NLM-43.
- `[CLI S] [Процес/Lightrack] Знайти канонічні skills і підключити їх до правил агентів`: active work is represented by Linear `NLM-36`; before archive/delete, confirm card has no unique comments/checklists/attachments not already in NLM-36.

No other Trello card is pulled into scope merely because it appeared in a historical inventory.

## Current migration blockers / review decisions

1. `View Transition API` mandatory rule — keep/revise/delete decision required after checking current implementation and design contract.
2. mandatory checklist for every task vs proportional workflow — resolve toward one non-contradictory rule.
3. 44px NLM touch target vs owner-wide 48px preference — resolve before final project rule rewrite.
4. `CLAUDE.md` exact delta must be calculated before retirement.
5. Provider-specific Gemini behavior must be checked against the current provider before copying tool names.
6. Old NLM `AGENTS.md` must not be replaced until all NLM-only deploy/NAS/localization/MCP rules have stable project-owned destinations.

## Retirement gate

Old mixed instruction files may be retired only when:

1. byte-identical canonical Start Here `AGENTS.md` and conditional skills are installed in `nlm.help`;
2. project-only Yii2/NAS/deploy/migration/localization/business rules remain in project-owned sources;
3. provider overlays are thin and no longer duplicate universal doctrine;
4. references to old section layouts are updated;
5. Start Here verification + NLM project gates pass, or unavailable runtime verification is explicitly recorded with the exact blocker;
6. the ledger has no unreviewed rule group and no unresolved `DELETE_CANDIDATE` hidden by omission.
