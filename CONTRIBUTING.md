# Contributing

This repository is plugin-first.

For repository layout and build architecture, see `docs/ARCHITECTURE.md`.

## Source Of Truth

- Migrated agent-neutral skill content lives in `src/content/skills/`.
- Shared conventions and shared templates live in `src/content/shared/`.
- Product module manifests live in `src/modules/`.
- Build, validation, packaging, and raw dev sync tooling lives in `scripts/`.
- Generated installable plugins are built into `plugins/` locally.
- Public user-facing scripts live in `scripts/`.

Do not commit generated plugin bundles. Change `src/content/` or `src/modules/`, then rebuild locally.

## Local Build

```bash
python3 scripts/build-plugins.py
python3 scripts/validate-language.py --scope all
python3 scripts/validate-skills.py
python3 scripts/package-release-assets.py
```

Release zips are written to `dist/`. Both `plugins/` build output and `dist/` are ignored; source content lives in `src/content/`.

## Local Hooks

Git hooks are opt-in:

```bash
scripts/install-git-hooks.sh
```

Installed hooks:

- `pre-commit`: validates skill language and package integrity
- `pre-push`: builds plugins, validates language and package integrity, packages release assets, and checks shell syntax

The language validator keeps skill instructions Russian-first while allowing English domain terms such as `Obsidian`, `vault`, `backlinks`, `wikilinks`, `RFC`, and `ADR`.

## Release

Install-ready releases are published by `.github/workflows/release.yml`.

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

The release workflow builds plugin bundles from `src/modules/*.yaml`, validates them, packages zip assets, and uploads them to GitHub Release.

See `docs/RELEASE.md`.

## Raw Dev Sync

Raw sync is retained only for local source testing:

```bash
scripts/sync-to-codex.sh --dry-run
scripts/sync-to-codex.sh
```

Do not present raw sync as the public install path. Users install built plugin release assets through `scripts/install-package.sh`.

## Adding Or Moving Skills

1. Add or update the skill under `src/content/skills/<skill-name>/`.
2. Keep `skill.yaml` valid with `id`, `description_ru`, and `entrypoint`.
3. Put rules in `rules/` and templates in `templates/`.
4. Add the skill to the relevant `src/modules/*.yaml` manifest.
5. Rebuild plugins and validate.

The RFC/ADR skill is named `rfc-adr-assistant`. Do not reintroduce the old RFC/ADR skill name.

## Bundle Rules

- `fiction-core` is the default product.
- `engineering-addon` is opt-in.
- `obsidian-addon` is opt-in and independent; it adapts to `fiction-core`, `engineering-addon`, or both when those packages are installed.

Bundle manifests are internal build inputs, not a user-facing API.

## Checks Before PR

```bash
python3 scripts/build-plugins.py
python3 scripts/validate-language.py --scope all
python3 scripts/validate-skills.py
python3 scripts/package-release-assets.py
bash -n scripts/install-package.sh scripts/sync-to-codex.sh
scripts/install-package.sh --help
```
