---
name: vaoferi-runtime-preview
description: Use when a repository has DEV/HMR, preview/staging, a stable reviewer URL, TTL/watchdog, route switching, artifact promotion, or any risk that the user-visible endpoint can serve a different build than the accepted source.
---

# Vaoferi Runtime / Preview Lifecycle

## Core invariant

```text
accepted source → identified candidate → verified stable artifact → normal teardown/fallback → same accepted user-visible state
```

A task is not complete while the accepted result exists only inside a temporary process, lease, branch, worktree, container, cache, or agent session.

## Required project facts

Before runtime/preview work, find the project-owned source for:

- canonical repository/path and authoritative branch;
- canonical reviewer/user-facing stable endpoint;
- DEV/HMR endpoint or internal listener;
- durable artifact location;
- build/promotion command;
- runtime/preview identity mechanism;
- stop/TTL/watchdog lifecycle;
- rollback path;
- control-plane command and its own source/version identity.

Do not invent a parallel runbook when the repository already has one.

## Acceptance frontier

Track progress as a monotonic frontier:

- **F0 SOURCE** — intended source committed, pushed, remote-synced.
- **F1 CANDIDATE** — candidate built from that exact source identity.
- **F2 TEMP TARGET** — canonical stable URL while DEV is active proves that exact identity.
- **F3 USER ACCEPTANCE** — required browser/runtime/visual checks pass.
- **F4 DURABLE PROMOTION** — accepted candidate installed/promoted as durable preview/staging artifact.
- **F5 TEARDOWN** — normal DEV stop/TTL/watchdog completes.
- **F6 STABLE PARITY** — same canonical URL after teardown proves the same accepted identity and key user-visible acceptance.
- **F7 DURABLE EVIDENCE** — source SHA, artifact identity, promotion result and stable endpoint proof are recorded durably.

A later failure returns to the exact failed frontier. Do not restart generic archaeology from F0 after every context switch.

## Durable identity

Runtime/preview evidence must survive the temporary DEV process.

Preferred identity is stored in the artifact itself or returned by an exact non-SPA endpoint/manifest and includes:

- project/release identity;
- exact source SHA/version;
- build/promote timestamp;
- runtime mode when useful;
- no secrets.

`HTTP 200`, container health, file timestamp, source-string presence or a screenshot taken only while DEV was alive do not prove durable acceptance.

If the identity route falls through to SPA HTML, identity proof is FAIL.

## Promotion is a transaction

Normal completion is:

1. build from exact pushed source;
2. verify staged candidate;
3. preserve rollback/preimage;
4. safely promote durable artifact;
5. verify promoted artifact identity and user-visible behavior;
6. only then stop/expire temporary DEV.

The previous artifact is a rollback target for failed promotion/recovery. It is not the normal fallback after successful newer acceptance.

## Single-writer publication invariant

A durable preview/staging target has exactly one declared **canonical publisher** or promotion path.

- Other workflows and scripts may build, test, or retain ephemeral artifacts, but they must not independently mutate the durable target, release pointer, or accepted artifact.
- If CI is allowed to publish, it invokes the same canonical publisher entrypoint; it does not recreate publication with a second `rsync`, `scp`, `sftp`, copy, delete, or remote-shell write path.
- Before **F4 DURABLE PROMOTION**, identify the canonical publisher and inspect repository-owned automation for **competing publishers** that can write the same durable target.
- A **direct write** into the durable target outside the canonical publisher is FAIL and is not promotion evidence, even when the copied files came from the correct source SHA.
- Multiple callers of one canonical publisher must be serialized when concurrent publication could race. Serialization does not make multiple independent publishers valid.
- If accepted stable state later reverts or changes without an accepted promotion, RECOVERY MODE checks competing publishers before broad infrastructure archaeology.

Projects own the concrete protected paths and regression checks. Start Here owns this invariant; do not embed project-specific paths here.

## RECOVERY MODE

If the owner/reviewer reports that the canonical stable endpoint no longer shows already accepted work, immediately enter **RECOVERY MODE**.

Priority:

1. prove current authoritative source identity;
2. prove what the stable endpoint actually serves;
3. restore the latest accepted state through the existing promotion path;
4. verify it with temporary DEV off;
5. only then resume secondary hardening/refactor/tooling work.

While RECOVERY MODE is active:

- do not broaden to unrelated infrastructure;
- do not create a second preview URL or local runtime;
- do not let documentation/secrets/tooling work hide the primary user-visible failure;
- status begins with either:
  - `VISIBLE RECOVERY PASS — <stable endpoint> serves <identity>`
  - `VISIBLE RECOVERY BLOCKED — <one exact failing check/command>`

## Anti-loop rule

Repeating the same blocker is not progress.

Each failed attempt records:

`hypothesis → exact experiment → observed result → what was ruled out → next smallest experiment`.

If **two consecutive iterations** do not advance the acceptance frontier and do not rule out a new hypothesis:

1. stop broad exploration;
2. reduce to one reproducible failing command/interaction;
3. inspect the exact implementation path and control-plane identity;
4. choose one smallest experiment that can falsify the leading hypothesis;
5. do not restate old blockers as a new handoff.

Long-running work optimizes for advancing the user-visible frontier, not accumulating progress comments.

## Control-plane identity

A runtime command counts as evidence only when the executor knows which implementation actually ran.

If an installed CLI/service may be older than the repository checkout:

- compare installed identity/version/hash with canonical source;
- update it through the approved path, or explicitly invoke the current checkout implementation when safe;
- do not let inability to replace a global binary block recovery when a safe current checkout command already performs the needed non-privileged operation;
- record which control-plane identity executed promotion/teardown.

A green result from a stale installed tool does not prove the current runtime contract.

## Branch/worktree integrity

Acceptance-critical runtime fixes cannot live only on a stale/diverged task branch while product work continues on the authoritative branch.

Before dependent user-visible work is Done:

- required runtime/identity/promotion changes are integrated or ported onto the current authoritative baseline;
- do not merge a heavily diverged stale branch wholesale;
- port the smallest still-relevant changes onto current main and rerun verification;
- evidence from an orphaned branch is historical reference, not current acceptance.

## Monotonic accepted baseline

Temporary DEV may be disposable. Accepted state may not be.

Valid progression:

```text
accepted A → permanent A → accepted B → permanent B
```

Forbidden normal lifecycle:

```text
accepted B on DEV → stop/TTL → permanent A
```

## Browser/runtime acceptance

For user-visible changes with temporary→durable topology:
- use the canonical stable endpoint, not localhost/internal port;
- verify exact candidate identity;
- run the **affected** visual/interaction checks required by the task risk tier;
- promote the durable artifact;
- stop DEV through the normal path;
- repeat key checks on the same stable endpoint and prove the same accepted identity.

A **manual forced TTL/watchdog expiry** is required per task when the change touches runtime/publisher/routing/promotion/lease/watchdog mechanics, or when a project-specific high-risk contract explicitly requires it. For an ordinary product/UI change, exact-SHA promotion + normal stop parity is sufficient when project automation already protects TTL/watchdog behavior.

Do not rerun a full product/browser suite inside a runtime finish merely because an unrelated UI test is red. Record the owning surface/task and keep runtime acceptance focused unless the runtime change itself creates broad blast radius.

For media/cache/theme behavior, inspect Network as well as appearance when the requirement concerns repeated requests, caching or progressive loading.

## Project automation

Projects with temporary→durable topology should own regression coverage that fails when:

- stable endpoint serves stale/unknown identity;
- identity endpoint falls through to SPA HTML;
- promotion installs a different source identity;
- stop/TTL exposes an older artifact;
- healthy HTTP/container masks stale content;
- stale control-plane tooling is mistaken for current tooling.

Start Here owns the invariant. Project code owns concrete endpoints, commands and tests.

## Handoff

Record:

- `FRONTIER: F0..F7`
- `SOURCE SHA:`
- `CONTROL-PLANE IDENTITY:`
- `TEMP TARGET IDENTITY:`
- `PROMOTED ARTIFACT IDENTITY:`
- `TEARDOWN PATH:`
- `STABLE TARGET AFTER TEARDOWN:`
- `USER-VISIBLE CHECKS:`
- `RECOVERY MODE: no` or exact blocker

If any applicable identity is unknown, do not use `Done`.
