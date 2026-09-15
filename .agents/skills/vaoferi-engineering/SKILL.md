---
name: vaoferi-engineering
description: Use for non-trivial implementation, bug fixes, refactors, tests, or engineering documentation when the universal AGENTS core is not enough.
---

# Vaoferi Engineering

## Procedure

1. Прочитай `PROJECT_RULES.md` і релевантні project docs/code перед змінами.
2. Сформулюй user/process outcome і перевір фактичний current behavior.
3. Знайди існуючу реалізацію, contract, native capability або dependency перед створенням нової логіки.
4. Для behavior change або bug fix застосуй TDD: failing test → verify red → minimal implementation → verify green → refactor only while green.
5. Змінюй мінімальну кількість пов'язаних файлів; не роби глобальний replace без target-list review.
6. Запусти релевантні tests/lint/build/runtime checks, потім перевір diff.
7. Поясни результат outcome-first; явно назви неперевірене.

## Documentation

- ADR створюй лише для durable/hard-to-reverse architecture or domain decision.
- Не створюй progress logs, дублікати README або документацію, яку ніхто не читає.
- Якщо project already має canonical SPEC/ADR/TESTING format — використовуй його замість нового формату.
