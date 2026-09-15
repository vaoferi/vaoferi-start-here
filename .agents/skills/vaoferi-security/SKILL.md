---
name: vaoferi-security
description: Use for secrets, credentials, authentication, authorization, permissions, privacy, exposed data, security-sensitive configuration, or destructive security remediation.
---

# Vaoferi Security

## Hard Rules

- Не копіюй secret values у chat, issue, docs, logs, tests або нові commits без необхідності.
- Не трекай real `.env`; дозволені лише явно safe examples/templates.
- У звітах використовуй least disclosure: path + class/rule + impact, без самого secret value.
- Якщо credential був у public repo/history або іншому ненадійному місці, вважай його exposed; простого видалення з latest commit недостатньо.
- Для exposed credential рекомендуй/виконуй rotation лише з явною авторизацією на destructive credential action; після rotation перевір consumers і revoke old secret.
- Не переписуй Git history, не видаляй production data і не змінюй auth/permissions destructive способом без окремого approval та rollback plan.
- Security/privacy/data integrity constraints не знижуються заради швидкості або бізнес-зручності.

## Verification

- Перевір tracked files, config ownership і relevant scanner/tests.
- Не друкуй знайдені secrets у failure output.
- Після remediation перевір, що active credential/config працює, а exposed value більше не є чинним, якщо rotation входила в scope.
