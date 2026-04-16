#!/usr/bin/env python3
"""Validate that source skill instructions use the project language.

The skills are intentionally Russian-first. English domain terms are allowed,
but English instructional boilerplate should not appear in skill source files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


DEV_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = DEV_ROOT.parent
SKILLS_ROOT = DEV_ROOT / "skills"

ENGLISH_INSTRUCTION_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\buse this skill\b",
        r"\bdo not use this skill\b",
        r"\bdo not trigger\b",
        r"\busually return\b",
        r"\byou help\b",
        r"\byou are\b",
        r"\byour task\b",
        r"\bwhen the user\b",
        r"\bif the user\b",
        r"\bsource of truth\b",
        r"\bkeep canonical decisions\b",
        r"\btreat .+ as optional\b",
        r"\bprefer plain markdown\b",
    )
)

ENGLISH_HEADING_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^##\s+Role\s*$",
        r"^##\s+Rules\s*$",
        r"^##\s+Output\s*$",
        r"^##\s+What this skill does\s*$",
        r"^##\s+What this skill does not do\s*$",
    )
)


def iter_skill_markdown() -> list[Path]:
    return sorted(SKILLS_ROOT.rglob("*.md"))


def validate_file(path: Path, errors: list[str]) -> None:
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for pattern in ENGLISH_HEADING_PATTERNS:
            if pattern.search(line):
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: English heading '{line.strip()}'"
                )
        for pattern in ENGLISH_INSTRUCTION_PATTERNS:
            if pattern.search(line):
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: English instructional phrase '{pattern.pattern}'"
                )


def main() -> int:
    if not SKILLS_ROOT.exists():
        print(".codex-dev/skills directory not found", file=sys.stderr)
        return 1

    errors: list[str] = []
    files = iter_skill_markdown()
    for path in files:
        validate_file(path, errors)

    if errors:
        print("Skill language validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print(
            "\nUse Russian for skill instructions. English domain terms are allowed.",
            file=sys.stderr,
        )
        return 1

    print(f"Skill language validation passed: {len(files)} markdown files checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
