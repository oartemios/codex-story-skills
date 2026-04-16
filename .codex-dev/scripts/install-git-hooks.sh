#!/usr/bin/env bash
set -euo pipefail

git config core.hooksPath .githooks

echo "Git hooks enabled from .githooks"
echo "pre-commit: validates skill language and package integrity"
echo "pre-push: builds plugins, validates, packages release assets, and checks shell syntax"
