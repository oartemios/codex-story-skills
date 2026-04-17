# Устранение проблем

## Release Asset Не Найден

Проверь имя plugin и версию:

```bash
bash /tmp/codex-story-skills-install.sh --plugin fiction-core --version v1.0.0
```

Допустимые plugin names:

- `fiction-core`
- `engineering-addon`
- `obsidian-addon`

Для latest GitHub Release asset:

```bash
bash /tmp/codex-story-skills-install.sh --plugin fiction-core --version latest
```

## Marketplace Entry Не Появился

Installer пишет сюда:

```text
~/.agents/plugins/marketplace.json
```

Plugin распаковывается сюда:

```text
~/plugins/<plugin-name>
```

Если использовались custom paths, проверь, что marketplace `source.path` указывает на распакованную plugin directory.

## Codex Не Показывает Plugin

Проверь, что plugin manifest существует:

```bash
test -f ~/plugins/fiction-core/.codex-plugin/plugin.json
```

Затем перезапусти Codex или заново открой plugin management, чтобы он перечитал local marketplace.

## Неверный Routing Skills

Проверь, что установлен ожидаемый package:

- `fiction-core` содержит fiction project skills.
- `engineering-addon` добавляет `rfc-adr-assistant`.
- `obsidian-addon` добавляет `obsidian-compat`.

## Development Build Устарел

Generated plugins нужно пересобрать из текущего source layer:

- migrated skills из `src/content/skills/`
- still-legacy skills из `.codex-dev/skills/`

```bash
python3 .codex-dev/scripts/build-plugins.py
python3 .codex-dev/scripts/validate-skills.py
```

Raw sync — только внутренний helper для локальной проверки source skills:

```bash
.codex-dev/scripts/sync-to-codex.sh --dry-run
```
