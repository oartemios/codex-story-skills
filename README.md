# codex-story-skills

![Plugin CI](https://github.com/oartemios/codex-story-skills/actions/workflows/ci.yml/badge.svg)

Fiction-first плагины для Codex: канон, структура, сюжетная диагностика, continuity-проверки и стартовая раскладка проекта.

Пакет по умолчанию — `fiction-core`. Инженерные RFC/ADR и совместимость с Obsidian подключаются отдельно.

## Какой пакет выбрать

- `fiction-core`: fiction-first workflow для канона, структуры, continuity, диагностики и bootstrap проекта
- `engineering-addon`: опциональный помощник для RFC/ADR
- `obsidian-addon`: опциональная совместимость с Obsidian vault для установленного workflow

## Установка

Базовая установка:

```bash
curl -fsSL https://raw.githubusercontent.com/oartemios/codex-story-skills/v1.0.2/scripts/install-package.sh -o /tmp/codex-story-skills-install.sh
bash /tmp/codex-story-skills-install.sh --version latest
```

Установка отдельного пакета:

```bash
bash /tmp/codex-story-skills-install.sh --plugin engineering-addon --version latest
bash /tmp/codex-story-skills-install.sh --plugin obsidian-addon --version latest
```

Установка комбинации:

```bash
bash /tmp/codex-story-skills-install.sh --preset obsidian-engineering --version latest
bash /tmp/codex-story-skills-install.sh --plugin engineering-addon --plugin obsidian-addon --version latest
```

После установки открой управление плагинами Codex и установи зарегистрированный локальный plugin или plugins.

Больше вариантов установки: `INSTALL.md`.

## Что входит

`fiction-core` содержит:

- `project-orchestrator`: выбирает следующий skill, маршрут и порядок работы
- `continuity-keeper`: проверяет изменения канона, сломанные связи и последствия правок
- `writer-assistant`: собирает канон, структуру, персонажей, конфликты и рабочие документы
- `story-analyst`: диагностирует ритм, противоречия, арки и сюжетные риски
- `project-bootstrap`: создает или выравнивает структуру проекта

Опциональные addons:

- `rfc-adr-assistant`: пишет, обновляет и проверяет инженерные RFC/ADR
- `obsidian-compat`: сопоставляет установленный workflow с Obsidian vault-навигацией

Подробные границы skills: `SKILLS.md`.

## Первые запросы

```text
Хочу проработать книгу 1. Что делать сначала?
Собери рабочий канон по этим материалам.
Проверь ритм книги и сюжетные риски.
Оформи ADR по этому решению.
Сопоставь мой Obsidian vault с проектной структурой.
```

Больше примеров: `EXAMPLES.md`.

## Документация

- `INSTALL.md`: варианты установки
- `SKILLS.md`: каталог skills и границы routing
- `EXAMPLES.md`: примеры первых запросов
- `TROUBLESHOOTING.md`: проблемы установки и routing
- `docs/ARCHITECTURE.md`: архитектура репозитория и модель сборки
- `docs/PACKAGING.md`: целевая multi-agent packaging модель
- `docs/RELEASE.md`: release workflow и контракт assets
- `CONTRIBUTING.md`: разработка skills и plugin build workflow
- `CHANGELOG.md`: история релизов

## Лицензия

MIT. См. `LICENSE`.
