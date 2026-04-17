# Contributing

This repository is plugin-first.

For repository layout and build architecture, see `docs/ARCHITECTURE.md`.

## Source Of Truth

- Legacy atomic source skills that are not yet migrated live in `.codex-dev/skills/`.
- Migrated agent-neutral skill content lives in `src/content/skills/`.
- Shared conventions and shared templates live in `src/content/shared/`.
- Product module manifests live in `src/modules/`.
- Build, validation, packaging, and raw dev sync tooling lives in `.codex-dev/scripts/`.
- Generated installable plugins are built into `plugins/` locally.
- Public user-facing scripts live in `scripts/`.

Do not commit generated plugin bundles or copied skill trees. Change `.codex-dev/skills/`, `src/content/`, or `src/modules/`, then rebuild locally.

## Local Build

```bash
python3 .codex-dev/scripts/build-plugins.py
python3 .codex-dev/scripts/validate-language.py --scope all
python3 .codex-dev/scripts/validate-skills.py
python3 .codex-dev/scripts/package-release-assets.py
```

Release zips are written to `dist/`. Both `plugins/` build output and `dist/` are ignored; source content remains split between `.codex-dev/skills/` for unmigrated skills and `src/content/` for migrated skills.

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

The release workflow builds plugin bundles from `src/modules/*.yaml`, validates them, packages zip assets, and uploads them to GitHub Release.

See `docs/RELEASE.md`.

## Raw Dev Sync

Raw sync is retained only for local source testing:

```bash
.codex-dev/scripts/sync-to-codex.sh --dry-run
.codex-dev/scripts/sync-to-codex.sh
```

Do not present raw sync as the public install path. Users install built plugin release assets through `scripts/install-package.sh`.

## Adding Or Moving Skills

1. Add or update the atomic skill under `src/content/skills/<skill-name>/` for new migrated content, or `.codex-dev/skills/<skill-name>/` for legacy content.
2. For migrated content, keep `skill.yaml` valid with `id`, `description_ru`, and `entrypoint`.
3. For legacy content, keep `SKILL.md` frontmatter valid with `name` and `description`.
4. Put migrated rules in `rules/`; keep legacy reusable rules in `references/` only for unmigrated content; keep templates in `templates/`.
5. Add the skill to the relevant `src/modules/*.yaml` manifest.
6. Rebuild plugins and validate.

The RFC/ADR skill is named `rfc-adr-assistant`. Do not reintroduce `developers-skills`.

## Bundle Rules

- `fiction-core` is the default product.
- `engineering-addon` is opt-in.
- `obsidian-addon` is opt-in and independent; it adapts to `fiction-core`, `engineering-addon`, or both when those packages are installed.

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
