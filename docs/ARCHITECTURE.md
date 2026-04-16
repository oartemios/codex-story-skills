# Архитектура

Репозиторий устроен как plugin-first пакет.

## Структура репозитория

```text
codex-story-skills/
  .codex-dev/
    skills/          # источник истины для atomic skills
    bundles/         # внутренние bundle manifests
    scripts/         # сборка, валидация, release и dev tooling
  plugins/           # ignored локальный build output
  scripts/           # публичные install entrypoints
  docs/
```

## Источник истины

Исходные atomic skills живут только в `.codex-dev/skills/`.

Bundle manifests лежат в `.codex-dev/bundles/*.yaml` и описывают, какие skills попадают в каждый plugin release asset.

Сгенерированные plugin bundles собираются локально в `plugins/` и игнорируются git. Release zip-файлы собираются в `dist/` и тоже игнорируются.

## Модель bundles

- `fiction-core`: основной fiction-first пакет
- `engineering-addon`: опциональная поддержка RFC/ADR
- `obsidian-addon`: опциональная совместимость с Obsidian workspace, независимая от доменных пакетов
- `full`: `fiction-core` + `engineering-addon` + `obsidian-addon`

## Сборка

```bash
python3 .codex-dev/scripts/build-plugins.py
python3 .codex-dev/scripts/validate-language.py --scope all
python3 .codex-dev/scripts/validate-skills.py
python3 .codex-dev/scripts/package-release-assets.py
```

## Release

Теги `v*` запускают `.github/workflows/release.yml`.

Release workflow собирает plugin bundles, валидирует их, упаковывает release assets и загружает:

- `fiction-core.zip`
- `engineering-addon.zip`
- `obsidian-addon.zip`
- `full.zip`

## Raw Dev Sync

Raw sync оставлен только для локальной проверки исходных skills:

```bash
.codex-dev/scripts/sync-to-codex.sh --dry-run
```

Не использовать raw sync как публичный install workflow.
