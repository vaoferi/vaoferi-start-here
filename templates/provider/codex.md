# Codex Global Critical Guardrails

Compact mirror of Vaoferi's highest-risk rules for `$CODEX_HOME/AGENTS.md` (default `~/.codex/AGENTS.md`). It supplements, never replaces, repository `AGENTS.md` / `PROJECT_RULES.md`.

## Critical working rules

- **Session baseline first.** Before write-capable repo work, compare local `.vaoferi/manifest.json` with canonical latest Start Here `main`; if stale, update through canonical sync, verify drift, then read `DEFINITION_OF_DONE.md` and `PROJECT_RULES.md`. Only then emit `✅ START HERE VERIFIED — <version> @ <short SHA> · central drift: none · PROJECT_RULES: loaded`. Otherwise emit `⛔ START HERE BLOCKED/OUTDATED — <reason>` and **do not begin write-capable repository work** without explicit owner override.
- Explain outcome-first. Behavior change/bug fix → TDD RED → minimal GREEN → regressions.
- Every relevant acceptance criterion needs proof before `In Review`/`Done`. User actions/UI behavior must be exercised on the real topmost user-facing target; source/string/DOM presence is supplementary only.
- Missing required browser/runtime proof = **BLOCKED**. Never call missing evidence a pass.
- `In Review` = Ready for Review. Blocked/failed work stays `In Progress`; executor evidence is independently checked by the reviewer.
- Every repository task requires **commit + push + exact pushed SHA** before review/Done.
- **WORKTREE CLEAN is mandatory.** Classify pre-existing dirty state before new implementation work; before handoff, `python .vaoferi/check_worktree_clean.py` must report `WORKTREE CLEAN: PASS`. Never reset/delete unknown work just to get green.
- Secrets: Vaultwarden is the global inventory; project-root `.env` holds only project-needed credentials. Never echo secret values.
- `VISUAL APPROVAL` requires explicit owner approval on a production-faithful current UI. New authored-UI `!important` is a hard failure without an accepted exception.
- Equal visible peer groups must not create accidental orphan layouts (`2+1`, `3+1`, `2+2+1`) without a documented reason.
- Verification is **risk-tiered**: focused RED→GREEN in the inner loop; affected-surface/breakpoint candidate gate before review; full project/browser matrix only for broad/high-risk/release or explicit project requirements. Isolate unrelated/flaky failures instead of expanding the current task.
- Runtime/visual review must point to an exact SHA/version on a current reviewer-accessible artifact.
- Temporary DEV → durable preview/staging/fallback requires **durable promotion + exact artifact identity + post-teardown verification**. Latest accepted visible state must survive DEV death; healthy-but-stale fallback = FAIL.
- If an accepted stable endpoint becomes stale/broken, enter **RECOVERY MODE**: restore the latest accepted durable state before secondary hardening. Two consecutive loops with no frontier movement/new falsification → one reproducible fail + one smallest experiment.
- Runtime evidence must identify the exact control-plane implementation that ran; stale installed tooling cannot prove a newer checkout's contract.
- Production deploy is not done on upload/read-back or `HTTP 200`; verify the exact reviewed candidate on effective origin and required browser/runtime surface.
- Never weaken/delete tests just to get green. Never claim verification that did not actually run.

Canonical details remain in Vaoferi Start Here and conditional skills.
