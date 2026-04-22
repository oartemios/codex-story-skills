#!/usr/bin/env python3
"""Build installable plugin bundles from internal skill sources."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from bundle_sources import PLUGINS_ROOT, bundle_names
from targets.codex import build_plugin, build_raw_codex_skills


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
    if not args.bundles:
        if PLUGINS_ROOT.exists():
            for path in sorted(PLUGINS_ROOT.iterdir()):
                if path.is_dir() and path.name not in names:
                    shutil.rmtree(path)
    for name in names:
        build_plugin(name)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
