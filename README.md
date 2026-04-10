# codex-story-skills

Reusable Codex skills for fiction writing, story architecture, diagnostics, and project bootstrap.

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

- `writer-assistant`: editorial and structural support for a fiction project
- `story-analyst`: diagnostics for pacing, contradictions, arcs, and story risks
- `project-bootstrap`: starter structure and migration support for fiction projects

## Scope

These skills are designed for fiction-first workflows and currently assume a recommended project layout based on:

- `canon/`
- `characters/`
- `books/`
- `archive/`
- `inbox/`

That layout is a convention, not a hard requirement. The current version optimizes for projects that already use it or can map their materials onto it with minimal adaptation.

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

Once the repository becomes more generic, more configurable, and better documented, it can be made public.
