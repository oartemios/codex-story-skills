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
- [x] Legacy duplicates in `.codex-dev/skills/obsidian-compat/` and `.codex-dev/skills/rfc-adr-assistant/` are intentionally still present.
- [ ] `fiction-core` is still the main un-migrated source set.

## Done

- [x] Optional pilot migrations are complete for `obsidian-compat` and `rfc-adr-assistant`.
- [x] The agent-neutral manifest layer is in place under `src/modules/`.
- [x] The Codex adapter boundary is explicit in `.codex-dev/scripts/targets/codex.py`.
- [x] This working plan file exists and can be used as the session handoff context.

## In Progress

- [ ] No source migration is being edited in this session; the next implementation pass should start with `fiction-core`.
- [ ] Keep the legacy duplicate skills untouched until the remaining migration steps are stable.

## Remaining

- [ ] Complete packaging migration after the optional pilots by applying the same source split to `fiction-core`.
- [ ] Migrate `fiction-core` into `src/content/skills/fiction-core/` and align its manifests with the agent-neutral model.
- [ ] Verify byte-compatible Codex output for migrated content and `fiction-core` before any fallback cleanup.
- [ ] Keep the CLI surface unchanged while validating generated artifacts and release packaging.
- [ ] Synchronize docs that still describe the old layout, including packaging, architecture, install, and release references.
- [ ] Remove legacy duplicates in the safe order only after parity and release flow stability are proven.
- [ ] Decide whether any final target adapter split is still needed after `fiction-core` lands.

## Risks / Dependencies

- [ ] Protect byte parity by comparing generated Codex output against the current baseline before removing any legacy fallback.
- [ ] Keep `.codex-dev/skills/obsidian-compat/` and `.codex-dev/skills/rfc-adr-assistant/` in place until all docs, smoke tests, and release paths stop referencing them.
- [ ] Treat the final adapter split as conditional; do not create extra abstraction if `.codex-dev/scripts/targets/codex.py` remains the only Codex-specific surface.
- [ ] Avoid any build or CLI behavior change until the migration plan explicitly marks parity as stable.

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
- [ ] 10-30 min: sweep one documentation surface for stale paths once the migrated slice stays clean.
- [ ] 10-30 min: reassess whether a separate target adapter is still needed after the `fiction-core` pass.

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
