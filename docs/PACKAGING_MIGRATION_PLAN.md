# Packaging Migration Plan

Last updated: 2026-04-17

This is the live working checklist for the multi-agent packaging migration.
Update it in place as work lands. Do not rewrite history; only tick items, add short notes, and keep the next short session obvious.

## Purpose

- [x] Keep one short-session checklist for the remaining packaging migration work.
- [x] Make it possible for a new agent to understand what is already done, what is still open, and what must stay stable.

## Current State

- [x] `obsidian-compat` is already migrated and lives under `src/content/skills/obsidian-compat/`.
- [x] `rfc-adr-assistant` is already migrated and lives under `src/content/skills/rfc-adr-assistant/`.
- [x] `src/content/*` and `src/modules/*.yaml` already act as the agent-neutral source layer.
- [x] Codex-specific generation is already isolated in `.codex-dev/scripts/targets/codex.py`.
- [x] CLI behavior and byte-compatible Codex output remain the compatibility bar.
- [x] The last legacy duplicate source tree (`rfc-adr-assistant`) has been retired; `obsidian-compat` now lives only under `src/content/skills/`.

## Done

- [x] Optional pilot migrations are complete for `obsidian-compat` and `rfc-adr-assistant`.
- [x] The agent-neutral manifest layer is in place under `src/modules/`.
- [x] The Codex adapter boundary is explicit in `.codex-dev/scripts/targets/codex.py`.
- [x] This working plan file exists and can be used as the session handoff context.
- [x] Shared source conventions are documented in `src/content/shared/conventions.md`.
- note: the shared layer now reflects the current `skill.yaml` + `prompt.md` + `rules/` + `templates/` model.
- [x] The `fiction-core` bundle source is fully migrated across its included skills.
- note: the bundle resolves to migrated skills under `src/content/skills/` and builds successfully through `python3 .codex-dev/scripts/build-plugins.py fiction-core`.
- [x] The bundle no longer needs a monolithic `src/content/skills/fiction-core/` source directory.
- note: the bundle is composed of per-skill canonical sources plus `src/modules/fiction-core.yaml`.
- [x] Byte-compatible Codex output was verified against legacy source for all bundled `fiction-core` skills.
- note: `diff -ru .codex-dev/skills/<skill> plugins/fiction-core/skills/<skill>` returned no differences for `project-orchestrator`, `continuity-keeper`, `writer-assistant`, `story-analyst`, and `project-bootstrap`.
- [x] No final target adapter split is needed for the current migration scope.
- note: `.codex-dev/scripts/targets/codex.py` remains the only Codex-specific adapter boundary, so no extra abstraction was introduced.

## In Progress

- [x] No source migration is being edited in this session; the cleanup pass covered docs, CLI parity, and adapter cleanup.
- note: `python3 .codex-dev/scripts/build-plugins.py`, `python3 .codex-dev/scripts/validate-language.py --scope all`, `python3 .codex-dev/scripts/validate-skills.py`, and `python3 .codex-dev/scripts/package-release-assets.py` all passed after the cleanup.
- [x] Keep the migrated source trees untouched while the cleanup pass settles.
- note: `src/content/skills/rfc-adr-assistant/` stayed canonical; the empty legacy `.codex-dev/skills/rfc-adr-assistant/` tree was removed instead of being repopulated.

## Remaining

- [x] Keep the CLI surface unchanged while validating generated artifacts and release packaging.
- note: `python3 .codex-dev/scripts/build-plugins.py` and `python3 .codex-dev/scripts/package-release-assets.py` succeed for the current bundle set.
- [x] Synchronize docs that still describe the old layout, including packaging, architecture, install, and release references.
- note: `CONTRIBUTING.md`, `TROUBLESHOOTING.md`, `docs/RELEASE.md`, `docs/ARCHITECTURE.md`, `docs/PACKAGING.md`, and `docs/PLUGIN_FIRST_REFACTOR.md` now describe the current hybrid layout; the remaining historical references are intentional context.
- [x] Remove legacy duplicates in the safe order only after parity and release flow stability are proven.
- note: the last legacy duplicate tree has been retired after parity and release packaging checks passed.

## Risks / Dependencies

- [x] Protect byte parity by comparing generated Codex output against the current baseline before removing any legacy fallback.
- note: `python3 .codex-dev/scripts/build-plugins.py fiction-core` succeeded, and `diff -ru` against `.codex-dev/skills/` stayed clean for `project-bootstrap`, `project-orchestrator`, `writer-assistant`, `continuity-keeper`, and `story-analyst`.
- note: normalizing `prompt.md` / `rules` path references changes generated `SKILL.md`, so keep legacy-style references until the parity policy is explicitly relaxed.
- note: the source docs now describe the shared layer separately from the legacy Codex-shaped output layer.
- [x] Treat the final adapter split as conditional; do not create extra abstraction if `.codex-dev/scripts/targets/codex.py` remains the only Codex-specific surface.
- note: `.codex-dev/scripts/targets/codex.py` is still the only Codex-specific adapter surface, so no extra split is needed for the current scope.
- [x] Avoid any build or CLI behavior change until the migration plan explicitly marks parity as stable.
- note: the current packaging flow remains build-compatible and the plan still treats byte parity as the gating condition.

## Short Session Steps

- [x] 10-30 min: inspect `fiction-core` source inventory and map the exact move into `src/content/skills/fiction-core/`.
- note: `project-bootstrap` is now canonical under `src/content/skills/project-bootstrap/` and the bundle builds through the existing Codex path.
- [x] 10-30 min: migrate one small `fiction-core` slice, then run the existing Codex generation path for that slice.
- note: `project-bootstrap` now builds through `python3 .codex-dev/scripts/build-plugins.py fiction-core`.
- [x] 10-30 min: verify byte-compatible output for that slice and record the result in this file.
- note: `diff -u .codex-dev/skills/project-bootstrap/SKILL.md plugins/fiction-core/skills/project-bootstrap/SKILL.md` returned no differences.
- note: `continuity-keeper` is now canonical under `src/content/skills/continuity-keeper/`, `python3 .codex-dev/scripts/build-plugins.py fiction-core` succeeds, and the generated `SKILL.md` matches legacy byte-for-byte.
- note: `writer-assistant` is now canonical under `src/content/skills/writer-assistant/`, `python3 .codex-dev/scripts/build-plugins.py fiction-core` succeeds, and the generated `SKILL.md` matches legacy byte-for-byte.
- note: `story-analyst` is now canonical under `src/content/skills/story-analyst/`, `python3 .codex-dev/scripts/build-plugins.py fiction-core` succeeds, and the generated `SKILL.md` matches legacy byte-for-byte.
- note: `project-orchestrator` is now canonical under `src/content/skills/project-orchestrator/`, `python3 .codex-dev/scripts/build-plugins.py fiction-core` succeeds, and the generated `SKILL.md` matches legacy byte-for-byte.
- [x] 10-30 min: sweep one documentation surface for stale paths once the migrated slice stays clean.
- note: `CONTRIBUTING.md` now reflects migrated skills in `src/content/skills/<skill>/` and keeps legacy `references/` only for unmigrated content.
- note: `docs/RELEASE.md`, `docs/ARCHITECTURE.md`, and `TROUBLESHOOTING.md` now describe the hybrid source layer instead of treating `.codex-dev/skills/` as the only source.
- note: `docs/PLUGIN_FIRST_REFACTOR.md` now reflects the current hybrid source layer instead of the earlier plugin-first-only snapshot.
- [x] 10-30 min: reassess whether a separate target adapter is still needed after the `fiction-core` pass.
- note: the current Codex adapter boundary is sufficient; no new target adapter was introduced.
- [x] 10-30 min: rerun the Codex build and parity check after the latest source-layer edits.
- note: the current source layer still matches the legacy baseline byte-for-byte for the bundled fiction-core skills.

### Fiction-core Inventory Map

- `fiction-core` is a bundle, not a single legacy directory.
- Canonical source layer for the bundle should land in `src/content/skills/<skill>/` entries, while the bundle manifest stays in `src/modules/fiction-core.yaml`.
- Shared content already lives in `src/content/shared/` and stays shared; it is not part of the `fiction-core` move.
- Exact source inventory for the bundle:
  - `project-orchestrator`: `SKILL.md`, `references/{ROUTING_RULES,RUNTIME_RULES,SCENARIO_RULES,TRIGGER_RULES,WORKFLOW_RULES}.md`, `templates/{next-step-template,orchestration-plan}.md`
  - `continuity-keeper`: `SKILL.md`, `references/{CHANGE_RULES,DEPENDENCY_RULES,TRIGGER_RULES}.md`, `templates/continuity-report-template.md`
  - `writer-assistant`: `SKILL.md`, `references/{ARCHIVE_RULES,CANON_RULES,CHARACTER_RULES,CONFLICT_RULES,SCENE_RULES,STARTER_RULES,STRUCTURE_RULES,SYSTEM_RULES,TRIGGER_RULES}.md`, `templates/{act-breakdown-template,chapter-map-template,character-template,conflict-matrix-template,current-canon-template,outline-template,scene-plan-template,system-template}.md`
  - `story-analyst`: `SKILL.md`, `references/{ANALYSIS_RULES,ARC_RULES,CONSISTENCY_RULES,PACING_RULES,TRIGGER_RULES}.md`, `templates/{arc-review-template,contradiction-report-template,pacing-review-template,story-diagnostics-template}.md`
  - `project-bootstrap`: `SKILL.md`, `references/{LAYOUT_RULES,MIGRATION_RULES,STARTER_RULES,TRIGGER_RULES}.md`, `templates/{migration-plan-template,starter-pack-template}.md`
- Move rule for each skill: split `SKILL.md` into `skill.yaml` + `prompt.md`, rename `references/` to `rules/`, and keep `templates/` as-is under the canonical skill directory.

## Update Rules

- [ ] When a step lands, tick the checkbox and add a one-line note instead of rewriting earlier entries.
- [ ] If a step regresses, add a short note under the relevant section so the next session sees the issue immediately.
- [ ] Keep this file focused on migration state, not on implementation details that belong in code or commit messages.
