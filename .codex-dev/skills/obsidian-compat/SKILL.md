---
name: obsidian-compat
description: Optional compatibility skill for mapping fiction-first project files into an Obsidian vault without making Obsidian the canonical source of truth.
---

# SKILL.md

## Role

You help adapt the fiction-first project layout to an Obsidian vault.

Use this skill when the user wants to:

- keep notes in Obsidian while preserving the project canon structure
- map vault folders to `canon/`, `characters/`, `books/`, `archive/`, and `inbox/`
- decide which Obsidian links, tags, or metadata are convenience navigation rather than canon
- migrate loose vault notes into the working project layout

Do not use this skill to make Obsidian required. The canonical project state remains the file-based fiction workflow unless the user explicitly chooses another source of truth.

## Rules

- Treat Obsidian compatibility as optional.
- Keep canonical decisions in project files, not only in backlinks or graph structure.
- Do not require plugins, dataview fields, or vault-specific conventions unless the user already uses them.
- Prefer plain Markdown links and folders over Obsidian-only behavior.
- If a vault has existing conventions, map them instead of replacing them.

## Output

Usually return one of:

- vault-to-project mapping
- migration notes
- folder and note naming recommendations
- risks where vault navigation could diverge from canon
