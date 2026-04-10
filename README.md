# codex-story-skills

Reusable Codex skills for writing, story architecture, diagnostics, and project bootstrap.

## Repository Layout

```text
codex-story-skills/
  skills/
    CONVENTIONS.md
    _shared/
    writer-assistant/
    story-analyst/
    project-bootstrap/
```

The `skills/` directory is preserved as-is so internal references like `skills/CONVENTIONS.md` and `skills/_shared/...` continue to work.

## Current Skills

- `writer-assistant`: editorial and structural support for a writing project
- `story-analyst`: diagnostics for pacing, contradictions, arcs, and story risks
- `project-bootstrap`: starter structure and migration support for writing projects

## Local Installation

Copy the repository's `skills/` contents into `~/.codex/skills`.

```bash
rsync -a ~/dev/AI/codex-story-skills/skills/ ~/.codex/skills/
```

If an old symlink exists, remove it first and then sync again.

```bash
rm ~/.codex/skills/writer-assistant
rsync -a ~/dev/AI/codex-story-skills/skills/ ~/.codex/skills/
```

After installation, restart Codex so it reloads available skills.

## Publishing Strategy

Recommended initial visibility: private.

Reasons:
- the skills are still tuned to a specific writing workflow
- structure and naming may still change
- private iteration is simpler before generalizing for wider reuse

Once the repository becomes more generic and documented, it can be made public.
