#!/usr/bin/env python3
"""Basic integrity checks for the runtime skills tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"

BACKTICK_MD_RE = re.compile(r"`([^`]+\.md)`")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
KEY_VALUE_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def iter_skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".") and path.name != "_shared"
    )


def resolve_md_reference(source: Path, ref: str) -> Path | None:
    if ref.startswith("skills/"):
        return ROOT / ref
    if ref.startswith("templates/"):
        for parent in source.parents:
            if (parent / "SKILL.md").exists():
                return parent / ref
        return source.parent / ref
    if ref.startswith("../") or ref.startswith("./"):
        return (source.parent / ref).resolve()
    return None


def validate_frontmatter(skill_md: Path, errors: list[str]) -> None:
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"{skill_md}: missing YAML frontmatter")
        return

    frontmatter = match.group(1)
    seen_keys: dict[str, int] = {}

    for lineno, line in enumerate(frontmatter.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        match = KEY_VALUE_RE.match(line)
        if not match:
            continue

        key = match.group(1)
        seen_keys[key] = seen_keys.get(key, 0) + 1
        if seen_keys[key] > 1:
            errors.append(
                f"{skill_md}: duplicate frontmatter key '{key}' (line {lineno})"
            )

    if "name" not in seen_keys:
        errors.append(f"{skill_md}: frontmatter must contain 'name'")
    if "description" not in seen_keys:
        errors.append(f"{skill_md}: frontmatter must contain 'description'")


def validate_markdown_references(md_file: Path, errors: list[str]) -> None:
    text = md_file.read_text(encoding="utf-8")
    for ref in BACKTICK_MD_RE.findall(text):
        resolved = resolve_md_reference(md_file, ref)
        if resolved is None:
            continue
        if not resolved.exists():
            rel = md_file.relative_to(ROOT)
            errors.append(f"{rel}: broken markdown reference '{ref}'")


def main() -> int:
    errors: list[str] = []

    if not SKILLS_ROOT.exists():
        print("skills directory not found", file=sys.stderr)
        return 1

    skill_dirs = iter_skill_dirs()
    if not skill_dirs:
        errors.append("no skill directories found in skills/")

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue
        validate_frontmatter(skill_md, errors)

        references_dir = skill_dir / "references"
        if not references_dir.exists():
            errors.append(f"{skill_dir}: missing references/")

    markdown_files = sorted(SKILLS_ROOT.rglob("*.md"))
    for md_file in markdown_files:
        validate_markdown_references(md_file, errors)

    if errors:
        print("Validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validation passed: {len(skill_dirs)} skills, {len(markdown_files)} markdown files checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
