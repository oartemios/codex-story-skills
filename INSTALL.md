# Установка

## Стабильная установка

Основной путь для пользователя:

```bash
curl -fsSL https://raw.githubusercontent.com/oartemios/codex-story-skills/v0.1.0/scripts/install-package.sh -o /tmp/codex-story-skills-install.sh
bash /tmp/codex-story-skills-install.sh --ref v0.1.0
```

Перед запуском можно просмотреть скачанный скрипт:

```bash
less /tmp/codex-story-skills-install.sh
```

Этот способ не использует `curl | bash`: скрипт скачивается отдельным файлом, и его можно проверить перед запуском.

При установке по release tag Git может вывести предупреждение про tag object или detached HEAD. Это нормально для стабильного тега; если установка завершается сообщением `Sync completed.`, пакет установлен корректно.

## Ручная установка через clone

```bash
git clone --branch v0.1.0 https://github.com/oartemios/codex-story-skills.git
cd codex-story-skills
scripts/sync-to-codex.sh
```

Для последней версии разработки используй `main` вместо `v0.1.0`.

Для установки в нестандартный каталог:

```bash
bash /tmp/codex-story-skills-install.sh --ref v0.1.0 --dest /path/to/codex/skills
```

При ручной установке через clone можно использовать:

```bash
scripts/sync-to-codex.sh --dest /path/to/codex/skills
```

## Предварительная проверка без изменений

При ручной установке через clone:

```bash
scripts/sync-to-codex.sh --dry-run
```

## Что делает безопасная синхронизация

- валидирует пакет перед установкой
- создает backup управляемых элементов в `~/.codex/skill-backups/`
- заменяет старые симлинки, если они ещё остались
- синхронизирует только runtime-слой `skills/`
- не трогает посторонние элементы в `~/.codex/skills`, например `.system`

Если указан `--dest`, backup по умолчанию создается в соседнем каталоге `skill-backups`.
Путь backup можно переопределить через `--backup-root`.

## Проверка после установки

```bash
ls -la ~/.codex/skills
```

В `~/.codex/skills` должны появиться каталоги `writer-assistant`, `story-analyst`, `project-bootstrap`, а также общие файлы `CONVENTIONS.md` и `_shared/`.

Также должен появиться `continuity-keeper` и `project-orchestrator`.
