#!/usr/bin/env python3
"""Validate Russian-first language conventions for skills and public docs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEV_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = DEV_ROOT.parent
CONTENT_ROOT = REPO_ROOT / "src" / "content"

PUBLIC_DOCS = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "INSTALL.md",
    REPO_ROOT / "SKILLS.md",
    REPO_ROOT / "EXAMPLES.md",
    REPO_ROOT / "TROUBLESHOOTING.md",
    REPO_ROOT / "docs" / "ARCHITECTURE.md",
    REPO_ROOT / "docs" / "PACKAGING.md",
    REPO_ROOT / "docs" / "SMOKE_TESTS.md",
)

CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
WORD_RE = re.compile(r"[A-Za-z]{3,}")

ALLOWED_ENGLISH_TERMS = {
    "ADR",
    "API",
    "BOUNDARY",
    "BOOT",
    "CHANGELOG",
    "CI",
    "CONT",
    "CONTRIBUTING",
    "Codex",
    "DEV",
    "GitHub",
    "HTTP",
    "INSTALL",
    "JSON",
    "MIT",
    "ORCH",
    "README",
    "REST",
    "RFC",
    "SECURITY",
    "SKILLS",
    "URL",
    "WRIT",
    "YAML",
    "addons",
    "archive",
    "asset",
    "assets",
    "assistant",
    "backlinks",
    "bootstrap",
    "branch",
    "bundle",
    "bundles",
    "canon",
    "characters",
    "commit",
    "core",
    "design",
    "dev",
    "docs",
    "engineering",
    "fiction",
    "full",
    "hooks",
    "inbox",
    "latest",
    "main",
    "manifest",
    "marketplace",
    "metadata",
    "obsidian",
    "package",
    "plugin",
    "plugins",
    "preset",
    "presets",
    "push",
    "release",
    "routing",
    "skills",
    "source",
    "sync",
    "tag",
    "tags",
    "vault",
    "wikilinks",
    "workflow",
    "zip",
}

ENGLISH_INSTRUCTION_PATTERNS = tuple(
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

ENGLISH_PUBLIC_DOC_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\bthe installer\b",
        r"\bthe plugin\b",
        r"\bthis project\b",
        r"\bthis package\b",
        r"\bcheck the\b",
        r"\bconfirm that\b",
        r"\bbefore tagging\b",
        r"\bafter installation\b",
        r"\bdo not commit\b",
        r"\bdo not rename\b",
        r"\bmore details\b",
        r"\bvalid plugin names\b",
    )
)

ENGLISH_HEADING_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"^#+\s+Role\s*$",
        r"^#+\s+Rules\s*$",
        r"^#+\s+Output\s*$",
        r"^#+\s+What this skill does\s*$",
        r"^#+\s+What this skill does not do\s*$",
        r"^#+\s+Troubleshooting\s*$",
        r"^#+\s+Examples\s*$",
        r"^#+\s+What The Installer Does\s*$",
        r"^#+\s+Release Asset Not Found\s*$",
        r"^#+\s+Marketplace Entry Is Missing\s*$",
        r"^#+\s+Codex Does Not Show The Plugin\s*$",
        r"^#+\s+Wrong Skill Routes\s*$",
        r"^#+\s+Development Build Looks Stale\s*$",
    )
)


def iter_skill_markdown() -> list[Path]:
    if not CONTENT_ROOT.exists():
        return []
    return sorted(CONTENT_ROOT.rglob("*.md"))


def iter_public_docs() -> list[Path]:
    return [path for path in PUBLIC_DOCS if path.exists()]


def is_code_fence(line: str) -> bool:
    return line.strip().startswith("```")


def english_words(line: str) -> list[str]:
    return WORD_RE.findall(line)


def non_allowed_english_words(line: str) -> list[str]:
    return [
        word
        for word in english_words(line)
        if word not in ALLOWED_ENGLISH_TERMS and word.lower() not in ALLOWED_ENGLISH_TERMS
    ]


def validate_patterns(
    path: Path,
    line: str,
    lineno: int,
    patterns: tuple[re.Pattern[str], ...],
    errors: list[str],
    label: str,
) -> None:
    for pattern in patterns:
        if pattern.search(line):
            errors.append(
                f"{path.relative_to(REPO_ROOT)}:{lineno}: {label} '{pattern.pattern}'"
            )


def validate_skill_file(path: Path, errors: list[str]) -> None:
    in_code = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if is_code_fence(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        validate_patterns(
            path,
            line,
            lineno,
            ENGLISH_HEADING_PATTERNS,
            errors,
            "English heading",
        )
        validate_patterns(
            path,
            line,
            lineno,
            ENGLISH_INSTRUCTION_PATTERNS,
            errors,
            "English instructional phrase",
        )


def validate_public_doc(path: Path, errors: list[str]) -> None:
    in_code = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if is_code_fence(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        validate_patterns(
            path,
            line,
            lineno,
            ENGLISH_HEADING_PATTERNS,
            errors,
            "English public heading",
        )
        validate_patterns(
            path,
            line,
            lineno,
            ENGLISH_PUBLIC_DOC_PATTERNS,
            errors,
            "English public-doc phrase",
        )

        stripped = line.strip()
        if not stripped or CYRILLIC_RE.search(stripped):
            continue
        if stripped.startswith(("http://", "https://", "```")):
            continue
        if stripped.startswith(("#", "-", "*")):
            words = non_allowed_english_words(stripped)
            if len(words) >= 3:
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno}: English-only public doc line '{stripped}'"
                )


def validate_scope(scope: str) -> tuple[int, list[str]]:
    errors: list[str] = []
    files: list[Path] = []

    if scope in ("skills", "all"):
        skill_files = iter_skill_markdown()
        if not skill_files:
            return 0, ["src/content/skills directory not found"]
        files.extend(skill_files)
        for path in skill_files:
            validate_skill_file(path, errors)

    if scope in ("public-docs", "all"):
        public_files = iter_public_docs()
        files.extend(public_files)
        for path in public_files:
            validate_public_doc(path, errors)

    return len(files), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=("skills", "public-docs", "all"),
        default="all",
        help="Files to validate. Default: all.",
    )
    args = parser.parse_args()

    checked, errors = validate_scope(args.scope)
    if errors:
        print("Language validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print(
            "\nUse Russian for instructions and public docs. English domain terms are allowed.",
            file=sys.stderr,
        )
        return 1

    print(f"Language validation passed: {checked} markdown files checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
