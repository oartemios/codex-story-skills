"""Shared bundle source helpers for the Codex packaging toolchain."""

from __future__ import annotations

from pathlib import Path

from bundle_manifest import load_bundle_manifest


SCRIPTS_ROOT = Path(__file__).resolve().parent
DEV_ROOT = SCRIPTS_ROOT.parent
REPO_ROOT = DEV_ROOT.parent
SRC_ROOT = REPO_ROOT / "src"
SKILLS_ROOT = DEV_ROOT / "skills"
MODULES_ROOT = SRC_ROOT / "modules"
CONTENT_ROOT = SRC_ROOT / "content"
CONTENT_SKILLS_ROOT = CONTENT_ROOT / "skills"
CONTENT_SHARED_ROOT = CONTENT_ROOT / "shared"
PLUGINS_ROOT = REPO_ROOT / "plugins"


def bundle_manifest_paths() -> list[Path]:
    if not MODULES_ROOT.exists():
        return []
    return sorted(MODULES_ROOT.glob("*.yaml"))


def bundle_names() -> list[str]:
    return [path.stem for path in bundle_manifest_paths()]


def load_bundle(name: str) -> dict:
    path = MODULES_ROOT / f"{name}.yaml"
    if not path.exists():
        raise ValueError(f"Bundle manifest not found: {path.relative_to(REPO_ROOT)}")
    return load_bundle_manifest(path)


def skill_source_exists(skill: str) -> bool:
    return (SKILLS_ROOT / skill / "SKILL.md").exists() or (
        CONTENT_SKILLS_ROOT / skill / "skill.yaml"
    ).exists()


def resolve_bundle_skills(name: str, seen: set[str] | None = None) -> tuple[list[str], bool]:
    seen = seen or set()
    if name in seen:
        raise ValueError(f"Bundle include cycle detected at {name}")
    seen.add(name)

    bundle = load_bundle(name)
    skills: list[str] = []
    include_shared = bool(bundle.get("include_shared", False))

    for included in bundle.get("includes", []):
        included_skills, included_shared = resolve_bundle_skills(included, seen.copy())
        include_shared = include_shared or included_shared
        for skill in included_skills:
            if skill not in skills:
                skills.append(skill)

    for skill in bundle.get("skills", []):
        if skill not in skills:
            skills.append(skill)

    return skills, include_shared


def all_skill_names() -> list[str]:
    names = {
        path.name
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".") and path.name != "_shared"
    }
    if CONTENT_SKILLS_ROOT.exists():
        names.update(
            path.name
            for path in CONTENT_SKILLS_ROOT.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
    return sorted(names)
