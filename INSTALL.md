# Установка

Основной способ установки - через готовый plugin bundle из GitHub Release.

## Fiction Core

`fiction-core` - пакет по умолчанию:

```bash
curl -fsSL https://raw.githubusercontent.com/oartemios/codex-story-skills/v1.0.0/scripts/install-package.sh -o /tmp/codex-story-skills-install.sh
bash /tmp/codex-story-skills-install.sh --version v1.0.0
```

Скрипт можно сначала прочитать:

```bash
less /tmp/codex-story-skills-install.sh
```

## Optional Addons

```bash
bash /tmp/codex-story-skills-install.sh --plugin engineering-addon --version v1.0.0
bash /tmp/codex-story-skills-install.sh --plugin obsidian-addon --version v1.0.0
bash /tmp/codex-story-skills-install.sh --plugin full --version v1.0.0
```

`obsidian-addon` устанавливается как самостоятельный пакет и может использоваться вместе с `fiction-core`, `engineering-addon` или обоими пакетами.

## Plugin Combinations

Можно установить несколько пакетов за один запуск:

```bash
bash /tmp/codex-story-skills-install.sh \
  --plugin engineering-addon \
  --plugin obsidian-addon \
  --version v1.0.0
```

То же самое через preset:

```bash
bash /tmp/codex-story-skills-install.sh --preset obsidian-engineering --version v1.0.0
```

Доступные presets:

- `fiction`: `fiction-core`
- `engineering`: `engineering-addon`
- `obsidian`: `obsidian-addon`
- `obsidian-fiction`: `fiction-core` + `obsidian-addon`
- `obsidian-engineering`: `engineering-addon` + `obsidian-addon`
- `full`: `full`

Доступные plugin assets:

- `fiction-core.zip`
- `engineering-addon.zip`
- `obsidian-addon.zip`
- `full.zip`

## What The Installer Does

1. Downloads a GitHub Release asset.
2. Unpacks the plugin under `~/plugins/<plugin-name>`.
3. Adds or updates the plugin entry in `~/.agents/plugins/marketplace.json`.
4. Leaves final installation to Codex plugin management.

The installer does not copy raw skills into `~/.codex/skills`.

## Custom Asset URL

For local testing or private release assets:

```bash
bash /tmp/codex-story-skills-install.sh \
  --plugin fiction-core \
  --asset-url https://example.com/fiction-core.zip
```

`--asset-url` работает только при установке одного plugin.

## Custom Local Paths

```bash
bash /tmp/codex-story-skills-install.sh \
  --plugin fiction-core \
  --plugin-root /path/to/plugins \
  --marketplace /path/to/.agents/plugins/marketplace.json
```

## Development Install

Raw skill sync is an internal development helper, not the public install path:

```bash
python3 .codex-dev/scripts/build-plugins.py
.codex-dev/scripts/sync-to-codex.sh --dry-run
```

Use it only when testing source skills locally.
