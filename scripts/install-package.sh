#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/oartemios/codex-story-skills.git"
REF="main"
WORKDIR=""
DEST_DIR="${HOME}/.codex/skills"

usage() {
  cat <<'EOF'
Usage:
  scripts/install-package.sh [--repo-url URL] [--ref REF] [--workdir PATH] [--dest PATH]

Behavior:
  1. Clones the package
  2. Validates it
  3. Safely syncs it into Codex Home
  4. Prints a short overview and example prompts
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-url)
      REPO_URL="$2"
      shift 2
      ;;
    --ref)
      REF="$2"
      shift 2
      ;;
    --workdir)
      WORKDIR="$2"
      shift 2
      ;;
    --dest)
      DEST_DIR="$2"
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

cleanup() {
  if [[ -n "${TEMP_DIR:-}" && -d "${TEMP_DIR}" ]]; then
    rm -rf "${TEMP_DIR}"
  fi
}

if [[ -z "${WORKDIR}" ]]; then
  TEMP_DIR="$(mktemp -d)"
  trap cleanup EXIT
  CLONE_PARENT="${TEMP_DIR}"
else
  mkdir -p "${WORKDIR}"
  CLONE_PARENT="${WORKDIR}"
fi

CLONE_DIR="${CLONE_PARENT}/codex-story-skills"

echo "==> Cloning ${REPO_URL} (${REF})"
git clone --depth 1 --branch "${REF}" "${REPO_URL}" "${CLONE_DIR}"

echo
echo "==> Installing into ${DEST_DIR}"
"${CLONE_DIR}/scripts/sync-to-codex.sh" --dest "${DEST_DIR}"

echo
echo "==> Пакет установлен"
echo "Возможности:"
echo " - project-orchestrator: помогает выбрать следующий skill и маршрут работы"
echo " - continuity-keeper: отслеживает изменения канона и сломанные связи"
echo " - writer-assistant: собирает канон, структуру, персонажей и рабочий слой"
echo " - story-analyst: проводит диагностику ритма, арок и противоречий"
echo " - project-bootstrap: создает или выравнивает структуру проекта"
echo
echo "Примеры запросов:"
echo " - \"Хочу проработать книгу 1\""
echo " - \"Собери канон после серии решений\""
echo " - \"Проверь, что сломалось после правок\""
echo " - \"Подготовь книгу к диагностике\""
echo " - \"С чего начать новый художественный проект\""
echo
echo "Документация:"
BASE_URL="${REPO_URL%.git}"
echo " - README: ${BASE_URL}/blob/${REF}/README.md"
echo " - INSTALL: ${BASE_URL}/blob/${REF}/INSTALL.md"
echo " - CONTRIBUTING: ${BASE_URL}/blob/${REF}/CONTRIBUTING.md"
echo
echo "Перезапусти Codex, чтобы он перечитал список skills."
