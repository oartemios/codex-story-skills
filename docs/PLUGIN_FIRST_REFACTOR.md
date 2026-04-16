# Plugin-First Refactor

Status: implemented as a minimal coherent refactor.

## 1. Final Folder Structure

```text
codex-story-skills/
  .codex-dev/
    skills/
      _shared/
      CONVENTIONS.md
      continuity-keeper/
      obsidian-compat/
      project-bootstrap/
      project-orchestrator/
      rfc-adr-assistant/
      story-analyst/
      writer-assistant/
    bundles/
      engineering-addon.yaml
      fiction-core.yaml
      full.yaml
      obsidian-addon.yaml
    scripts/
      build-plugins.py
      package-release-assets.py
      sync-to-codex.sh
      validate-skills.py
  plugins/
    .gitkeep        # generated plugin bundles appear here locally, ignored by git
  scripts/
    install-package.sh
```

`.codex-dev/skills/` is the only source of truth for skill source. `plugins/` is a local generated output directory and must not commit copied skill trees.

## 2. Migration Plan

1. Move raw source skills from top-level `skills/` to `.codex-dev/skills/`.
2. Move build/dev tooling from top-level `scripts/` to `.codex-dev/scripts/`.
3. Keep only public install entrypoints in top-level `scripts/`.
4. Rename `developers-skills` to `rfc-adr-assistant`.
5. Add internal bundle manifests under `.codex-dev/bundles/`.
6. Generate plugin bundles under `plugins/` locally for validation and release packaging.
7. Update docs so plugin installation is the primary workflow.
8. Keep raw sync hidden as a development helper only.

## 3. File Rename And Move Plan

Moved:

- `skills/` -> `.codex-dev/skills/`
- `scripts/validate-skills.py` -> `.codex-dev/scripts/validate-skills.py`
- `scripts/sync-to-codex.sh` -> `.codex-dev/scripts/sync-to-codex.sh`

Renamed:

- `.codex-dev/skills/developers-skills/` -> `.codex-dev/skills/rfc-adr-assistant/`
- skill frontmatter `name: developers-skills` -> `name: rfc-adr-assistant`

Added:

- `.codex-dev/skills/obsidian-compat/`
- `.codex-dev/bundles/*.yaml`
- `.codex-dev/scripts/build-plugins.py`
- `.codex-dev/scripts/package-release-assets.py`
- `plugins/.gitkeep`
- new plugin-first `scripts/install-package.sh`

## 4. Plugin Build Strategy

The build script reads `.codex-dev/bundles/*.yaml` and copies selected source skills into `plugins/<bundle>/skills/` locally. `plugins/*` is ignored so generated skill copies are not stored in the repository.

Bundle model:

- `fiction-core`: default fiction package
- `engineering-addon`: optional `rfc-adr-assistant`
- `obsidian-addon`: `fiction-core` plus optional `obsidian-compat`
- `full`: includes all current bundles

Generated plugins include `.codex-plugin/plugin.json` and a generated `README.md`. They should not be edited manually or committed.

Build command:

```bash
python3 .codex-dev/scripts/build-plugins.py
```

Validation command:

```bash
python3 .codex-dev/scripts/validate-skill-language.py
python3 .codex-dev/scripts/validate-skills.py
```

## 5. Release Asset Strategy

Release assets are zip files made from generated plugin directories:

- `fiction-core.zip`
- `engineering-addon.zip`
- `obsidian-addon.zip`
- `full.zip`

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
bash /tmp/codex-story-skills-install.sh --version v0.1.0
```

Addon:

```bash
bash /tmp/codex-story-skills-install.sh --plugin engineering-addon --version v0.1.0
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

- Existing users with raw skills installed under `~/.codex/skills` may keep stale copies until they remove or ignore them.
- The skill rename from `developers-skills` to `rfc-adr-assistant` changes trigger names and documentation references.
- Generated plugin bundles duplicate source skills only in local build output and release assets; `.codex-dev/skills/` remains canonical in git.
- `obsidian-addon` is optional but installable on its own: it includes `fiction-core` plus Obsidian compatibility. It should not make Obsidian a required runtime or source of truth.
- `full` can install overlapping skills if users also install individual addons. Prefer either `fiction-core` plus selected addons, or `full`, not both.
- Release installation depends on uploaded zip assets matching the generated plugin directory names.
- Marketplace registration writes to a local marketplace file; Codex may need restart or plugin management reload to show new entries.
