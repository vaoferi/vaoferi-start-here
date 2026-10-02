# Memory and Recovery Contract — Vaoferi repositories

This file is centrally owned by **Vaoferi Start Here** and is synced into every participating repository. It defines how long-term agent memory reduces repeated dead ends without becoming a parallel source of truth.

## 1. Authority: memory is a guardrail, not a source of truth

Hindsight is **not a source of truth**. It is an experience layer for prior decisions, failed approaches, corrections and useful project context.

When sources disagree, use this order:

1. current Start Here + current project `PROJECT_RULES.md` / current ADR or runbook for intended workflow;
2. current code/config/tests and verified runtime for what the system actually does;
3. active Linear owner decisions and task state;
4. Hindsight memory, Git history and historical notes as evidence/context.

Current runtime/code can prove that documentation is stale. That does **not** make silent drift acceptable: update or flag the canonical documentation in the same workstream.

Never let a recalled memory override a newer verified fact merely because it sounds familiar.

## 2. Canonical-route stop

If a current high-authority document says to use a canonical route and that route fails, stop before inventing a second route.

Before bypassing it:

1. reproduce the failure on the exact documented host/path/tool/runtime;
2. verify environment identity, version, current Git SHA/worktree and target identity;
3. verify required credential **names/presence** through approved seams without printing values;
4. search current project docs/ADR/runbooks and active Linear issues for a changed decision;
5. recall/reflect in Hindsight for the same failure signature, disproved approaches and re-entry conditions;
6. state one leading hypothesis and run the **smallest experiment** capable of falsifying it.

A workaround is allowed only after evidence identifies a real blocker. Record why the canonical route could not work, what was tried, and what condition would make the workaround unnecessary. A workaround must not quietly become the new architecture.

Example class: if project rules say Synology-native Linux execution, failure of one SSH/helper route is a reason to diagnose that route — not a reason to move Git/build/tests to a Windows UNC/WebDAV checkout, encode commands through another shell hop, or invoke unrelated Docker paths until something happens to run.

## 3. Anti-loop rule

Before non-trivial diagnosis/implementation, recall or reflect on the current repository/problem when Hindsight is available.

Do not repeat a previously failed/disproved approach unless an explicit **invalidating condition** changed and you can name the evidence. Good invalidators include a different deployed SHA, restored credential, corrected host/path, upgraded dependency, changed topology or a new reproduction that disproves the earlier cause.

Two consecutive cycles with no acceptance-frontier movement, no new falsified hypothesis and no narrower reproducible failure are a process failure. Collapse the work to:

- one current observable failure;
- one leading hypothesis;
- one smallest experiment;
- one next decision based on its result.

## 4. What to retain

Prefer durable, sanitized experience records. A useful trap/correction memory has:

- `project/repo`;
- `problem signature` / observable symptom;
- environment and artifact identity when relevant;
- attempted approach;
- outcome: `failed`, `disproved`, `superseded`, or `verified`;
- evidence pointer: Linear issue/comment, Git SHA/PR, test/runbook path, sanitized log location;
- canonical route;
- `do-not-repeat-until` condition / invalidator;
- verified date/SHA and confidence/scope.

Do **not** retain secret values, cookies/tokens, personal data, document scans, biometric material, raw production payloads or other sensitive data. Hindsight may remember the **name/location/recovery procedure** for a credential, never its value.

Corrections matter more than confident prose. When an earlier conclusion is disproved, retain the correction with evidence so future sessions retrieve the invalidation, not only the original guess.

## 5. Supported Hindsight coding-agent model

Use the upstream `@vectorize-io/hindsight-coding-agents` integration rather than hand-written per-agent bridges.

Machine config lives at `~/.hindsight/coding-agent.json`. Do **not** carry an active Hindsight config in a repository: cloning a repository must not silently enable external memory.

The recommended behavioral core is:

```json
{
  "bankIdTemplate": "coding-agent::{gitProject}",
  "observationScopes": "shared",
  "autoInject": "reflect",
  "retainSessions": false,
  "retainTags": ["project:{gitProject}", "env:work"],
  "retainMetadata": {"repo": "{gitProject}"},
  "toolGuideExtra": "Hindsight is past experience, not current truth. Before bypassing a documented canonical route, verify why it fails against current repo/runtime/Linear evidence. Do not repeat a failed approach unless its invalidating condition changed. Never store or echo secrets, PII or biometric data."
}
```

The default `coding-agent::{gitProject}` is intentionally harness-neutral: Codex, Claude Code and other supported agents working in the same repository share the same repository bank. `observationScopes: "shared"` keeps one belief set per bank instead of splitting beliefs by harness.

`retainSessions: false` is a deliberate Vaoferi privacy default. Owner↔agent sessions may contain credentials, PII or sensitive operational context, and raw automatic transcript write-back would create an uncontrolled third copy. Git ingestion/retrieval and Hindsight tools continue to work; agents explicitly ingest only sanitized durable corrections/decisions. Enabling raw session retention for a scope requires an explicit privacy/retention decision.

After a material correction/dead end, use Hindsight's supported ingest/retain tooling to save the sanitized record from section 4. Do not rely on the raw transcript being retained.

Use `npx @vectorize-io/hindsight-coding-agents install all` on a workstation only after choosing the approved server mode. The installer owns host wiring; do not manually reproduce its hooks/MCP configuration unless upstream explicitly requires recovery.

### Cross-machine persistence

Local daemon mode is machine-local and therefore **does not by itself satisfy** cross-machine continuity. For Windows/macOS/Linux continuity, use one owner-approved shared Hindsight server (self-hosted or Cloud) and point each machine's machine-level config at it.

Do not choose a paid/external memory provider merely for convenience. Server placement, retention/privacy and backup are owner decisions. A shared self-hosted service on approved infrastructure is preferred when it meets operational constraints; deployment belongs to the infrastructure workflow, not an application repository.

Any Hindsight API token/LLM key follows the Start Here secret contract: Vaultwarden is the durable secret inventory; the machine bootstrap injects the credential without writing it into Git/Linear/memory. Global infrastructure credentials do not belong in a random project `.env`.

## 6. Knowledge pages and cross-project memory

Repository banks remain the default because project facts should not bleed between products. Cross-project memory is a **curated second layer**, not a dump of every transcript.

Promote only genuinely reusable experience (for example Synology scheduler quirks, Git-over-network-filesystem hazards, deploy evidence patterns) after it is sanitized and verified. Preserve provenance tags/metadata so a recalled cross-project lesson still says where it came from.

Do not merge NLM product facts, client/site data or credentials into a global bank just because several agents can access it.

## 7. Diagnostics and readiness

Memory failure must degrade to ordinary agent work, not block product work and not trigger a random workaround.

When Hindsight seems empty or stale:

1. use the integration's diagnostic/sync-status tools/logs;
2. confirm the resolved bank is the expected repository bank;
3. confirm the current harness is wired by the supported installer;
4. confirm server reachability/auth without printing tokens;
5. fix memory plumbing separately from the product unless memory itself is the task.

Memory is useful when it shortens archaeology. It is unhealthy when an agent trusts stale recall over current evidence or spends the product task repairing memory infrastructure.
