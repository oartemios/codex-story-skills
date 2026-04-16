# Contributing

This repository is plugin-first.

For repository layout and build architecture, see `docs/ARCHITECTURE.md`.

## Source Of Truth

- Atomic source skills live only in `.codex-dev/skills/`.
- Bundle manifests live in `.codex-dev/bundles/`.
- Build, validation, packaging, and raw dev sync tooling lives in `.codex-dev/scripts/`.
- Generated installable plugins are built into `plugins/` locally.
- Public user-facing scripts live in `scripts/`.

Do not commit generated plugin bundles or copied skill trees. Change `.codex-dev/skills/` or `.codex-dev/bundles/`, then rebuild locally.

## Local Build

```bash
python3 .codex-dev/scripts/build-plugins.py
python3 .codex-dev/scripts/validate-language.py --scope all
python3 .codex-dev/scripts/validate-skills.py
python3 .codex-dev/scripts/package-release-assets.py
```

Release zips are written to `dist/`. Both `plugins/` build output and `dist/` are ignored; `.codex-dev/skills/` remains the only source of truth.

## Local Hooks

Git hooks are opt-in:

```bash
.codex-dev/scripts/install-git-hooks.sh
```

Installed hooks:

- `pre-commit`: validates skill language and package integrity
- `pre-push`: builds plugins, validates language and package integrity, packages release assets, and checks shell syntax

The language validator keeps skill instructions Russian-first while allowing English domain terms such as `Obsidian`, `vault`, `backlinks`, `wikilinks`, `RFC`, and `ADR`.

## Release

Install-ready releases are published by `.github/workflows/release.yml`.

```bash
git tag v1.0.1
git push origin v1.0.1
```

The release workflow builds plugin bundles from `.codex-dev/bundles/*.yaml`, validates them, packages zip assets, and uploads them to GitHub Release.

See `docs/RELEASE.md`.

## Raw Dev Sync

Raw sync is retained only for local source testing:

```bash
.codex-dev/scripts/sync-to-codex.sh --dry-run
.codex-dev/scripts/sync-to-codex.sh
```

Do not present raw sync as the public install path. Users install built plugin release assets through `scripts/install-package.sh`.

## Adding Or Moving Skills

1. Add or update the atomic skill under `.codex-dev/skills/<skill-name>/`.
2. Keep `SKILL.md` frontmatter valid with `name` and `description`.
3. Put reusable rules in `references/` and templates in `templates/`.
4. Add the skill to the relevant `.codex-dev/bundles/*.yaml` manifest.
5. Rebuild plugins and validate.

The RFC/ADR skill is named `rfc-adr-assistant`. Do not reintroduce `developers-skills`.

## Bundle Rules

- `fiction-core` is the default product.
- `engineering-addon` is opt-in.
- `obsidian-addon` is opt-in and independent; it adapts to `fiction-core`, `engineering-addon`, or both when those packages are installed.
- `full` combines `fiction-core`, `engineering-addon`, and `obsidian-addon`.

Bundle manifests are internal build inputs, not a user-facing API.

## Checks Before PR

```bash
python3 .codex-dev/scripts/build-plugins.py
python3 .codex-dev/scripts/validate-language.py --scope all
python3 .codex-dev/scripts/validate-skills.py
python3 .codex-dev/scripts/package-release-assets.py
bash -n scripts/install-package.sh .codex-dev/scripts/sync-to-codex.sh
scripts/install-package.sh --help
```
