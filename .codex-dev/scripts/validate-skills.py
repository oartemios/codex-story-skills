#!/usr/bin/env python3
"""Basic integrity checks for the internal skill source and built plugins."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from bundle_manifest import load_bundle_manifest


DEV_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = DEV_ROOT.parent
SKILLS_ROOT = DEV_ROOT / "skills"
BUNDLES_ROOT = DEV_ROOT / "bundles"
PLUGINS_ROOT = REPO_ROOT / "plugins"

BACKTICK_MD_RE = re.compile(r"`([^`]+\.md)`")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
KEY_VALUE_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")

TOP_LEVEL_DOCS = (
    "README.md",
    "INSTALL.md",
    "EXAMPLES.md",
    "SKILLS.md",
    "TROUBLESHOOTING.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
)

TOP_LEVEL_REFERENCE_DOCS = TOP_LEVEL_DOCS + ("ROADMAP.md",)


def iter_skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".") and path.name != "_shared"
    )


def resolve_md_reference(source: Path, ref: str) -> Path | None:
    if source.parent == REPO_ROOT and "/" not in ref and ref in TOP_LEVEL_REFERENCE_DOCS:
        return REPO_ROOT / ref
    if ref.startswith("skills/"):
        if PLUGINS_ROOT in source.parents:
            for parent in source.parents:
                if parent.parent == PLUGINS_ROOT:
                    return parent / ref
        return DEV_ROOT / ref
    if ref.startswith("templates/"):
        for parent in source.parents:
            if (parent / "SKILL.md").exists():
                return parent / ref
        return source.parent / ref
    if ref.startswith("../") or ref.startswith("./"):
        return (source.parent / ref).resolve()
    return None


def normalize_markdown_link_target(target: str) -> str | None:
    target = target.strip()
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return None

    target = target.split("#", 1)[0]
    if not target:
        return None
    return target


def resolve_markdown_link(source: Path, target: str) -> Path | None:
    target = normalize_markdown_link_target(target)
    if target is None:
        return None
    if target.startswith("/"):
        return REPO_ROOT / target.lstrip("/")
    return (source.parent / target).resolve()


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
            rel = md_file.relative_to(REPO_ROOT)
            errors.append(f"{rel}: broken markdown reference '{ref}'")

    if md_file.parent == REPO_ROOT:
        for target in MARKDOWN_LINK_RE.findall(text):
            resolved = resolve_markdown_link(md_file, target)
            if resolved is None:
                continue
            if not resolved.exists():
                rel = md_file.relative_to(REPO_ROOT)
                errors.append(f"{rel}: broken markdown link '{target}'")


def validate_bundle_manifests(errors: list[str]) -> None:
    if not BUNDLES_ROOT.exists():
        errors.append(".codex-dev/bundles: missing bundle manifests directory")
        return

    manifests = sorted(BUNDLES_ROOT.glob("*.yaml"))
    if not manifests:
        errors.append(".codex-dev/bundles: no bundle manifests found")
        return

    bundle_names = {path.stem for path in manifests}
    for manifest in manifests:
        data = yaml_load(manifest, errors)
        if data is None:
            continue
        for field in ("name", "description"):
            if not data.get(field):
                errors.append(f"{manifest.relative_to(REPO_ROOT)}: missing '{field}'")
        if data.get("name") != manifest.stem:
            errors.append(
                f"{manifest.relative_to(REPO_ROOT)}: name must match file stem"
            )
        for skill in data.get("skills", []):
            if not (SKILLS_ROOT / skill / "SKILL.md").exists():
                errors.append(
                    f"{manifest.relative_to(REPO_ROOT)}: unknown skill '{skill}'"
                )
        for included in data.get("includes", []):
            if included not in bundle_names:
                errors.append(
                    f"{manifest.relative_to(REPO_ROOT)}: unknown included bundle '{included}'"
                )


def yaml_load(path: Path, errors: list[str]) -> dict | None:
    try:
        data = load_bundle_manifest(path)
    except Exception as exc:  # noqa: BLE001 - validator should report any parse issue.
        errors.append(f"{path.relative_to(REPO_ROOT)}: invalid YAML: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(REPO_ROOT)}: expected YAML object")
        return None
    return data


def json_load(path: Path, errors: list[str]) -> dict | None:
    try:
        import json

        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validator should report any parse issue.
        errors.append(f"{path.relative_to(REPO_ROOT)}: invalid JSON: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(REPO_ROOT)}: expected JSON object")
        return None
    return data


def validate_built_plugins(errors: list[str]) -> None:
    if not PLUGINS_ROOT.exists():
        return

    plugin_dirs = sorted(path for path in PLUGINS_ROOT.iterdir() if path.is_dir())
    if not plugin_dirs:
        return

    for plugin_dir in plugin_dirs:
        manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
        if not manifest_path.exists():
            errors.append(f"{plugin_dir.relative_to(REPO_ROOT)}: missing plugin.json")
            continue
        manifest = json_load(manifest_path, errors)
        if manifest is None:
            continue
        if manifest.get("name") != plugin_dir.name:
            errors.append(
                f"{manifest_path.relative_to(REPO_ROOT)}: name must match plugin directory"
            )
        if manifest.get("skills") != "./skills/":
            errors.append(
                f"{manifest_path.relative_to(REPO_ROOT)}: skills must be './skills/'"
            )
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists():
            errors.append(f"{plugin_dir.relative_to(REPO_ROOT)}: missing skills/")
            continue
        for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
            if skill_dir.name == "_shared":
                continue
            if not (skill_dir / "SKILL.md").exists():
                errors.append(
                    f"{skill_dir.relative_to(REPO_ROOT)}: missing SKILL.md"
                )


def main() -> int:
    errors: list[str] = []

    if not SKILLS_ROOT.exists():
        print(".codex-dev/skills directory not found", file=sys.stderr)
        return 1

    skill_dirs = iter_skill_dirs()
    if not skill_dirs:
        errors.append("no skill directories found in .codex-dev/skills/")

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
    if PLUGINS_ROOT.exists():
        markdown_files.extend(sorted(PLUGINS_ROOT.rglob("*.md")))
    top_level_docs = [REPO_ROOT / doc for doc in TOP_LEVEL_DOCS]
    for doc in top_level_docs:
        if not doc.exists():
            errors.append(f"{doc.relative_to(REPO_ROOT)}: missing top-level doc")

    markdown_files.extend(doc for doc in top_level_docs if doc.exists())
    for md_file in markdown_files:
        validate_markdown_references(md_file, errors)
    validate_bundle_manifests(errors)
    validate_built_plugins(errors)

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
