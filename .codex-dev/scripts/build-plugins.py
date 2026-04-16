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
SKILLS_ROOT = DEV_ROOT / "skills"
BUNDLES_ROOT = DEV_ROOT / "bundles"
PLUGINS_ROOT = REPO_ROOT / "plugins"
VERSION = "0.1.0"

AUTHOR = {
    "name": "Artem Orlov",
    "url": "https://github.com/oartemios",
}


def load_bundle(name: str) -> dict:
    path = BUNDLES_ROOT / f"{name}.yaml"
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
            "This directory is generated from `.codex-dev/skills/`.",
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
        copy_tree(SKILLS_ROOT / "_shared", skills_dir / "_shared")
        shutil.copy2(SKILLS_ROOT / "CONVENTIONS.md", skills_dir / "CONVENTIONS.md")

    for skill in skills:
        copy_tree(SKILLS_ROOT / skill, skills_dir / skill)

    manifest = plugin_manifest(bundle)
    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_plugin_readme(plugin_dir, bundle, skills)
    print(f"Built {plugin_dir.relative_to(REPO_ROOT)}")


def bundle_names() -> list[str]:
    return sorted(path.stem for path in BUNDLES_ROOT.glob("*.yaml"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "bundles",
        nargs="*",
        help="Bundle names to build. Defaults to all manifests in .codex-dev/bundles.",
    )
    args = parser.parse_args()

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
