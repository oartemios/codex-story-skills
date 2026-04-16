# codex-story-skills

![Plugin CI](https://github.com/oartemios/codex-story-skills/actions/workflows/ci.yml/badge.svg)

Fiction-first Codex plugins for projects that need canon, structure, story diagnostics, continuity checks, and project bootstrap support.

The default product is `fiction-core`. Engineering RFC/ADR support and Obsidian compatibility are optional addons.

## Packages

- `fiction-core`: default fiction-first plugin
- `engineering-addon`: optional RFC/ADR assistant
- `obsidian-addon`: optional Obsidian vault compatibility
- `full`: combined plugin with `fiction-core` plus optional addons

## Quick Start

Install the default plugin from a GitHub Release asset:

```bash
curl -fsSL https://raw.githubusercontent.com/oartemios/codex-story-skills/v0.1.0/scripts/install-package.sh -o /tmp/codex-story-skills-install.sh
bash /tmp/codex-story-skills-install.sh --version v0.1.0
```

Install another package:

```bash
bash /tmp/codex-story-skills-install.sh --plugin engineering-addon --version v0.1.0
bash /tmp/codex-story-skills-install.sh --plugin obsidian-addon --version v0.1.0
bash /tmp/codex-story-skills-install.sh --plugin full --version v0.1.0
```

The installer downloads a built plugin asset, unpacks it under `~/plugins`, registers it in `~/.agents/plugins/marketplace.json`, and leaves final installation to Codex plugin management.

More details:

- `INSTALL.md`

## Included Skills

`fiction-core` contains:

- `project-orchestrator`: chooses the next skill, route, and work order
- `continuity-keeper`: checks canon changes, broken links, and consequences
- `writer-assistant`: builds canon, structure, characters, conflicts, and working documents
- `story-analyst`: diagnoses pacing, contradictions, arcs, and story risks
- `project-bootstrap`: creates or aligns the project layout

Optional addons:

- `rfc-adr-assistant`: writes, updates, and reviews engineering RFC/ADR documents
- `obsidian-compat`: maps fiction-first project files into optional Obsidian vault workflows

Detailed skill boundaries:

- `SKILLS.md`

## Repository Layout

```text
codex-story-skills/
  .codex-dev/
    skills/          # source of truth for atomic skills
    bundles/         # internal bundle manifests
    scripts/         # build, validation, and dev tooling
  plugins/           # local generated plugin output, ignored except .gitkeep
  scripts/           # user-facing install entrypoints only
  docs/
  README.md
  INSTALL.md
  SKILLS.md
```

Raw skills are not public install targets. Plugin bundles are generated artifacts built from `.codex-dev/skills/` during release packaging and are not committed with copied skills.

## Development

Build and validate plugins:

```bash
python3 .codex-dev/scripts/build-plugins.py
python3 .codex-dev/scripts/validate-skill-language.py
python3 .codex-dev/scripts/validate-skills.py
python3 .codex-dev/scripts/package-release-assets.py
```

Optional local git hooks:

```bash
.codex-dev/scripts/install-git-hooks.sh
```

Publish an install-ready release by pushing a version tag:

```bash
git tag v0.2.0
git push origin v0.2.0
```

GitHub Actions uploads the plugin zip assets to the release.

The old raw sync flow is retained only as an internal development helper:

```bash
.codex-dev/scripts/sync-to-codex.sh --dry-run
```

Do not document raw sync as the main installation path.

## Docs

- `docs/PLUGIN_FIRST_REFACTOR.md`: migration plan, file moves, build strategy, release asset strategy, install flow, and risks
- `docs/RELEASE.md`: release workflow and asset contract
- `EXAMPLES.md`: first-use prompts
- `TROUBLESHOOTING.md`: installation and routing troubleshooting
- `CONTRIBUTING.md`: source skill and plugin build workflow
- `CHANGELOG.md`: release history

## License

MIT. See `LICENSE`.
