---
name: vaoferi-observability
description: Default website instrumentation, consent-safe telemetry, error capture, free-tier quota strategy, provider dashboard binding, and real ingestion verification for static/SPA/CMS/server-rendered websites.
---

# Vaoferi Observability — Start Here 4.0.0

## Trigger and outcome

Load for every new/updated web product: static HTML, WordPress/CMS, SPA, Yii2/PHP, SSR, landing page and authenticated admin/cabinet. At onboarding, audit existing instrumentation and make it operational where appropriate. Revisit when a user-facing flow, URL/host, deployment, forms, login or tracking policy changes.

Goal: after a bug, answer `page → safe action/event → client error or network response → request/correlation ID → backend result → support report`. This is not permission to collect every typed character or every private screen. **Privacy/data minimization is a hard requirement; recording quantity is not a success metric.**

Keep website-specific account IDs, domain binding, owner consent and evidence in **project-owned** `docs/observability/STATUS.md` (or existing equivalent). The centrally synced skill must not contain customer/project URLs, IDs, secrets or private content.

## Provider roster — free first

| Provider | Primary job | Official setup/dashboard | Free strategy |
| --- | --- | --- | --- |
| Microsoft Clarity | Public UX: heatmaps, rage/dead clicks, sampled/allowed replays | https://clarity.microsoft.com/ and https://clarity.microsoft.com/pricing | Vendor advertises free; verify current terms and privacy/consent at integration time |
| PostHog | Named business events, funnels and sampled replay | https://app.posthog.com/ and https://posthog.com/pricing | Current published free allowance: 1M analytics events and 5K web replays/month; establish hard cost controls |
| Sentry | JS/app/server errors, stack traces, grouping, release impact; low-volume error replay | https://sentry.io/organizations/ and https://sentry.io/pricing/ | Free Developer replay starts at 50 sessions at time of this policy; prioritize errors and disable paid overage |

Official documentation: https://clarity.microsoft.com/ ; https://posthog.com/docs/ ; https://docs.sentry.io/ . Recheck current vendor quotas, included features, recording semantics, retention and billing in each account; never treat these numbers as permanent.

**Default:** assess all three in every website, not automatically enable all three recordings. Clarity for eligible public behavior, PostHog for meaningful product events, Sentry for errors. Choose at most ONE replay provider per page/surface by default. Small low-traffic projects may use only Sentry error-triggered replay; on public sites with frequent UX problems prefer Clarity; when funnel/replay correlation is key use PostHog. A provider may be NOT_APPLICABLE with a documented reason, never just omitted silently. Zero-paid is mandatory: no paid feature, no surprise card/overage, disable or throttle at quota exhaustion.

Provider availability does not imply project access. Verify the **right organization, project ID, hostname/route and environment** before using a dashboard. The developer may be logged into the wrong provider account. Never use a credential or project ID from another client's website.

## Static hosting and server-rendered apps

The **browser SDK** of each provider can be embedded in static HTML, CMS, SPA or Yii2 templates, subject to CSP, consent and deployment approval. A static site needs no PHP server for browser event capture; it does need a separate allowed backend/service for first-party support-report submission and email notifications. Do not claim a static host can receive/store reports solely with HTML.

Add scripts once at the current approved asset/build/theme entry point, not in every template or page. Use vendor's documented snippet and project-scoped public identifier; never commit private keys/DSNs. For authenticated apps, instrument **only allowlisted safe routes/events**; login, personal documents, medical/biometric content, personal messages and private profiles are replay-disabled unless specifically designed, masked and approved.

## Capture policy and consent

1. Before instrumenting: classify pages as PUBLIC / AUTHENTICATED / SENSITIVE. Identify controller/route, form fields, screenshots, media, network bodies and jurisdiction-specific notice/consent requirements. Use current privacy/legal guidance; never presume a vendor's “GDPR-ready” banner constitutes the site's legal basis.
2. Default event schema: `site_id, environment, release_sha, route_template, timestamp, event_name, safe_element_id, outcome, elapsed_ms, http_status, error_code, correlation_id`. No full query string, URL token, raw clicked text, input value, DOM contents, IP/user agent dump, cookie or authorization header.
3. Memory-only bounded ring buffer of recent safe events (e.g. last 5 minutes) can be included in a bug report after explicit submission. Do not persist raw session history indefinitely.
4. Where consent is required, no analytics/replay transmission until valid affirmative choice; honor denial, revocation and consent changes. Error reporting may have a different applicable basis but still requires an explicit site policy. Avoid pre-consent replay backfilling.
5. Sensitive pages: replay **OFF** unless dedicated permission + proven masking. Mask/redact text, images, inputs, error strings, navigation metadata and network data. Never record credentials, passport/ID scans, face imagery, financial/health information or private messages.
6. Report detail/replay visible only to authorized staff; keep access audit, retention/deletion and data-subject rights workflow. Do not expose a privileged replay link in ordinary email.
7. Test with canary PII strings in disposable test pages to prove they never reach events/replay. Client redaction is insufficient as sole enforcement for first-party bug report storage: server must allowlist/redact too.

## Workflow at every eligible project

**A. Discover, no changes yet.** Locate root, framework and actual production sites/subdomains; read project rules and test/deploy entry points. Inventory existing Clarity/PostHog/Sentry (and alternatives like Matomo), duplicates, site account mapping, privacy notice, consent manager and JS bundle/CSP. Do not install a second overlapping tracker while one is already present. Respect project-owned exceptions.

**B. Choose a free plan per site.** Mark each provider `ENABLED / NOT_CONFIGURED / BLOCKED / NOT_APPLICABLE`, plus mode `events / errors / replay`, expected volume, quota cap, account/project verification, allowed routes and replay sampling. One replay provider per surface unless owner approved an exception. Missing account/consent = BLOCKED; no “PASS” from source inspection.

**C. Implement narrowly.** Prefer native SDK documented current integration at existing asset entry point. Configure release/environment tags; stable request ID and error association when a backend exists. Protect against double initialization, ad blockers, offline and script failure; analytics outage must never break business flow. Never auto deploy to production.

**D. Verify where lawful.** In browser test a disposable/synthetic safe page: expected network request **after** consent where needed; expected event in the exact account/project dashboard; one synthetic JS error grouped in Sentry; PostHog funnel event visible; Clarity page/session only on allowed public test path; no duplicate events or unexpected provider traffic. Confirm on both desktop and mobile if relevant; check blocked scripts degrade gracefully. Verify masked canary strings are absent on provider payloads/replay, no sensitive route recording. A console log, snippet match, GET 200 or screenshot alone does NOT prove ingestion.

**E. Record evidence and maintain.** Save project-owned site status: full monitored host and route class, provider/account/project identity (non-secret), dashboard link, mode, quota/cap/sampling, region/consent rule, exclusions, tested URL, tested UTC time, exact release SHA, evidence of dashboard ingestion, result and owner next action. Review on initial release, domain migration, auth/privacy change and after major user-facing release. If a provider is blocked, name the exact missing authorization/project ID and continue safe existing user-facing bugfix work.

## Minimal project-owned status record

Create or extend `docs/observability/STATUS.md` (do **not** copy this file as a centrally owned sync artifact):

- Site/host(s), stack, production versus preview domain and source SHA.
- Provider table: `provider | verified organization/project | dashboard URL | status | mode | consent gate | quota/cap | replay route exclusions | last ingest proof`.
- Alerting: owner notification route and sample report link/ID; do not disclose private payload in email.
- Known privacy/consent exceptions and retention/deletion location.
- Latest evidence: `provider → real test event ID and UTC time → correct domain/account → browser/network + dashboard result → PASS/FAIL/BLOCKED`.
- Outstanding decisions: account/consent/paid-feature/hosting capability. No secrets.

## Subagents and cost-aware delegation (when actually available)

- `openrouter/baidu-ernie-5.5-flash-preview:free` — implementation and SDK wiring.
- `nous/qwen-qwen4-max:free` — RED→GREEN contract / browser test cases.
- `nous/tencent-hy4-flash:free` — narrow triage and vendor docs.
- `gpt-6-luna` — UX placement, privacy notice and responsive QA.
- `gpt-6.1-terra` — independent review of privacy, auth, network data and application stability.

Use only 2–3 relevant subagents per issue; check model capabilities and real tests. Review must be independent from implementation. One issue/PR at a time, with exact evidence and no broad rewrites.

## Definition of Done and pitfalls

PASS only if the correct site's provider identity and event/replay/error ingestion are independently confirmed, no PII leakage or unauthorized pre-consent traffic occurred, free quota cap is enforced, and the site still works with tracking blocked. A provider legitimately out of scope is `NOT_APPLICABLE` with a reason, not an imaginary PASS. Production deployment needs separate owner authorization and a verified receipt; local preview integration is not production.

Pitfalls: three overlapping replay SDKs exhaust free quotas; testing the wrong PostHog/Sentry/Clarity account yields false confidence; arbitrary URL query/text/JS error capture can leak PII; consent banners are not equivalent to enforcement; static HTML cannot process an email/bug report without a backend; missing external project IDs cannot be generated by an agent; observability setup must not postpone an urgent existing production UX bug.
