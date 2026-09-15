# PROJECT_RULES.md

Цей файл описує лише правила репозиторію `vaoferi-start-here`.

## Purpose

Це public canonical source універсальних правил і reusable skills для AI-агентів у репозиторіях Vaoferi.

## Hard Constraints

- Репозиторій публічний: тут заборонені secrets, credentials, приватні project facts, внутрішні URL, приватні NAS paths та production data.
- Canonical root `AGENTS.md` має залишатися універсальним і не перевищувати 12 KiB UTF-8.
- Universal design doctrine не редагується тут: її canonical source — окремий `vaoferi-design-skill`; тут зберігається лише pinned/vendored copy для offline use.
- `PROJECT_RULES.md` у target repositories є project-owned і ніколи не перезаписується universal sync.
- Централізовано керовані target paths мають бути явно перелічені в manifest; sync не може мовчки перезаписувати manual drift.

## Runtime And Tests

- Python: 3.11+.
- Core scripts: Python standard library unless окрема потреба явно схвалена.
- Tests: `python -m unittest discover -s tests -v`.
- Universal contract check: `python scripts/check_agents_contract.py AGENTS.md`.

## Change Policy

- Universal owner/agent behavior редагується тут і лише потім синхронізується в target repos.
- Project-specific правила не додаються в root `AGENTS.md`.
- Provider-specific quirks живуть у thin provider overlays, а не дублюють universal contract.
- Зміни design methodology спочатку робляться в canonical design repository, потім оновлюється pin/vendor snapshot.
- Release/update має бути deterministic, idempotent і fail-closed на конфлікті ownership/drift.
