---
name: vaoferi-task-tracking
description: Use when reading, migrating, creating, updating, or retiring work items across Linear and legacy Trello so there is only one active source of truth.
---

# Vaoferi Task Tracking

## Invariant

`Linear` — єдине активне джерело робочих задач. `Trello` — legacy input, який поступово очищається.

## Trello → Linear Procedure

1. Не створюй нову work card у Trello.
2. Коли релевантна Trello card з'являється в роботі, прочитай її повністю: description, comments, checklists, attachments/context якщо доступні.
3. Перенеси кожну ще корисну незавершену дію в Linear або в уже існуючу Linear issue.
4. Durable facts/decisions, яким не місце у task tracker, перенеси в canonical docs/tests/code comments лише коли це правильний long-term source.
5. Перевір parity: у Trello не залишилось унікальної корисної інформації чи незавершеної роботи.
6. Після parity прибери card з активного Trello: archive; якщо безпечний hard-delete окремо підтримується й доречний, він може бути наступним cleanup step.
7. У Linear зафіксуй migration destination/evidence настільки коротко, наскільки потрібно для traceability.

Не роби bulk-delete без вичитки. Мета — максимально очистити Trello без silent loss.
