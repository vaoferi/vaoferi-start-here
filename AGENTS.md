# AGENTS.md

Універсальний контракт AI-агента з власником Vaoferi repositories. Він однаковий у підключених проєктах; project facts живуть у `PROJECT_RULES.md` та project-owned docs.

`DEFINITION_OF_DONE.md` — centrally-owned обов'язковий completion contract для всіх repository-scoped IMPLEMENTATION задач. Project rules можуть його тільки посилювати, але не послаблювати без explicit owner decision.

## Communication

- Усі видимі плани, діагностика, питання, SPEC і звіти власнику — українською; product/code language не підміняй мовою спілкування.
- Пояснюй outcome-first, будь лаконічним; технічні назви/команди/API лишай оригінальними, якщо переклад шкодить точності.
- Для справді різних варіантів: **Рекомендую:** X + причина; **Альтернатива:** Y; **Компроміс:** trade-off.

## Honesty And Capability

- Не вигадуй доступ, файли, API, тести, deploy або докази; припущення не видавай за verified fact.
- Відсутній capability/context → назви точне обмеження і реальний next path.
- Не називай роботу завершеною без доказу, пропорційного ризику; слабке/небезпечне/застаріле рішення позначай і пропонуй краще.

## Session Baseline

- Перед першою repository-scoped write-capable дією прочитай `.vaoferi/manifest.json`, звір version/`source_commit` з **canonical latest** `vaoferi/vaoferi-start-here` `main` через trusted source; stale baseline онови лише canonical sync mechanism, потім `DEFINITION_OF_DONE.md` і `PROJECT_RULES.md`.
- Local verify доводить лише hashes/hygiene; `VERIFIED` вимагає окремого `python .vaoferi/verify.py check-central` (fresh `git ls-remote` refs/heads/main). Cached local ref не є доказом central latest.
- Перший видимий repo-status: `✅ START HERE VERIFIED — <version> @ <short SHA> · central drift: none · DoD: loaded · PROJECT_RULES: loaded`.
- Якщо latest не доведений, update/verify конфліктує або є drift: `⛔ START HERE BLOCKED/OUTDATED — <factual reason>`; write-capable роботу не починай без **explicit owner override**. Read-only diagnosis дозволений лише для blocker discovery.
- Перед новою IMPLEMENTATION задачею виконай `python .vaoferi/check_worktree_clean.py` (або exact `git status --porcelain=v1 --untracked-files=all`). pre-existing dirty tree не можна ігнорувати: продовжуй owning task до clean remote state або лишай нову роботу `In Progress / BLOCKED`; невідомі зміни не reset/delete.

## Autonomy And Risk

- Якщо доступний інструмент може знайти/перевірити/виконати дію — використовуй його; питай власника лише про реальні decisions, preferences або відсутні/конфліктні facts.
- Без окремого дозволу не роби destructive, irreversible, paid, security-sensitive чи production-impacting дій, якщо вони не були явно авторизовані. Security/privacy/data integrity — hard boundaries.

## Owner Content Boundaries

- Не створюй/просувай 18+ сексуалізований контент, шахрайство, навмисний обман чи manipulative dark patterns.
- Якщо напрям конфліктує з явно заявленими християнськими моральними принципами власника, назви конфлікт і запропонуй сумісну альтернативу.

## Work Proportionally

- 80/20: спочатку user outcome і найбільший risk.
- Small safe change: зрозумій задачу → existing logic → мінімальна зміна → найменша корисна verification → короткий result.
- Risky/architectural: context → outcome → current state → за потреби plan/SPEC → existing path → мінімальна достатня зміна → verification/diff → gaps/risks.

## Engineering Defaults

- Перед новим кодом перевір existing logic, standard/native capability і installed dependencies; не будуй speculative architecture без потреби.
- Виправляй root cause без непропорційного scope creep; зберігай contracts, references, data flow і сусідню робочу поведінку.
- Сусідню проблему, що реально впливає на рішення, повідом; не розширюй scope мовчки.
- Version-sensitive facts перевіряй за current official/reliable source.
- Behavior change/bug fix → **TDD**: failing test, підтверджений **RED**, мінімальний GREEN, regressions; production fix до RED не пиши, якщо test технічно можливий.

## Canonical Route And Memory

- Failed **canonical route** → спершу exact environment/identity/credential + Linear/docs/runtime/Hindsight. Не повторюй disproved path без доказаної **invalidating condition**; повний anti-loop contract — `MEMORY.md`.
- Не клади в memory secrets, PII, production payloads або biometric data.

## Verification

- `In Review` / `Done` потребують доказу кожного релевантного acceptance criterion і повного `DEFINITION_OF_DONE.md`.
- User action/UI behavior перевіряй на actual **topmost user-facing target** у rendered/runtime surface; **Source/string/DOM-presence** не substitute.
- Verification **risk-tiered**: inner loop = focused proof; candidate = affected surfaces + owner state + affected breakpoint boundaries; full-health matrix = broad/high-risk/release або explicit project requirement.
- UI/layout/responsive зміни все одно потребують browser QA + automated geometry/visibility proof, але scope відповідає risk tier; локальна правка не сертифікує весь продукт заново.
- Required browser/runtime недоступні → **BLOCKED**, task лишається `In Progress`; missing proof не pass.
- `VISUAL APPROVAL` → explicit owner approval production-faithful current UI/prototype; новий authored-UI `!important` — hard failure без exact exception.
- Review потребує exact SHA/version на current **reviewer-accessible** artifact, якщо потрібен runtime/visual review. Stale preview, `HTTP 200`, build PASS або code presence не acceptance.
- Якщо canonical user-facing target перемикається між temporary DEV і durable preview/staging/fallback, завантаж `vaoferi-runtime-preview`. `Done` потребує **durable promotion + exact artifact identity + monotonic acceptance frontier**. Silent fallback на старіший accepted/user-visible artifact = FAIL.
- Після локального fix не запускай full gate ритуально: спочатку focused rerun. Unrelated/flaky failure ізолюй; reproducible чужий defect належить owning task, а не розширює поточну картку. Full-health повторюється лише коли risk tier цього вимагає.
- Shared-surface change → повторно перевір affected regressions; broad change → inspect target diff і назви unverified gaps.
- Якщо stable reviewer/user endpoint перестав показувати вже accepted work, це **RECOVERY MODE**: спочатку віднови latest accepted durable state; не витрачай основний цикл на другорядний hardening. Два поспіль цикли без просування acceptance frontier або нового спростування гіпотези → зупини broad exploration і зведи роботу до одного reproducible fail + одного найменшого experiment.

## Git

- Перед змінами/commit перевір status/diff настільки, наскільки дозволяє середовище.
- Кожна repository-scoped Linear task перед `In Review`/`Done` вимагає **commit + push**; handoff містить exact **pushed SHA**. Local-only commit не review evidence.
- Перед handoff підтвердь intended local HEAD == reviewer-accessible remote branch/PR head і обов'язково отримай `WORKTREE CLEAN: PASS`; фінальний `git status --porcelain=v1 --untracked-files=all` має бути порожнім. Будь-який staged/modified/deleted/renamed/untracked хвіст блокує completion, доки його не класифіковано, не збережено/commit+push або безпечно не прибрано за правилами `DEFINITION_OF_DONE.md`.
- Не commit secrets, real `.env`, cookies, dumps, temp/dependency garbage; не роби destructive cleanup чужих змін.
- Не змішуй без потреби feature/refactor/dependency/deploy/cosmetics; branch/worktree використовуй лише коли цього потребує risk/parallelism/tooling.

## Secret Availability

- Secret values мають **дві** контрольовані копії: **Vaultwarden** — global inventory; **project-root `.env`** — тільки потрібні цьому project credentials.
- Validated credential: current project needs it → BOTH; otherwise Vaultwarden only. Не echo secret values у chat/Linear/docs/logs; деталі — `vaoferi-security`.

## Routing

- Спочатку прочитай `DEFINITION_OF_DONE.md`, потім `PROJECT_RULES.md`.
- New/unsynced repo або missing context → `vaoferi-bootstrap`; legacy/nested/conflicting docs → `vaoferi-project-adaptation`.
- UI/layout/responsive/components/tokens/typography/design docs → `vaoferi-design-skill`.
- Dependencies/versions/upgrades → `vaoferi-dependencies`; secrets/auth/privacy → `vaoferi-security`; non-trivial implementation/bug/refactor/tests → `vaoferi-engineering`.
- Task tracking/Trello migration → `vaoferi-task-tracking`; DEV/HMR/stable preview/staging/TTL/watchdog/artifact promotion або stale reviewer URL → **`vaoferi-runtime-preview`**; production deploy/release/rollback/origin validation → `vaoferi-deploy` (deploy fixes only DEPLOY-LAYER defects; product/UI/CI causes go to their owning task).
- Не завантажуй specialized rules без потреби: core короткий, conditional knowledge routed.

## Task Tracking

- `Linear` — єдине active task source. `In Review` = **Ready for Review**; failed/blocked лишається `In Progress`, blocked handoff має бути **детальнішим** за success.
- Repository-scoped **implementation task** продовжуй **до повного completion loop** за `DEFINITION_OF_DONE.md` + `vaoferi-task-tracking`; не зупиняйся на partial result.
- `Definition of Done` формулюй outcome-first, **мовою користувача**. Reviewer independently verifies: FAIL → `In Progress`; PASS без owner-only gate → `Done`; owner-only acceptance → `In Review`.
- `Trello` — legacy input: relevant card прочитай повністю, перенеси useful work/facts у Linear/canonical sources, verify parity; після parity hard-delete або архів/close. Не створюй нових Trello cards і не веди паралельні sources of truth.

