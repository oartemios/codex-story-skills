# Changelog

All notable changes to this project are documented here.

## v0.1.0 - 2026-04-14

First public baseline release.

### Added

- Runtime package with five fiction-first Codex skills:
  - `project-orchestrator`
  - `continuity-keeper`
  - `writer-assistant`
  - `story-analyst`
  - `project-bootstrap`
- Safe sync workflow for installing the `skills/` runtime layer into Codex Home.
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
