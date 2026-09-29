# Definition of Done — Vaoferi repositories

Цей документ є обов'язковим completion contract для всіх repository-scoped IMPLEMENTATION задач у підключених Vaoferi проєктах.

## 1. Немає "майже готово"

Задача не може перейти в `In Review` або `Done`, якщо після агента лишився будь-який погоджений хвіст: код, тест, lint/typecheck, build, browser/runtime QA, commit, push, remote sync, evidence або acceptance criterion.

Якщо виконання фізично заблоковане зовнішнім фактором, задача лишається `In Progress / BLOCKED` з детальним blocker handoff. Заборонено маскувати незавершену роботу під review-ready.

## 2. Git completion і чистий worktree є обов'язковими

### Preflight: чужі або старі зміни не можна ігнорувати

Перед початком **нової** repository-scoped IMPLEMENTATION задачі агент запускає:

`git status --porcelain=v1 --untracked-files=all`

або canonical helper:

`python .vaoferi/check_worktree_clean.py`

Якщо worktree вже dirty, агент **не має права** просто почати нову задачу поверх нього.

- Кожен pre-existing staged/modified/deleted/renamed/untracked файл треба інвентаризувати й прив'язати до конкретної задачі або джерела.
- Якщо зміни належать незавершеній активній задачі, агент продовжує **саме її** до commit + push + clean worktree, а не відкриває поверх неї інший implementation slice.
- Якщо зміни належать іншій відомій задачі, її треба явно link-нути/відновити й довести до безпечного remote state окремим commit/push перед новим review-ready handoff.
- Якщо ownership неможливо довести без ризику втрати даних, поточна робота лишається `In Progress / BLOCKED`; невідомі зміни не видаляються, не reset-яться і не маскуються.
- Generated/temp garbage, створене поточним агентом і доведено disposable, прибирається до handoff. Чужі або невідомі файли не знищуються заради зеленого status.

### Completion: нуль незакомічених файлів

Перед `In Review` / `Done` для кожної repository-scoped IMPLEMENTATION задачі агент зобов'язаний:

1. перевірити цільовий diff та `git status --porcelain=v1 --untracked-files=all`;
2. commit-нути **всі** безпечно класифіковані project-owned зміни, які мають зберігатися, з коректною issue traceability;
3. push-нути кожен intended commit у reviewer-accessible remote branch/PR;
4. підтвердити, що intended local HEAD == remote branch/PR head;
5. повторно запустити `python .vaoferi/check_worktree_clean.py`;
6. отримати **порожній Git status** і `WORKTREE CLEAN: PASS`;
7. записати exact pushed SHA/PR та clean-worktree evidence у Linear handoff.

У кінці задачі має залишатися **нуль незакомічених tracked/staged/untracked файлів**. Gitignored private/runtime файли не є Git-worktree змінами, але tracked secrets або випадково unignored приватні файли — окрема security failure, не привід їх commit-ити.

Local-only commit не є завершенням. Непушений commit, dirty worktree або невідомий mixed diff блокують `In Review` / `Done`.

## 3. Risk-tiered manual browser QA

Кожна user-visible зміна все ще потребує **реальної browser-перевірки**, але обсяг перевірки має відповідати blast radius, а не автоматично дорівнювати максимальній release-матриці.

Перед verification acceptance ledger фіксує affected surfaces, relevant behavior/states/themes/orientations, owner-reproduced viewport/state, affected responsive breakpoints і risk tier.

### Candidate UI gate — default для локальної UI-задачі

Для звичайної локальної зміни перевір:
- кожну affected user-facing surface;
- owner-reproduced viewport/state;
- для кожного **зачепленого breakpoint** — `n-1 / n / n+1`;
- representative narrow і desktop state, якщо зміна може впливати на обидва класи;
- тільки релевантні theme/orientation/interaction states.

Не треба вручну проганяти весь сайт і всі browser flows після зміни одного кольору, локального spacing або одного Hero gradient, якщо diff/contract не мають broader impact.

### Full Health canonical matrix

Повна матриця нижче є mandatory для broad/high-risk UI, release/production checkpoint, CI/nightly health, shared/global layout/tokens/app-shell змін або коли focused evidence показує ширший blast radius.

| Клас | Portrait | Landscape |
|---|---:|---:|
| extra-small / below-common phone | 280×480 | 480×280 |
| normal phone | 390×844 | 844×390 |
| tablet | 768×1024 | 1024×768 |
| desktop | 1440×900 | 900×1440 |
| ultra-wide / extreme large | 2560×1080 | 1080×2560 |

Project-specific viewport-и можуть посилювати відповідний risk tier. Якщо blast radius невідомий — verification розширюється, а не мовчки звужується.

У кожному перевіреному state перевіряються required content/visibility, clipping/overlap, horizontal overflow, reachable controls, responsive reflow, relevant theme/state behavior і Console/Network там, де це релевантно acceptance.

## 4. Stable user-facing target після teardown / fallback

Якщо project workflow має тимчасовий DEV/HMR runtime, preview/staging mode, TTL/watchdog, route switching або інший fallback на durable user-facing artifact, browser QA на активному DEV **не є достатнім доказом Done**.

Перед `In Review` / `Done` user-visible зміна має довести весь lifecycle:

1. exact pushed/accepted SHA відомий;
2. canonical reviewer-accessible target під час DEV/temporary runtime показує саме цей SHA/version;
3. required browser/runtime QA на цьому target PASS;
4. accepted candidate built/verified і promoted у durable stable preview/staging artifact;
5. temporary DEV/runtime нормально зупинено через project-standard teardown path; **manual forced TTL/watchdog expiry** обов'язковий, якщо задача змінює runtime/publisher/routing/promotion/lease/watchdog mechanics або project contract прямо цього вимагає;
6. **той самий canonical stable endpoint** після normal teardown/fallback все ще показує accepted SHA/version;
7. ключові user-visible acceptance points повторно перевірені після fallback.

Для звичайної product/UI зміни, яка не торкається runtime lifecycle, exact-SHA durable promotion + normal stop parity є достатнім per-task lifecycle proof, якщо automated project regression уже захищає TTL/watchdog. Не симулюй TTL expiry після кожної CSS/text правки.

Нормальний teardown/TTL/watchdog **не має права мовчки зробити видимим старіший user-facing artifact**. Latest accepted user-visible state є durable baseline до наступного explicit accepted promotion.

Якщо stable artifact старіший за accepted candidate, task лишається `In Progress`: спочатку треба виконати project-owned build/verify/promotion path або fail closed. `HTTP 200`, healthy container чи доступний fallback без exact candidate identity не є PASS.

Project docs визначають конкретний endpoint, identity mechanism, promotion command і teardown lifecycle. Якщо project взагалі не має temporary→stable/fallback topology, цей gate документується як `N/A` з короткою причиною.

### 4.1 Acceptance frontier, durable evidence and recovery

For temporary→durable runtimes, completion follows this monotonic frontier:

`SOURCE → CANDIDATE → TEMP TARGET → USER ACCEPTANCE → DURABLE PROMOTION → TEARDOWN → STABLE PARITY → DURABLE EVIDENCE`.

Hard rules:

- permanent/stable preview means the **latest accepted durable user-visible state**, not merely any healthy fallback;
- exact artifact identity must survive the temporary DEV process; SPA HTML from an identity route is a FAIL;
- accepted runtime/promotion fixes may not remain only on a stale/diverged task branch while dependent work continues on the authoritative branch;
- if accepted work disappears from the canonical stable endpoint, enter **RECOVERY MODE** and restore the latest accepted durable state before secondary hardening;
- evidence must include the exact control-plane implementation that actually executed build/promotion/teardown;
- two consecutive iterations with no frontier advance and no newly falsified hypothesis require scope collapse to one reproducible failure and one smallest next experiment.

Detailed procedure: `.agents/skills/vaoferi-runtime-preview/SKILL.md`.

## 5. Automated responsive/geometry verification

Manual browser QA не замінює automated browser geometry/visibility regression для layout/responsive роботи.

### Candidate scope

За замовчуванням machine gate перевіряє **affected surface/range**: owner-reproduced edge case, affected breakpoint boundaries `n-1 / n / n+1`, relevant min/max heights або aspect states, і representative intermediate state там, де між boundaries може виникнути інша geometry.

### Full-health scope

Exhaustive integer CSS-pixel sweep по bounded range або широка browser/state matrix потрібні, коли змінюється shared/global layout/token/breakpoint system; ризик є саме “дірка між sampled widths”; owner defect відтворюється у bounded interval; є broad redesign/refactor; або CI/release/nightly/full-health contract цього вимагає.

Не роби повний Cartesian sweep ритуалом для кожної локальної visual правки.

Machine gate має fail-ити на relevant scope, якщо expected element зник, rect виходить за approved container/viewport, siblings overlap, required inset колапсує, з'явився unexpected horizontal overflow або content стає clipped/hidden.

Pixel-diff може доповнювати geometry assertions, але не замінює semantic/DOM geometry proof там, де потрібні видимість, кількість або взаємне розташування.

## 6. Verification ladder — focused by default, full when risk requires

### V1 — Inner loop
Після кожної маленької зміни: focused RED → GREEN regression, найменший релевантний lint/type/static check і exact browser interaction, якщо behavior browser-dependent. **Не запускай full project/browser gate після кожної CSS/helper/timing правки.**

### V2 — Candidate gate
Коли implementation slice готовий: build якщо applicable, focused regression suites, candidate browser/geometry gate з секцій 3/5 і relevant security/static checks.

### V3 — Stable acceptance
Для reviewer-visible change: commit + push exact candidate SHA; canonical reviewer target показує саме цей SHA/version; key affected acceptance повторно перевірена; temporary→durable topology виконує секцію 4.

### V4 — Full health
Повний project gate / broad browser-engine matrix / full responsive matrix обов'язковий для high-risk або broad change: auth/roles/permissions/passwords; API/persistence/schema/data model; security/privacy; media pipeline/shared loading-cache behavior; runtime/publisher/deploy/projectctl/promotion; dependency/build tooling; shared/global CSS/design tokens/router/app shell; broad multi-surface redesign/refactor; production/release checkpoint; broader blast radius із focused evidence; або explicit project/owner requirement.

Для ordinary локальної задачі — **не більше двох full-health runs за замовчуванням**: final candidate і один repeat після focused fix реального failure. Третій full-health run потребує короткого письмового пояснення: який **новий ризик** він доводить і чому focused rerun недостатній.

### Failure ownership
1. Affected/current-card failure блокує task і виправляється тут.
2. Unrelated failure → isolate smallest owning test + bounded repeat (зазвичай 2–3 рази).
3. Reproducible unrelated defect → owning task/follow-up; поточна картка не ремонтує чужий subsystem.
4. Timing/flaky assertion без user-visible repro → test-hardening; production behavior не змінюється лише заради зеленого flaky assertion.
5. Після focused fix повтори candidate gate; новий full-health run лише коли risk tier цього вимагає.

Known failure не можна назвати PASS. PRE-EXISTING/UNRELATED, CI/ENVIRONMENT і EXTERNAL failures фіксуються чесно та не маскуються product-fix-ом.

## 7. Evidence handoff у Linear

Repository-scoped IMPLEMENTATION задача не готова до review без короткого evidence ledger:

- `MODE: IMPLEMENTATION`
- `SHA/PR: <exact pushed SHA / PR>`
- `FOCUSED TESTS: PASS`
- `PROJECT GATES: PASS` або `N/A + exact reason`
- `BUILD: PASS` або `N/A + reason`
- `BROWSER/RUNTIME: PASS — <affected surfaces> × <manual states count>`
- `AUTOMATED RESPONSIVE/GEOMETRY: PASS — <command/test>` або `N/A + documented non-UI reason`
- `REMOTE SYNC: PASS`
- `WORKTREE CLEAN: PASS — python .vaoferi/check_worktree_clean.py`
- `KNOWN EXCEPTIONS: none` або explicit accepted exception

Reviewer перевіряє докази незалежно. Missing evidence = FAIL → `In Progress`.

## 8. Project rules можуть тільки посилювати

`PROJECT_RULES.md`, `DESIGN_CONTRACT.md`, `TESTING.md`, SPEC та інші project-owned docs можуть додавати viewport-и, acceptance criteria, security gates, browser engines, ролі, теми, локалізації та production checks.

Вони не можуть послабити цей Definition of Done без explicit owner decision, зафіксованого в canonical docs.

## 9. Принцип

**Зробив задачу — довів її до віддаленої, перевіреної, відтворюваної й незалежно перевіряємої готовності.**

Код без push, UI без browser QA, browser QA без affected-surface matrix, layout без automated responsive geometry regression або task без evidence — це не Done.