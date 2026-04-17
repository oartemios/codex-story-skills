#!/usr/bin/env python3
"""Basic integrity checks for the internal skill source and built plugins."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from bundle_sources import (
    CONTENT_ROOT,
    CONTENT_SHARED_ROOT,
    CONTENT_SKILLS_ROOT,
    MODULES_ROOT,
    PLUGINS_ROOT,
    REPO_ROOT,
    bundle_manifest_paths,
    bundle_names,
    skill_source_exists,
)
from bundle_manifest import load_bundle_manifest


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
    if not CONTENT_SKILLS_ROOT.exists():
        return []
    return sorted(
        path
        for path in CONTENT_SKILLS_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )


def resolve_md_reference(source: Path, ref: str) -> Path | None:
    if source.parent == REPO_ROOT and "/" not in ref and ref in TOP_LEVEL_REFERENCE_DOCS:
        return REPO_ROOT / ref
    if ref.startswith("skills/"):
        if ref == "skills/CONVENTIONS.md":
            content_ref = CONTENT_SHARED_ROOT / "conventions.md"
        elif ref.startswith("skills/_shared/"):
            content_ref = CONTENT_SHARED_ROOT / ref.removeprefix("skills/_shared/")
        else:
            content_ref = CONTENT_ROOT / ref.removeprefix("skills/")
        if content_ref.exists():
            return content_ref
        return None
    if ref.startswith("templates/"):
        if CONTENT_SKILLS_ROOT in source.parents:
            for parent in source.parents:
                if parent.parent == CONTENT_SKILLS_ROOT:
                    return parent / ref
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


def validate_content_skill(skill_dir: Path, errors: list[str]) -> None:
    manifest_path = skill_dir / "skill.yaml"
    if not manifest_path.exists():
        errors.append(f"{skill_dir.relative_to(REPO_ROOT)}: missing skill.yaml")
        return

    data = yaml_load(manifest_path, errors)
    if data is None:
        return
    if data.get("id") != skill_dir.name:
        errors.append(
            f"{manifest_path.relative_to(REPO_ROOT)}: id must match skill directory"
        )
    for field in ("kind", "description_ru", "entrypoint"):
        if not data.get(field):
            errors.append(f"{manifest_path.relative_to(REPO_ROOT)}: missing '{field}'")
    if data.get("kind") and data.get("kind") != "skill":
        errors.append(f"{manifest_path.relative_to(REPO_ROOT)}: kind must be 'skill'")

    entrypoint = data.get("entrypoint")
    if isinstance(entrypoint, str):
        validate_content_manifest_path(
            manifest_path,
            skill_dir,
            entrypoint,
            "entrypoint",
            errors,
            expected_prefix=None,
        )
    elif entrypoint is not None:
        errors.append(f"{manifest_path.relative_to(REPO_ROOT)}: entrypoint must be a string")

    validate_content_manifest_file_list(
        manifest_path,
        skill_dir,
        data,
        "rules",
        errors,
        required=True,
        expected_prefix="rules/",
    )
    validate_content_manifest_file_list(
        manifest_path,
        skill_dir,
        data,
        "templates",
        errors,
        required=False,
        expected_prefix="templates/",
    )
    validate_content_manifest_file_list(
        manifest_path,
        CONTENT_ROOT,
        data,
        "shared",
        errors,
        required=False,
        expected_prefix="shared/",
    )

    rules_dir = skill_dir / "rules"
    if not rules_dir.exists():
        errors.append(f"{skill_dir.relative_to(REPO_ROOT)}: missing rules/")


def validate_content_manifest_path(
    manifest_path: Path,
    base_dir: Path,
    value: str,
    field: str,
    errors: list[str],
    expected_prefix: str | None,
) -> None:
    rel_manifest = manifest_path.relative_to(REPO_ROOT)
    if not value:
        errors.append(f"{rel_manifest}: {field} contains an empty path")
        return
    if value.startswith("/"):
        errors.append(f"{rel_manifest}: {field} path must be relative: '{value}'")
        return
    path = Path(value)
    if ".." in path.parts:
        errors.append(f"{rel_manifest}: {field} path must not traverse upward: '{value}'")
        return
    if expected_prefix is not None and not value.startswith(expected_prefix):
        errors.append(
            f"{rel_manifest}: {field} path must start with '{expected_prefix}': '{value}'"
        )
        return
    resolved = base_dir / path
    if not resolved.exists():
        errors.append(f"{rel_manifest}: {field} path not found: '{value}'")
        return
    if not resolved.is_file():
        errors.append(f"{rel_manifest}: {field} path is not a file: '{value}'")


def validate_content_manifest_file_list(
    manifest_path: Path,
    base_dir: Path,
    data: dict,
    field: str,
    errors: list[str],
    required: bool,
    expected_prefix: str,
) -> None:
    rel_manifest = manifest_path.relative_to(REPO_ROOT)
    if field not in data:
        if required:
            errors.append(f"{rel_manifest}: missing '{field}'")
        return

    values = data.get(field)
    if not isinstance(values, list):
        errors.append(f"{rel_manifest}: '{field}' must be a list")
        return
    if required and not values:
        errors.append(f"{rel_manifest}: '{field}' must not be empty")
        return

    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            errors.append(f"{rel_manifest}: '{field}' entries must be strings")
            continue
        if value in seen:
            errors.append(f"{rel_manifest}: duplicate '{field}' entry '{value}'")
            continue
        seen.add(value)
        validate_content_manifest_path(
            manifest_path,
            base_dir,
            value,
            field,
            errors,
            expected_prefix=expected_prefix,
        )


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
    if not MODULES_ROOT.exists():
        errors.append("src/modules: missing module manifests directory")
        return

    manifests = bundle_manifest_paths()
    if not manifests:
        errors.append("src/modules: no module manifests found")
        return

    bundle_names_set = set(bundle_names())
    bundle_data: dict[str, dict] = {}
    for manifest in manifests:
        data = yaml_load(manifest, errors)
        if data is None:
            continue
        bundle_data[manifest.stem] = data
        for field in ("name", "description"):
            if not data.get(field):
                errors.append(f"{manifest.relative_to(REPO_ROOT)}: missing '{field}'")
        if data.get("name") != manifest.stem:
            errors.append(
                f"{manifest.relative_to(REPO_ROOT)}: name must match file stem"
            )

        skills = validate_bundle_list_field(manifest, data, "skills", errors)
        includes = validate_bundle_list_field(manifest, data, "includes", errors)

        for skill in skills:
            if not skill_source_exists(skill):
                errors.append(
                    f"{manifest.relative_to(REPO_ROOT)}: unknown skill '{skill}'"
                )

        for included in includes:
            if included not in bundle_names_set:
                errors.append(
                    f"{manifest.relative_to(REPO_ROOT)}: unknown included bundle '{included}'"
                )

    validate_bundle_include_cycles(manifests, bundle_data, errors)


def validate_bundle_list_field(
    manifest_path: Path,
    data: dict,
    field: str,
    errors: list[str],
) -> list[str]:
    rel_manifest = manifest_path.relative_to(REPO_ROOT)
    value = data.get(field)
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append(f"{rel_manifest}: '{field}' must be a list")
        return []

    items: list[str] = []
    seen: dict[str, int] = {}
    for index, item in enumerate(value, start=1):
        if not isinstance(item, str):
            errors.append(f"{rel_manifest}: '{field}' item #{index} must be a string")
            continue
        if not item:
            errors.append(f"{rel_manifest}: '{field}' item #{index} must not be empty")
            continue
        if item in seen:
            errors.append(
                f"{rel_manifest}: duplicate '{field}' entry '{item}' "
                f"(items {seen[item]} and {index})"
            )
        else:
            seen[item] = index
        items.append(item)
    return items


def validate_bundle_include_cycles(
    manifests: list[Path],
    bundle_data: dict[str, dict],
    errors: list[str],
) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()
    reported: set[tuple[str, ...]] = set()

    def report_cycle(path: list[str]) -> None:
        cycle = path[path.index(path[-1]) :]
        signature = tuple(cycle)
        if signature in reported:
            return
        reported.add(signature)
        cycle_text = " -> ".join(cycle)
        errors.append(f"src/modules/{path[-1]}.yaml: include cycle detected: {cycle_text}")

    def visit(name: str, path: list[str]) -> None:
        if name in visiting:
            report_cycle(path + [name])
            return
        if name in visited:
            return

        visiting.add(name)
        path.append(name)
        data = bundle_data.get(name)
        if isinstance(data, dict):
            includes = data.get("includes")
            if isinstance(includes, list):
                for included in includes:
                    if isinstance(included, str) and included in bundle_data:
                        visit(included, path)
        path.pop()
        visiting.remove(name)
        visited.add(name)

    for manifest in manifests:
        visit(manifest.stem, [])


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

    skill_dirs = iter_skill_dirs()
    if not skill_dirs:
        errors.append("no skill directories found in src/content/skills/")

    for skill_dir in skill_dirs:
        validate_content_skill(skill_dir, errors)

    markdown_files = sorted(CONTENT_ROOT.rglob("*.md")) if CONTENT_ROOT.exists() else []
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
