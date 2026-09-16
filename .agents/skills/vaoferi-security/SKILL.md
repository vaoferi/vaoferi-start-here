---
name: vaoferi-security
description: Use for secrets, credentials, authentication, authorization, permissions, privacy, exposed data, security-sensitive configuration, or destructive security remediation.
---

# Vaoferi Security

## Practical Local Secret Policy

- A local `.env`, `.env.local` or project-equivalent secret file is an **approved normal working store** for deploy, migration, API and tool credentials when the file is private to the intended machine/workspace and ignored by Git.
- Prefer an existing project-local secret convention over introducing a new secret manager or making the owner re-enter keys repeatedly.
- Do **not** delete, blank, rotate or migrate a working local secret file to Vaultwarden/another manager merely because it contains real credentials.
- Agents may read approved local env/config values when the task needs them and tool access permits it. Do not echo the values into chat, logs, issues, docs or reports.
- Convenience wins over additional secret-management ceremony when the credential remains local/private and the current mechanism is reliable.

## Hard Boundaries

- Do not commit or intentionally track a real `.env`/credential file. Safe examples/templates are allowed.
- Do not bundle local secrets into public/shared artifacts or copy them to a deployment target unless that runtime explicitly requires its own protected server-side configuration.
- Do not expose secret values in chat, issues, Linear, Trello, docs, logs, screenshots or tests without a concrete unavoidable need.
- If a credential was committed to a public/shared repository, published, logged to an untrusted/shared system, or otherwise actually exposed, treat that as a real incident; deleting the latest copy alone is not enough.
- For an exposed credential, rotation/revocation may be required, but destructive credential actions still need the appropriate authorization and consumer/rollback checks.
- Do not rewrite Git history, delete production data or change auth/permissions destructively without explicit approval and a rollback plan.

## Verification

- For local secret stores, verify the file is ignored/untracked (`git check-ignore` / `git status` / equivalent) rather than deleting it.
- When relevant, verify deploy/package tooling does not accidentally include the local secret file.
- Secret scanners and failure output must report path + rule/class, never the secret value itself.
- After real exposure remediation, verify the active credential/config still works and the exposed value is no longer valid when rotation was in scope.
