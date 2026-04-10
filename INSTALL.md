# Установка

## Установка в Codex Home

```bash
scripts/sync-to-codex.sh
```

## Предварительная проверка без изменений

```bash
scripts/sync-to-codex.sh --dry-run
```

## Что делает безопасная синхронизация

- валидирует пакет перед установкой
- создает backup управляемых элементов в `~/.codex/skill-backups/`
- заменяет старые симлинки, если они ещё остались
- синхронизирует только runtime-слой `skills/`
- не трогает посторонние элементы в `~/.codex/skills`, например `.system`

## Проверка после установки

```bash
ls -la ~/.codex/skills
```

В `~/.codex/skills` должны появиться каталоги `writer-assistant`, `story-analyst`, `project-bootstrap`, а также общие файлы `CONVENTIONS.md` и `_shared/`.

Также должен появиться `continuity-keeper` и `project-orchestrator`.
