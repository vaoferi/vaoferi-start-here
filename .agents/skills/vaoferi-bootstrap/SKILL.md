---
name: vaoferi-bootstrap
description: Use when starting work in a new or unsynchronized repository, or when project context/rules are missing or conflicting. Discover known facts first and ask only for unresolved decisions.
---

# Vaoferi Bootstrap

Мета: підготувати repo до автономної роботи без повторних запитань і без вигаданих project facts.

## Resolve Before Asking

Для кожного потрібного факту перевіряй у такому порядку:

1. код, config, package manifests, CI, Git metadata;
2. current project docs, tests, ADR/runbooks;
3. active task source (`Linear`) і вже встановлені Vaoferi owner defaults;
4. актуальні офіційні зовнішні джерела, якщо факт version-sensitive;
5. питання власнику лише коли відповідь відсутня, конфліктна або є справжнім preference/priority decision.

Не проси власника виконувати пошук, який можеш зробити доступними інструментами.

## Minimum Context

З'ясуй настільки, наскільки це реально потрібно задачі або першому setup:

- purpose і primary user/process outcome;
- stack/runtime/package manager;
- build/test/lint commands;
- deploy/preview environment, якщо релевантно;
- production/data/security boundaries;
- product/site/content languages;
- interaction language з власником окремо від product language;
- design source of truth;
- CI і project source-of-truth docs;
- unresolved decisions/conflicts.

Не вигадуй значення для "повноти".

## Existing Repository Handoff

Bootstrap discovers facts; it does not decide that old project documentation is disposable.

If an existing repository contains legacy, nested, duplicated, stale or conflicting governance/design/provider/task documentation, load `vaoferi-project-adaptation` before cleanup or replacement. Let that skill perform recursive inventory, classification, conflict resolution, migration, parity and retirement checks.

A clean/new repository can skip that heavier adaptation pass when there is no pre-existing knowledge to reconcile.

## Output

Після discovery:

- коротко зафіксуй confirmed facts;
- окремо переліч unresolved/conflicting decisions;
- постав тільки питання, що реально блокують наступний крок;
- якщо `PROJECT_RULES.md` уже існує, не перезаписуй його мовчки;
- bootstrap/update universal-owned files роби через canonical sync mechanism, коли він доступний;
- якщо потрібна legacy-doc reconciliation, передай confirmed context у `vaoferi-project-adaptation`, а не починай cleanup навмання.
