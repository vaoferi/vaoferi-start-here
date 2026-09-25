# Codex Global Critical Guardrails

This is the intentionally small global Codex mirror for the owner's highest-risk working rules.

Install/reconcile it as `$CODEX_HOME/AGENTS.md`; default: `~/.codex/AGENTS.md`. It does not replace repository `AGENTS.md` or `PROJECT_RULES.md`; project/directory instructions remain authoritative for project facts.

## Critical working rules

- **Session baseline first.** Before the first write-capable repository action, inspect `.vaoferi/manifest.json`, compare installed Start Here version/source commit with canonical latest Vaoferi Start Here `main`, update through the canonical sync path if stale, verify central drift, then read repository `AGENTS.md`, `PROJECT_RULES.md`, and routed project docs. The first visible repo-status must be `✅ START HERE VERIFIED — <version> @ <short SHA> · central drift: none · PROJECT_RULES: loaded` only after factual latest comparison + local verify. Otherwise emit `⛔ START HERE BLOCKED/OUTDATED — <reason>` and **do not begin write-capable repository work** without explicit owner override; read-only diagnosis is allowed.
- Explain/verify **outcome-first**. For behavior changes and bug fixes use **TDD**: prove RED, implement minimum GREEN, then regressions.
- Every relevant **acceptance criterion** needs proof before `In Review`/`Done`. User actions/UI behavior must be exercised on the real **topmost user-facing target**; source/string/DOM presence is not a substitute.
- Missing required browser/runtime proof = **BLOCKED**. Never call missing evidence a pass.
- `In Review` means **Ready for Review**. **Blocked**/failed work stays `In Progress`; the executor preserves evidence and the reviewer verifies independently.
- Every repository-scoped task requires **commit + push** before review/Done; record exact **pushed SHA**. Local-only commits are not review evidence.
- **WORKTREE CLEAN is mandatory.** Before a new implementation task, classify any pre-existing `git status --porcelain=v1 --untracked-files=all` output instead of ignoring it. Before `In Review`/`Done`, `python .vaoferi/check_worktree_clean.py` must report `WORKTREE CLEAN: PASS`; unknown dirty state stays `In Progress / BLOCKED`, never reset/delete it just to get green.
- Secrets: **Vaultwarden** stores validated credentials globally; project-root `.env` stores only credentials needed by that project. Never echo secret values.
- `VISUAL APPROVAL` requires explicit owner approval on a production-faithful current UI before visible implementation. New authored-UI `!important` is a hard failure without an exact accepted exception.
- Equal visible peer groups must not create accidental orphan layouts such as `2+1`, `3+1`, `2+2+1` without a documented semantic/compositional/accessibility reason.
- Run project-required lint/build/tests and required browser/responsive/device gates; inspect Console/Network when relevant.
- Runtime/visual review must point to an exact SHA/version on a current **reviewer-accessible** artifact/preview.
- Production deploy is not complete on upload/read-back or `HTTP 200`: verify the exact reviewed candidate on effective origin and required browser/runtime surface; do not repeat write-capable deploy attempts without changed evidence/preconditions.
- Never weaken/delete tests just to get green. Never claim verified behavior, deployment, access, latest baseline, or test results that did not actually run.

Canonical detailed doctrine remains in Vaoferi Start Here and conditional skills. This global layer intentionally duplicates only critical guardrails so they remain present even when a repository copy is stale.
