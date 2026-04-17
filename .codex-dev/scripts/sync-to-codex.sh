#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_DIR=""
DEST_DIR="${HOME}/.codex/skills"
BACKUP_ROOT=""
DRY_RUN=0
TEMP_DIR=""

cleanup() {
  if [[ -n "${TEMP_DIR}" ]]; then
    rm -rf "${TEMP_DIR}"
  fi
}
trap cleanup EXIT

usage() {
  cat <<'EOF'
Usage:
  .codex-dev/scripts/sync-to-codex.sh [--dry-run] [--dest PATH] [--backup-root PATH]

Options:
  --dry-run           Show what would be synced without changing ~/.codex/skills
  --dest PATH         Override target Codex skills directory
  --backup-root PATH  Override backup directory root
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --dest)
      DEST_DIR="$2"
      shift 2
      ;;
    --backup-root)
      BACKUP_ROOT="$2"
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

echo "==> Validating skills package"
python3 "${SCRIPT_DIR}/validate-skills.py"

TEMP_DIR="$(mktemp -d)"
SOURCE_DIR="${TEMP_DIR}/codex-skills"

echo "==> Building raw Codex skills package"
python3 "${SCRIPT_DIR}/build-plugins.py" --raw-skills-dir "${SOURCE_DIR}"

if [[ -z "${BACKUP_ROOT}" ]]; then
  BACKUP_ROOT="$(dirname "${DEST_DIR}")/skill-backups"
fi

mkdir -p "${DEST_DIR}"

mapfile -t MANAGED_ITEMS < <(find "${SOURCE_DIR}" -mindepth 1 -maxdepth 1 -print | sort)

if [[ ${DRY_RUN} -eq 1 ]]; then
  echo
  echo "==> Dry run: managed top-level items"
  for item in "${MANAGED_ITEMS[@]}"; do
    echo " - $(basename "${item}")"
  done
  echo
  echo "==> Dry run: rsync preview"
  rsync -avn --itemize-changes "${SOURCE_DIR}/" "${DEST_DIR}/"
  exit 0
fi

TIMESTAMP="$(date +"%Y-%m-%d_%H-%M-%S")"
BACKUP_DIR="${BACKUP_ROOT}/${TIMESTAMP}"
mkdir -p "${BACKUP_DIR}"

echo
echo "==> Backing up managed items to ${BACKUP_DIR}"
for item in "${MANAGED_ITEMS[@]}"; do
  name="$(basename "${item}")"
  target="${DEST_DIR}/${name}"

  if [[ -L "${target}" ]]; then
    echo " - moving symlink ${name} to backup"
    mv "${target}" "${BACKUP_DIR}/${name}"
    continue
  fi

  if [[ -e "${target}" ]]; then
    echo " - copying existing ${name}"
    rsync -a "${target}" "${BACKUP_DIR}/"
  fi
done

echo
echo "==> Syncing package into ${DEST_DIR}"
rsync -a --checksum "${SOURCE_DIR}/" "${DEST_DIR}/"

echo
echo "==> Post-check"
python3 "${SCRIPT_DIR}/validate-skills.py" >/dev/null

for item in "${MANAGED_ITEMS[@]}"; do
  name="$(basename "${item}")"
  target="${DEST_DIR}/${name}"
  if [[ ! -e "${target}" ]]; then
    echo "Missing installed item after sync: ${name}" >&2
    exit 1
  fi
done

echo "Sync completed."
echo "Backup saved to: ${BACKUP_DIR}"
echo "Restart Codex to reload skills."
