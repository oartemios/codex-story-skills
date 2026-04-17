# Plugin-First Refactor

Status: historical record of the plugin-first refactor.

Current note: product module manifests live in `src/modules/`, and source content lives in `src/content/skills/`.

## 1. Final Folder Structure

```text
codex-story-skills/
  .codex-dev/
    skills/
      continuity-keeper/
      project-bootstrap/
      project-orchestrator/
      rfc-adr-assistant/
      story-analyst/
      writer-assistant/
    scripts/
      build-plugins.py
      package-release-assets.py
      sync-to-codex.sh
      validate-skills.py
  plugins/
    .gitkeep        # generated plugin bundles appear here locally, ignored by git
  src/
    content/
      shared/
      skills/
        obsidian-compat/
    modules/
      engineering-addon.yaml
      fiction-core.yaml
      obsidian-addon.yaml
  scripts/
    install-package.sh
```

Skill source is canonical in `src/content/skills/`. `plugins/` is a local generated output directory and must not commit copied skill trees.

## 2. Migration Plan

1. Move build/dev tooling from top-level `scripts/` to `.codex-dev/scripts/`.
2. Keep only public install entrypoints in top-level `scripts/`.
3. Rename the RFC/ADR skill to `rfc-adr-assistant`.
4. Add internal bundle manifests. Current path: `src/modules/`.
5. Generate plugin bundles under `plugins/` locally for validation and release packaging.
6. Update docs so plugin installation is the primary workflow.
7. Keep raw sync hidden as a development helper only.

## 3. File Rename And Move Plan

Moved:

- `scripts/validate-skills.py` -> `.codex-dev/scripts/validate-skills.py`
- `scripts/sync-to-codex.sh` -> `.codex-dev/scripts/sync-to-codex.sh`

Renamed:

- skill frontmatter `name` updated to `rfc-adr-assistant`

Added:

- `src/modules/*.yaml`
- `.codex-dev/scripts/build-plugins.py`
- `.codex-dev/scripts/package-release-assets.py`
- `plugins/.gitkeep`
- new plugin-first `scripts/install-package.sh`

## 4. Plugin Build Strategy

The build script reads `src/modules/*.yaml` and copies selected source skills into `plugins/<bundle>/skills/` locally. `plugins/*` is ignored so generated skill copies are not stored in the repository.

Bundle model:

- `fiction-core`: default fiction package
- `engineering-addon`: optional `rfc-adr-assistant`
- `obsidian-addon`: optional `obsidian-compat`, independent from domain packages

Generated plugins include `.codex-plugin/plugin.json` and a generated `README.md`. They should not be edited manually or committed.

Build command:

```bash
python3 .codex-dev/scripts/build-plugins.py
```

Validation command:

```bash
python3 .codex-dev/scripts/validate-language.py --scope all
python3 .codex-dev/scripts/validate-skills.py
```

## 5. Release Asset Strategy

Release assets are zip files made from generated plugin directories:

- `fiction-core.zip`
- `engineering-addon.zip`
- `obsidian-addon.zip`

Package command:

```bash
python3 .codex-dev/scripts/package-release-assets.py
```

The release workflow in `.github/workflows/release.yml` builds plugins, validates them, packages zips into `dist/`, then uploads the zips as GitHub Release assets.

## 6. Install Flow Design

User flow:

1. Download `scripts/install-package.sh`.
2. Run it with `--plugin <name>` and `--version <tag>`.
3. The script downloads `<plugin>.zip` from GitHub Releases.
4. The script unpacks the plugin under `~/plugins/<plugin-name>`.
5. The script registers the local plugin in `~/.agents/plugins/marketplace.json`.
6. Codex plugin management installs the registered plugin.

Default:

```bash
bash /tmp/codex-story-skills-install.sh --version v1.0.1
```

Addon:

```bash
bash /tmp/codex-story-skills-install.sh --plugin engineering-addon --version v1.0.1
bash /tmp/codex-story-skills-install.sh --plugin engineering-addon --plugin obsidian-addon --version v1.0.1
bash /tmp/codex-story-skills-install.sh --preset obsidian-engineering --version v1.0.1
```

## 7. README And INSTALL Update Plan

README now presents:

- plugin-first package identity
- `fiction-core` as the default
- optional `engineering-addon` and `obsidian-addon`
- `.codex-dev/` as internal source/build layer
- `plugins/` as ignored local generated output
- raw sync as development-only

INSTALL now presents:

- release asset download as the main path
- plugin choices
- local marketplace registration
- custom asset URL support
- raw sync as internal-only

## 8. Risks And Compatibility Notes

- The RFC/ADR skill rename changes trigger names and documentation references.
- Generated plugin bundles duplicate source skills only in local build output and release assets; `src/content/skills/` is the canonical source layer.
- `obsidian-addon` is optional and installable on its own. It adapts to `fiction-core`, `engineering-addon`, or both when those packages are installed, but should not make Obsidian a required runtime or source of truth.
- Release installation depends on uploaded zip assets matching the generated plugin directory names.
- Marketplace registration writes to a local marketplace file; Codex may need restart or plugin management reload to show new entries.
