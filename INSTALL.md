# Установка

Основной способ установки - через готовый plugin bundle из GitHub Release.

## Fiction Core

`fiction-core` - пакет по умолчанию:

```bash
curl -fsSL https://raw.githubusercontent.com/oartemios/codex-story-skills/v1.0.1/scripts/install-package.sh -o /tmp/codex-story-skills-install.sh
bash /tmp/codex-story-skills-install.sh --version v1.0.1
```

Скрипт можно сначала прочитать:

```bash
less /tmp/codex-story-skills-install.sh
```

## Опциональные Addons

```bash
bash /tmp/codex-story-skills-install.sh --plugin engineering-addon --version v1.0.1
bash /tmp/codex-story-skills-install.sh --plugin obsidian-addon --version v1.0.1
```

`obsidian-addon` устанавливается как самостоятельный пакет и может использоваться вместе с `fiction-core`, `engineering-addon` или обоими пакетами.

## Комбинации Plugins

Можно установить несколько пакетов за один запуск:

```bash
bash /tmp/codex-story-skills-install.sh \
  --plugin engineering-addon \
  --plugin obsidian-addon \
  --version v1.0.1
```

То же самое через preset:

```bash
bash /tmp/codex-story-skills-install.sh --preset obsidian-engineering --version v1.0.1
```

Доступные presets:

- `fiction`: `fiction-core`
- `engineering`: `engineering-addon`
- `obsidian`: `obsidian-addon`
- `obsidian-fiction`: `fiction-core` + `obsidian-addon`
- `obsidian-engineering`: `engineering-addon` + `obsidian-addon`

Доступные plugin assets:

- `fiction-core.zip`
- `engineering-addon.zip`
- `obsidian-addon.zip`

## Что делает Installer

1. Скачивает GitHub Release asset.
2. Распаковывает plugin в `~/plugins/<plugin-name>`.
3. Добавляет или обновляет запись plugin в `~/.agents/plugins/marketplace.json`.
4. Оставляет финальную установку на стороне Codex plugin management.

Installer не копирует raw skills в `~/.codex/skills`.

## Custom Asset URL

Для локальной проверки или private release assets:

```bash
bash /tmp/codex-story-skills-install.sh \
  --plugin fiction-core \
  --asset-url https://example.com/fiction-core.zip
```

`--asset-url` работает только при установке одного plugin.

## Кастомные Локальные Пути

```bash
bash /tmp/codex-story-skills-install.sh \
  --plugin fiction-core \
  --plugin-root /path/to/plugins \
  --marketplace /path/to/.agents/plugins/marketplace.json
```

## Development Install

Raw skill sync — внутренний development helper, а не публичный install path:

```bash
python3 .codex-dev/scripts/build-plugins.py
.codex-dev/scripts/sync-to-codex.sh --dry-run
```

Используй его только для локальной проверки source skills.
