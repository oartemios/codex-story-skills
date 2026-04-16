"""Read internal bundle manifests.

The project keeps bundle manifests as small YAML files without requiring
third-party YAML dependencies for the build scripts.
"""

from __future__ import annotations

from pathlib import Path


def parse_scalar(value: str) -> str | bool:
    if value == "true":
        return True
    if value == "false":
        return False
    return value


def load_bundle_manifest(path: Path) -> dict:
    data: dict[str, object] = {}
    current_list: str | None = None

    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        if line.startswith("  - "):
            if current_list is None:
                raise ValueError(f"{path}: list item without list key on line {lineno}")
            item = line[4:].strip()
            if not item:
                raise ValueError(f"{path}: empty list item on line {lineno}")
            data[current_list].append(parse_scalar(item))  # type: ignore[index, union-attr]
            continue

        if line.startswith(" "):
            raise ValueError(f"{path}: unsupported indentation on line {lineno}")

        if ":" not in line:
            raise ValueError(f"{path}: expected key/value on line {lineno}")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"{path}: empty key on line {lineno}")
        if value:
            data[key] = parse_scalar(value)
            current_list = None
        else:
            data[key] = []
            current_list = key

    return data
