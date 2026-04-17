#!/usr/bin/env python3
"""Build installable Codex plugin bundles from internal skill sources."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from bundle_manifest import load_bundle_manifest


REPO_ROOT = Path(__file__).resolve().parents[2]
DEV_ROOT = REPO_ROOT / ".codex-dev"
SRC_ROOT = REPO_ROOT / "src"
SKILLS_ROOT = DEV_ROOT / "skills"
MODULES_ROOT = SRC_ROOT / "modules"
CONTENT_ROOT = SRC_ROOT / "content"
CONTENT_SKILLS_ROOT = CONTENT_ROOT / "skills"
CONTENT_SHARED_ROOT = CONTENT_ROOT / "shared"
PLUGINS_ROOT = REPO_ROOT / "plugins"
VERSION = "1.0.1"

AUTHOR = {
    "name": "Artem Orlov",
    "url": "https://github.com/oartemios",
}


def load_bundle(name: str) -> dict:
    path = MODULES_ROOT / f"{name}.yaml"
    if not path.exists():
        raise ValueError(f"Bundle manifest not found: {path.relative_to(REPO_ROOT)}")
    return load_bundle_manifest(path)


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


def copy_tree(source: Path, dest: Path) -> None:
    if not source.exists():
        raise ValueError(f"Source not found: {source.relative_to(REPO_ROOT)}")
    shutil.copytree(source, dest)


def render_codex_skill(source: Path, dest: Path) -> None:
    metadata = load_bundle_manifest(source / "skill.yaml")
    prompt_path = source / metadata.get("entrypoint", "prompt.md")
    if not prompt_path.exists():
        raise ValueError(f"Skill prompt not found: {prompt_path.relative_to(REPO_ROOT)}")

    skill_name = metadata.get("id")
    description = metadata.get("description_ru")
    if not skill_name or not description:
        raise ValueError(f"{source.relative_to(REPO_ROOT)}: missing id or description_ru")

    dest.mkdir(parents=True)
    skill_md = "\n".join(
        [
            "---",
            f"name: {skill_name}",
            f"description: {description}",
            "---",
            "",
            prompt_path.read_text(encoding="utf-8").rstrip(),
            "",
        ]
    )
    (dest / "SKILL.md").write_text(skill_md, encoding="utf-8")

    rules_dir = source / "rules"
    if rules_dir.exists():
        copy_tree(rules_dir, dest / "references")

    templates_dir = source / "templates"
    if templates_dir.exists():
        copy_tree(templates_dir, dest / "templates")


def copy_skill(skill: str, dest: Path) -> None:
    content_source = CONTENT_SKILLS_ROOT / skill
    legacy_source = SKILLS_ROOT / skill

    if (content_source / "skill.yaml").exists():
        render_codex_skill(content_source, dest)
        return
    if legacy_source.exists():
        copy_tree(legacy_source, dest)
        return
    raise ValueError(f"Skill source not found: {skill}")


def copy_shared(dest: Path) -> None:
    if CONTENT_SHARED_ROOT.exists():
        copy_tree(CONTENT_SHARED_ROOT / "templates", dest / "_shared" / "templates")
        shutil.copy2(CONTENT_SHARED_ROOT / "conventions.md", dest / "CONVENTIONS.md")
        return
    copy_tree(SKILLS_ROOT / "_shared", dest / "_shared")
    shutil.copy2(SKILLS_ROOT / "CONVENTIONS.md", dest / "CONVENTIONS.md")


def plugin_manifest(bundle: dict) -> dict:
    name = bundle["name"]
    display_name = bundle.get("display_name", name)
    description = bundle.get("description", "")
    category = bundle.get("category", "Writing")

    prompts = {
        "fiction-core": [
            "Хочу проработать книгу 1. Что делать сначала?",
            "Собери рабочий канон по этим материалам.",
            "Проверь ритм книги и сюжетные риски.",
        ],
        "engineering-addon": [
            "Оформи ADR по этому решению.",
            "Напиши RFC для этой миграции.",
        ],
        "obsidian-addon": [
            "Помоги сопоставить Obsidian vault с проектной структурой.",
            "Проверь, где vault-навигация расходится с каноном.",
        ],
        "full": [
            "Хочу проработать книгу 1. Что делать сначала?",
            "Оформи ADR по этому решению.",
            "Сопоставь Obsidian vault с проектной структурой.",
        ],
    }

    return {
        "name": name,
        "version": VERSION,
        "description": description,
        "author": AUTHOR,
        "homepage": "https://github.com/oartemios/codex-story-skills",
        "repository": "https://github.com/oartemios/codex-story-skills",
        "license": "MIT",
        "keywords": ["codex", "skills", "fiction", "writing"],
        "skills": "./skills/",
        "interface": {
            "displayName": display_name,
            "shortDescription": description,
            "longDescription": description,
            "developerName": AUTHOR["name"],
            "category": category,
            "capabilities": ["Write"],
            "websiteURL": "https://github.com/oartemios/codex-story-skills",
            "defaultPrompt": prompts.get(name, []),
            "brandColor": "#256A5E",
        },
    }


def write_plugin_readme(plugin_dir: Path, bundle: dict, skills: list[str]) -> None:
    lines = [
        f"# {bundle.get('display_name', bundle['name'])}",
        "",
        bundle.get("description", ""),
        "",
        "## Included Skills",
        "",
    ]
    lines.extend(f"- `{skill}`" for skill in skills)
    lines.extend(
        [
            "",
            "This directory is generated from repository source content.",
            "Do not edit generated plugin artifacts by hand.",
            "",
        ]
    )
    (plugin_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def build_plugin(name: str) -> None:
    bundle = load_bundle(name)
    skills, include_shared = resolve_bundle_skills(name)
    plugin_dir = PLUGINS_ROOT / name
    skills_dir = plugin_dir / "skills"

    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)

    (plugin_dir / ".codex-plugin").mkdir(parents=True)
    skills_dir.mkdir(parents=True)

    if include_shared:
        copy_shared(skills_dir)

    for skill in skills:
        copy_skill(skill, skills_dir / skill)

    manifest = plugin_manifest(bundle)
    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_plugin_readme(plugin_dir, bundle, skills)
    print(f"Built {plugin_dir.relative_to(REPO_ROOT)}")


def bundle_names() -> list[str]:
    return sorted(path.stem for path in MODULES_ROOT.glob("*.yaml"))


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


def build_raw_codex_skills(dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    copy_shared(dest)
    for skill in all_skill_names():
        copy_skill(skill, dest / skill)
    try:
        shown = dest.relative_to(REPO_ROOT)
    except ValueError:
        shown = dest
    print(f"Built {shown}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw-skills-dir",
        help="Build a raw Codex skills tree at this path instead of plugin bundles.",
    )
    parser.add_argument(
        "bundles",
        nargs="*",
        help="Bundle names to build. Defaults to all manifests in src/modules.",
    )
    args = parser.parse_args()

    if args.raw_skills_dir:
        build_raw_codex_skills(Path(args.raw_skills_dir).expanduser().resolve())
        return 0

    names = args.bundles or bundle_names()
    for name in names:
        build_plugin(name)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
