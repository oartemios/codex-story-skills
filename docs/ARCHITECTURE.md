# Архитектура

Репозиторий устроен как plugin-first пакет.

## Структура репозитория

```text
codex-story-skills/
  scripts/           # сборка, валидация, release и dev tooling
  src/
    content/         # agent-neutral source for skills and shared content
    modules/         # agent-neutral product manifests
  plugins/           # ignored локальный build output
  scripts/           # публичные install entrypoints
  docs/
```

Текущая архитектура является Codex plugin-first baseline. Целевое направление для multi-agent packaging описано в `docs/PACKAGING.md`: один общий source layer и отдельные targets для Codex, Claude Code и Qwen Code.

## Источник истины

Agent-neutral source lives in `src/content/skills/`, and shared content remains in `src/content/`.

Product manifests лежат в `src/modules/*.yaml` и описывают, какие skills попадают в каждый plugin release asset. Это первый вынесенный agent-neutral слой целевой multi-agent packaging модели.

Сгенерированные plugin bundles собираются локально в `plugins/` и игнорируются git. Release zip-файлы собираются в `dist/` и тоже игнорируются.

## Модель bundles

- `fiction-core`: основной fiction-first пакет
- `engineering-addon`: опциональная поддержка RFC/ADR
- `obsidian-addon`: опциональная совместимость с Obsidian workspace, независимая от доменных пакетов

## Сборка

```bash
python3 scripts/build-plugins.py
python3 scripts/validate-language.py --scope all
python3 scripts/validate-skills.py
python3 scripts/package-release-assets.py
```

## Release

Теги `v*` запускают `.github/workflows/release.yml`.

Release workflow собирает plugin bundles, валидирует их, упаковывает release assets и загружает:

- `fiction-core.zip`
- `engineering-addon.zip`
- `obsidian-addon.zip`

## Raw Dev Sync

Raw sync оставлен только для локальной проверки исходных skills:

```bash
scripts/sync-to-codex.sh --dry-run
```

Не использовать raw sync как публичный install workflow.
