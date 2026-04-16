# Release

This project is distributed as GitHub Release assets.

## Assets

Each release must publish:

- `fiction-core.zip`
- `engineering-addon.zip`
- `obsidian-addon.zip`
- `full.zip`

These files are built from `.codex-dev/bundles/*.yaml` and `.codex-dev/skills/`.

## Automated Release

Create and push a version tag:

```bash
git tag v0.2.0
git push origin v0.2.0
```

GitHub Actions runs `.github/workflows/release.yml`, builds plugin bundles, validates them, packages release assets, and uploads the zip files to the GitHub Release.

The release workflow can also be run manually with `workflow_dispatch` and an explicit tag.

## Local Preflight

Before tagging:

```bash
python3 .codex-dev/scripts/build-plugins.py
python3 .codex-dev/scripts/validate-skill-language.py
python3 .codex-dev/scripts/validate-skills.py
python3 .codex-dev/scripts/package-release-assets.py
```

Confirm local assets exist:

```bash
test -f dist/fiction-core.zip
test -f dist/engineering-addon.zip
test -f dist/obsidian-addon.zip
test -f dist/full.zip
```

`plugins/` and `dist/` are ignored local build outputs. Do not commit generated plugin bundles or zip assets.

## User Install Contract

The installer downloads assets using:

```text
https://github.com/oartemios/codex-story-skills/releases/download/<tag>/<plugin>.zip
```

Do not rename release assets without updating `scripts/install-package.sh` and install docs.

The installer supports multiple plugins in one run, so every independently installable asset must be present in each release.
