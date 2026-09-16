---
name: vaoferi-task-tracking
description: Use when reading, migrating, creating, updating, or retiring work items across Linear and legacy Trello so there is only one active source of truth.
---

# Vaoferi Task Tracking

## Invariant

`Linear` — єдине активне джерело робочих задач. `Trello` — тимчасове legacy input для міграції, не planner і не довгостроковий archive.

## Trello → Linear Procedure

1. Не створюй нову work card у Trello.
2. Коли релевантна Trello card з'являється в роботі, прочитай її повністю: description, comments, checklists, attachments/context якщо доступні.
3. Перенеси кожну ще корисну незавершену дію в Linear або в уже існуючу Linear issue.
4. Durable facts/decisions, яким не місце у task tracker, перенеси в canonical docs/tests/code comments лише коли це правильний long-term source.
5. Перевір parity: у Trello не залишилось унікальної корисної інформації чи незавершеної роботи.
6. Після parity фінальний стан — hard-delete card з Trello. Архівування не є завершенням cleanup і не перетворює Trello на історичний archive.
7. Якщо поточний connector/tool не вміє hard-delete, не маскуй це як Done: зафіксуй blocker/pending deletion і використай інший підтримуваний шлях видалення, коли він доступний.
8. У Linear зафіксуй migration destination/evidence настільки коротко, наскільки потрібно для traceability.

Не роби bulk-delete без вичитки. Мета — повністю очистити Trello без silent loss; історія, яку справді треба зберегти, має жити в Linear або canonical docs/tests, а не в Trello.
