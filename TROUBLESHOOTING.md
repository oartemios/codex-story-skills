# Troubleshooting

## Release Asset Not Found

Check the plugin name and version:

```bash
bash /tmp/codex-story-skills-install.sh --plugin fiction-core --version v0.1.0
```

Valid plugin names:

- `fiction-core`
- `engineering-addon`
- `obsidian-addon`
- `full`

For the latest GitHub Release asset:

```bash
bash /tmp/codex-story-skills-install.sh --plugin fiction-core --version latest
```

## Marketplace Entry Is Missing

The installer writes to:

```text
~/.agents/plugins/marketplace.json
```

The plugin is unpacked under:

```text
~/plugins/<plugin-name>
```

If custom paths were used, confirm that the marketplace `source.path` points to the unpacked plugin directory.

## Codex Does Not Show The Plugin

Confirm the plugin manifest exists:

```bash
test -f ~/plugins/fiction-core/.codex-plugin/plugin.json
```

Then restart Codex or reopen plugin management so it reloads the local marketplace.

## Wrong Skill Routes

Confirm the expected package is installed:

- `fiction-core` contains fiction project skills only.
- `engineering-addon` adds `rfc-adr-assistant`.
- `obsidian-addon` adds `obsidian-compat`.
- `full` contains all current skills.

## Development Build Looks Stale

Generated plugins must be rebuilt from `.codex-dev/skills/`:

```bash
python3 .codex-dev/scripts/build-plugins.py
python3 .codex-dev/scripts/validate-skills.py
```

Raw sync is internal-only and should be used only for local source testing:

```bash
.codex-dev/scripts/sync-to-codex.sh --dry-run
```
