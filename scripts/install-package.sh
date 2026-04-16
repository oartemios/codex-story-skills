#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/oartemios/codex-story-skills"
VERSION="v0.1.0"
PLUGIN="fiction-core"
ASSET_URL=""
PLUGIN_ROOT="${HOME}/plugins"
MARKETPLACE_PATH="${HOME}/.agents/plugins/marketplace.json"

usage() {
  cat <<'EOF'
Usage:
  scripts/install-package.sh [--plugin NAME] [--version VERSION] [--asset-url URL]
                             [--plugin-root PATH] [--marketplace PATH]

Installs a built Codex plugin release asset locally and registers it in the
local marketplace. Default plugin: fiction-core.

Plugins:
  fiction-core        Default fiction-first package
  engineering-addon   Optional RFC/ADR support
  obsidian-addon      Fiction Core plus Obsidian compatibility
  full                fiction-core plus optional addons

Examples:
  scripts/install-package.sh
  scripts/install-package.sh --plugin full --version v0.1.0
  scripts/install-package.sh --plugin engineering-addon
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --plugin)
      PLUGIN="$2"
      shift 2
      ;;
    --version|--ref)
      VERSION="$2"
      shift 2
      ;;
    --asset-url)
      ASSET_URL="$2"
      shift 2
      ;;
    --plugin-root)
      PLUGIN_ROOT="$2"
      shift 2
      ;;
    --marketplace)
      MARKETPLACE_PATH="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

case "${PLUGIN}" in
  fiction-core|engineering-addon|obsidian-addon|full)
    ;;
  *)
    echo "Unknown plugin: ${PLUGIN}" >&2
    usage >&2
    exit 1
    ;;
esac

if [[ -z "${ASSET_URL}" ]]; then
  if [[ "${VERSION}" == "latest" ]]; then
    ASSET_URL="${REPO_URL}/releases/latest/download/${PLUGIN}.zip"
  else
    ASSET_URL="${REPO_URL}/releases/download/${VERSION}/${PLUGIN}.zip"
  fi
fi

command -v curl >/dev/null || { echo "curl is required" >&2; exit 1; }
command -v unzip >/dev/null || { echo "unzip is required" >&2; exit 1; }
command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 1; }

TEMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "${TEMP_DIR}"
}
trap cleanup EXIT

ASSET_PATH="${TEMP_DIR}/${PLUGIN}.zip"
EXTRACT_DIR="${TEMP_DIR}/extract"
TARGET_DIR="${PLUGIN_ROOT}/${PLUGIN}"

mkdir -p "${EXTRACT_DIR}" "${PLUGIN_ROOT}" "$(dirname "${MARKETPLACE_PATH}")"

echo "==> Downloading ${ASSET_URL}"
curl -fsSL "${ASSET_URL}" -o "${ASSET_PATH}"

echo "==> Unpacking ${PLUGIN}"
unzip -q "${ASSET_PATH}" -d "${EXTRACT_DIR}"

if [[ -d "${EXTRACT_DIR}/${PLUGIN}" ]]; then
  UNPACKED_DIR="${EXTRACT_DIR}/${PLUGIN}"
else
  UNPACKED_DIR="${EXTRACT_DIR}"
fi

if [[ ! -f "${UNPACKED_DIR}/.codex-plugin/plugin.json" ]]; then
  echo "Release asset does not contain .codex-plugin/plugin.json" >&2
  exit 1
fi

if [[ -e "${TARGET_DIR}" ]]; then
  BACKUP_DIR="${PLUGIN_ROOT}/.${PLUGIN}.backup.$(date +"%Y-%m-%d_%H-%M-%S")"
  echo "==> Moving existing ${PLUGIN} to ${BACKUP_DIR}"
  mv "${TARGET_DIR}" "${BACKUP_DIR}"
fi

mv "${UNPACKED_DIR}" "${TARGET_DIR}"

echo "==> Registering ${PLUGIN} in ${MARKETPLACE_PATH}"
PLUGIN_NAME="${PLUGIN}" \
PLUGIN_DIR="${TARGET_DIR}" \
MARKETPLACE_PATH="${MARKETPLACE_PATH}" \
python3 - <<'PY'
import json
import os
from pathlib import Path

plugin_name = os.environ["PLUGIN_NAME"]
plugin_dir = Path(os.environ["PLUGIN_DIR"]).expanduser().resolve()
marketplace_path = Path(os.environ["MARKETPLACE_PATH"]).expanduser().resolve()
marketplace_root = marketplace_path.parent
home_plugin_dir = (Path.home() / "plugins" / plugin_name).resolve()

if plugin_dir == home_plugin_dir and marketplace_path == (Path.home() / ".agents" / "plugins" / "marketplace.json").resolve():
    source_path = f"./plugins/{plugin_name}"
else:
    source_path = "./" + os.path.relpath(plugin_dir, marketplace_root)

if marketplace_path.exists():
    data = json.loads(marketplace_path.read_text(encoding="utf-8"))
else:
    data = {
        "name": "local",
        "interface": {"displayName": "Local Plugins"},
        "plugins": [],
    }

plugins = data.setdefault("plugins", [])
entry = {
    "name": plugin_name,
    "source": {
        "source": "local",
        "path": source_path,
    },
    "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    },
    "category": "Writing",
}

for index, existing in enumerate(plugins):
    if existing.get("name") == plugin_name:
        plugins[index] = entry
        break
else:
    plugins.append(entry)

marketplace_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PY

echo "Installed plugin: ${PLUGIN}"
echo "Plugin path: ${TARGET_DIR}"
echo "Marketplace: ${MARKETPLACE_PATH}"
echo "Open Codex plugin management and install ${PLUGIN} from the local marketplace."
