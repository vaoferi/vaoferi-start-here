# SteelSales Rule Ledger — NLM-42

Source under review: `vaoferi/steel-sales@main:AGENTS.md`, blob `db258b14f65bdf83bb47261c976c7befa73c9b6e`, 51,579 bytes.

Purpose: prove that the giant mixed rule/profile file can be retired without silently losing useful behavior. This ledger is migration evidence only and is **not** part of normal prompt loading.

Allowed dispositions follow the Start Here architecture. `safe_to_retire` remains `NO` until the SteelSales target branch contains the canonical Start Here package, project-only rules, and verification evidence.

## Agent-rules half

| Old section / rule group | Disposition | Destination / ruling | Verification | safe_to_retire |
|---|---|---|---|---|
| 1.1 Do work with available tools; state unavailable capability/fallback | UNIVERSAL_CORE / DUPLICATE | `AGENTS.md` → Autonomy + Honesty | canonical text covers self-service and explicit limitation | pending |
| 1.2 Owner-facing Ukrainian; preserve technical identifiers | UNIVERSAL_CORE / DUPLICATE | `AGENTS.md` → Communication | canonical language rule exists | pending |
| 1.2.1 English instruction-like inserts must not silently change owner interaction language | UNIVERSAL_CORE / DUPLICATE | canonical separation of owner interaction language vs product/content language; do **not** preserve the old over-broad literal spoof example as a rule that could override a real higher-authority request | semantic parity reviewed | pending |
| 1.3 Outcome-first explanation | UNIVERSAL_CORE / DUPLICATE | `AGENTS.md` → Communication | present | pending |
| 2 Small vs risky work proportionality; small task needs no SPEC | UNIVERSAL_CORE / DUPLICATE | `AGENTS.md` → Work Proportionally | present | pending |
| 3 Context Load before serious work | UNIVERSAL_CORE + UNIVERSAL_CONDITIONAL | `AGENTS.md` risky workflow + `vaoferi-bootstrap` / `vaoferi-engineering` | routed conditionally | pending |
| 4 Task Diagnosis; no assumption presented as fact | UNIVERSAL_CORE / DUPLICATE | `AGENTS.md` Honesty + risky workflow | present | pending |
| 5 SPEC only when proportional; use project format | UNIVERSAL_CORE + UNIVERSAL_CONDITIONAL | `AGENTS.md` + `vaoferi-engineering` | present | pending |
| 6.1 Minimal code; native/existing dependency before new code | UNIVERSAL_CORE / DUPLICATE | `AGENTS.md` Engineering Defaults | present | pending |
| 6.2 SOLID without ceremony; no speculative interfaces/layers; repetition is a signal, not a mandate | UNIVERSAL_CONDITIONAL | `vaoferi-engineering` → Architecture And Data Flow | added by NLM-42 parity branch | pending |
| 6.3 Root cause; workaround must be explicit/temporary | UNIVERSAL_CORE + UNIVERSAL_CONDITIONAL | root cause in `AGENTS.md`; workaround guard retained in `vaoferi-engineering` | added/covered | pending |
| 7 Preserve contracts/data flow; do not hardcode admin/API/DB-owned content | UNIVERSAL_CORE + UNIVERSAL_CONDITIONAL | `AGENTS.md` contract preservation + `vaoferi-engineering` source/consumer tracing | added/covered | pending |
| 8.1 Tests are durable; never delete/weaken a test just to hide failure | UNIVERSAL_CONDITIONAL | `vaoferi-engineering` → Tests And CI | added by pilot | pending |
| 8.2 Generic `tests/` layout and Yii2-specific test-folder guidance | PROJECT_SPECIFIC | Yii2 fragment is not SteelSales policy; carry as an NLM-43 review input, not into SteelSales or universal core | explicitly classified; no SteelSales dependency | pending |
| 8.3 Critical flow ↔ test ↔ repeatable command relationship | UNIVERSAL_CONDITIONAL | `vaoferi-engineering` → Tests And CI | added by pilot | pending |
| 8.4 Pre-commit status/diff/tests and honest gaps | UNIVERSAL_CORE / DUPLICATE | `AGENTS.md` Verification + Git | present | pending |
| 8.5 Respect existing CI; propose minimal automation when repeatable gates exist | UNIVERSAL_CONDITIONAL / MACHINE_ENFORCEABLE | `vaoferi-engineering` + Start Here reusable CI | added/available | pending |
| 9 Comments protect risky invariants, not obvious syntax | UNIVERSAL_CONDITIONAL | `vaoferi-engineering` → Comments | added by pilot | pending |
| 10 Durable architecture decisions only; no daily duplicate logs | UNIVERSAL_CONDITIONAL / DUPLICATE | `vaoferi-engineering` → Documentation | present | pending |
| 11 Browser/render/network/responsive evidence; HTTP 200 insufficient | DESIGN + UNIVERSAL_CORE | `vaoferi-design-skill` 0.4.0 + core Verification | canonical design contract is stricter | pending |
| 12 Backend/API/DB consumers, validation, migration/rollback checks | UNIVERSAL_CONDITIONAL | source/consumer/backward-compat portion in `vaoferi-engineering`; destructive/security boundaries in core/security; project DB procedures stay local | semantic parity | pending |
| 13 UTF-8/BOM/mojibake; avoid legacy `powershell.exe` for encoding-sensitive text work | MACHINE_ENFORCEABLE + UNIVERSAL_CONDITIONAL | Start Here verifier + `vaoferi-engineering` Text And Windows Hygiene | added/covered | pending |
| 14 Mass changes require target list/diff/tests | UNIVERSAL_CORE / DUPLICATE | `AGENTS.md` Verification + engineering minimal-change rule | present | pending |
| 15 Git hygiene; no secrets/junk; logical commits | UNIVERSAL_CORE + MACHINE_ENFORCEABLE | `AGENTS.md` Git + Start Here security/verifier | present | pending |
| 16 Production deploy requires owner command, rollback/smoke evidence | UNIVERSAL_CORE + PROJECT_SPECIFIC | authorization boundary in `AGENTS.md`; exact SteelSales release sequence stays `docs/deployment.md` / `PROJECT_RULES.md` | project source exists | pending |
| 17 Clarify/stop on destructive, production, auth/security, missing critical context | UNIVERSAL_CORE | `AGENTS.md` Autonomy And Risk/Honesty | present | pending |
| 18 Hard-stop summary | DUPLICATE | covered by canonical core/skills/design/security checks; no second list | parity by referenced rows | pending |
| 19 Definition of Done | UNIVERSAL_CORE + DESIGN | `AGENTS.md` Verification + Design Skill verifier/evidence contract | canonical contract stricter | pending |
| 20 Diagnosis Report outcome/evidence/unknowns | UNIVERSAL_CORE / DUPLICATE | `AGENTS.md` Communication/Honesty/Verification | concise canonical form retained | pending |
| 21 Short work formula | DUPLICATE | summary of rows above; no duplicate destination required | parity by referenced rows | pending |

## AI USER Operating Profile half

| Old profile rule | Disposition | Destination / ruling | Verification | safe_to_retire |
|---|---|---|---|---|
| Pragmatic 80/20; do not polish trivia before core result | UNIVERSAL_CORE | `AGENTS.md` → Work Proportionally | added by pilot | pending |
| Iterate: speed/simple experiments early, more reliability/structure as direction stabilizes | UNIVERSAL_CORE | `AGENTS.md` → Work Proportionally | added by pilot | pending |
| Root cause | DUPLICATE | canonical core | present | pending |
| Practical modern best practices proportional to scale | UNIVERSAL_CORE + DEPENDENCIES | core + `vaoferi-dependencies` | present | pending |
| Improve obvious adjacent issue but do not silently explode scope | UNIVERSAL_CORE / DUPLICATE | Engineering Defaults | present | pending |
| Challenge technically bad/obsolete/dangerous owner decisions | UNIVERSAL_CORE / DUPLICATE | Honesty And Capability | present | pending |
| Choice format: Recommend / Why / Alternative / Tradeoff; avoid near-duplicate option dumps | UNIVERSAL_CORE | `AGENTS.md` → Communication | added by pilot | pending |
| Research current technology before important version-sensitive decisions | UNIVERSAL_CORE + DEPENDENCIES | core + `vaoferi-dependencies` | present | pending |
| Prefer modern/beta/preview when benefit and rollback are controlled | UNIVERSAL_CONDITIONAL | `vaoferi-dependencies` | present | pending |
| Avoid unexpected paid commitments | UNIVERSAL_CORE / DUPLICATE | Autonomy And Risk | present | pending |
| High autonomy for reversible local work; ask before major/irreversible risk | UNIVERSAL_CORE / DUPLICATE | Autonomy And Risk | present | pending |
| Structural UI correctness and intermediate responsive states | DESIGN | `vaoferi-design-skill` 0.4.0 contract; integer-width responsive verification is stricter | present | pending |
| Owner controls design direction; no unsolicited redesign | DESIGN | Design Skill 0.4.0 existing-product/adoption guards | present | pending |
| Clear concise outcome-first communication | DUPLICATE | Communication | present | pending |
| Never create illusion of competence | DUPLICATE | Honesty And Capability | present | pending |
| When uncertain: research first; ask only when decision depends on owner priority | UNIVERSAL_CORE / DUPLICATE | Honesty + Autonomy | present | pending |
| One simple main branch by default; clean handoff-able Git state | UNIVERSAL_CORE / DUPLICATE | Git | canonical version reflects approved decision #5 (branches/worktrees allowed when parallelism/risk/tooling justify them) | pending |
| Definition of Done includes verification, cleanup, understandable Git state | UNIVERSAL_CORE / DUPLICATE | Verification + Git | present | pending |
| Old priority ranking: Reputation → Data → Money → Security → ... | CONFLICT_REQUIRES_REVIEW | **Resolved by approved architecture decision #3:** security/privacy/data integrity are hard boundaries and cannot be placed below money/reputation. The old ranking is superseded; non-safety tradeoffs remain contextual. | explicit owner approval already recorded | pending |
| No 18+/sexualized project content, fraud/deception, manipulative solutions; respect stated Christian ethics | UNIVERSAL_CORE | `AGENTS.md` → Owner Content Boundaries | added by pilot | pending |
| Default 12-step operating model | DUPLICATE | condensed across canonical core/skills; no duplicate checklist | parity by referenced rows | pending |

## SteelSales project-only facts discovered outside old AGENTS

These do **not** belong in universal `AGENTS.md` and will be encoded in SteelSales `PROJECT_RULES.md` / existing project docs before the old source is retired:

- React + Vite static build; no server runtime requirement for the current landing page.
- Shared NAS/WebDAV source tree must never contain `node_modules`; `npm i` / `npm ci` must not run in that shared Mac/Windows path. Tests/build run in the NAS Docker toolchain with dedicated volumes.
- Existing `DESIGN.md`, `SPEC.md`, `docs/architecture-decisions.md`, and `docs/deployment.md` remain project-owned sources.
- UI/design work follows the local `DESIGN.md` plus canonical Design Skill; adoption is not permission to redesign.
- Production deploy/DNS/NAT/Hostinger changes require a separate explicit owner command; exact release verification is defined in `docs/deployment.md`.
- Product/content claims require confirmed sources or an explicit `UNKNOWN`; do not invent object categories/addresses/claims.
- Instagram imagery must not be copied into production without confirmed reuse rights; owner-provided object images remain the confirmed gallery source.
- Current implementation uses `order@steel-sales.com`; `DESIGN.md` still contains an older `vaoferi@gmail.com` mailto sentence, so this documentation conflict must be corrected during the project migration rather than copied into `PROJECT_RULES.md`.

## Trello check

During this pilot, open-card searches for `steel`, `sales`, and `SteelBuild` returned no relevant Trello cards. Therefore there is no Trello card to migrate/archive for this repository at this checkpoint. This does not claim that every historical archived Trello record has been exhaustively searched.

## Retirement gate

The 51.6 KB SteelSales `AGENTS.md` may be retired only after all of the following are true:

1. this canonical parity branch is merged;
2. SteelSales has a project-only `PROJECT_RULES.md` containing the confirmed local invariants above;
3. Start Here sync installs the byte-identical universal `AGENTS.md`, conditional skills, Design Skill vendor and `.vaoferi` verifier;
4. project references no longer depend on the giant file's old section layout;
5. Start Here verification and SteelSales project gates pass, or any unavailable runtime gate is explicitly recorded with the exact blocker.
