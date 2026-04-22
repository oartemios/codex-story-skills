# Changelog

All notable changes to this project are documented here.

## Unreleased

## v1.0.1 - 2026-04-16

### Changed

- Public README now focuses on product install/use, with internal architecture moved to `docs/ARCHITECTURE.md`.
- Language validator now covers source skills and Russian-first public documentation.

## v1.0.0 - 2026-04-16

### Added

- Plugin-first package layout with `scripts/` as source/build tooling and `plugins/` as generated installable artifacts.
- `fiction-core`, `engineering-addon`, and `obsidian-addon` plugin bundles.
- `rfc-adr-assistant` skill for optional engineering RFC/ADR drafting and review.
- `obsidian-compat` skill for optional Obsidian vault compatibility.
- Release asset packaging script for plugin zip files.
- GitHub Actions release workflow that uploads install-ready plugin zip assets.
- Skill language validator and opt-in local git hooks for pre-commit/pre-push checks.
- `obsidian-addon` remains independent and can be combined with `fiction-core`, `engineering-addon`, or both.
- Installer now supports multiple `--plugin` arguments and named presets such as `obsidian-engineering`.

### Changed

- Renamed the RFC/ADR skill to `rfc-adr-assistant`.
- Moved raw skill sync to `scripts/sync-to-codex.sh` as an internal development helper.
- Replaced public install flow with release-asset download and local marketplace registration.

## v0.1.0 - 2026-04-14

First public baseline release.

### Added

- Runtime package with five fiction-first Codex skills:
  - `project-orchestrator`
  - `continuity-keeper`
  - `writer-assistant`
  - `story-analyst`
  - `project-bootstrap`
- Safe sync workflow for installing the former `skills/` runtime layer into Codex Home.
- Package validation script for skill frontmatter and internal markdown references.
- GitHub Actions CI for validation, shell syntax checks, installer help, dry-run sync, and real sync into a fake Codex Home.
- Public documentation:
  - `README.md`
  - `INSTALL.md`
  - `EXAMPLES.md`
  - `SKILLS.md`
  - `TROUBLESHOOTING.md`
  - `CONTRIBUTING.md`
  - `SECURITY.md`
- MIT license.

### Notes

- The package is intentionally optimized for Russian-language fiction-first workflows.
- The recommended project layout is `canon/`, `characters/`, `books/`, `archive/`, and `inbox/`, but this is a convention rather than a hard requirement.
- `main` remains the active development branch; use the `v0.1.0` tag for the first stable public snapshot.
