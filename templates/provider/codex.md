# Codex Global Critical Guardrails

This is the intentionally small global Codex mirror for the owner's highest-risk working rules.

Install/reconcile it as `$CODEX_HOME/AGENTS.md`; the default Codex home is `~/.codex`, so the default file is `~/.codex/AGENTS.md`.

It does not replace repository `AGENTS.md` or `PROJECT_RULES.md`. Project/directory instructions still supply the real project context. Keep this file universal: no project-specific paths, ports, domains, credentials, or product facts.

## Critical working rules

- Read the repository `AGENTS.md`, `PROJECT_RULES.md`, and routed project docs before non-trivial work.
- Explain and verify work **outcome-first**: say what the user/process can actually do, then the internal function/module details if needed.
- For behavior changes and bug fixes use **TDD**: reproduce with a failing test, prove RED, implement the minimum GREEN fix, then run regressions.
- Every relevant **acceptance criterion** needs its own proof before `In Review` or `Done`.
- If the criterion is a user action/UI behavior, execute that action on the actual **topmost user-facing target** in a real rendered/runtime surface. Source/string/DOM-presence checks are not a substitute.
- If required browser/runtime verification cannot run, report **BLOCKED** and keep the task out of Review/Done. Never call missing proof a pass.
- If the task/project requires `VISUAL APPROVAL`, get explicit owner approval on a production-faithful current UI/prototype before visible implementation.
- In authored UI, new `!important` is a hard failure unless there is an exact approved/documented exception.
- Run the project-required lint/build/tests plus real browser/responsive checks relevant to the acceptance. Check Console/Network when they can reveal user-facing failures.
- Review must point to the exact SHA/version and a **reviewer-accessible** current artifact/preview when visual/runtime review is required. A stale preview is not evidence.
- Never weaken/delete tests or verification merely to make a gate green.
- Never claim verified behavior, deployment, access, or test results that did not actually run.

Canonical detailed doctrine remains in Vaoferi Start Here and its conditional skills. This global layer intentionally duplicates only these critical guardrails so they remain present even before repository-specific routing is loaded.
