#!/usr/bin/env python3
"""Create GitHub Release zip assets from built plugin bundles."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGINS_ROOT = REPO_ROOT / "plugins"
DIST_ROOT = REPO_ROOT / "dist"


def package_plugin(plugin_dir: Path, dist_root: Path) -> None:
    if not (plugin_dir / ".codex-plugin" / "plugin.json").exists():
        raise SystemExit(f"Not a built plugin: {plugin_dir.relative_to(REPO_ROOT)}")
    archive_base = dist_root / plugin_dir.name
    shutil.make_archive(str(archive_base), "zip", root_dir=plugin_dir.parent, base_dir=plugin_dir.name)
    print(f"Wrote {(archive_base.with_suffix('.zip')).relative_to(REPO_ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugins", nargs="*", help="Plugin names. Defaults to all built plugins.")
    parser.add_argument("--dist", default=str(DIST_ROOT), help="Output directory for zip assets.")
    args = parser.parse_args()

    dist_root = Path(args.dist).expanduser().resolve()
    dist_root.mkdir(parents=True, exist_ok=True)

    names = args.plugins or sorted(path.name for path in PLUGINS_ROOT.iterdir() if path.is_dir())
    for name in names:
        package_plugin(PLUGINS_ROOT / name, dist_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
