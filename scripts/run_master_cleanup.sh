#!/usr/bin/env bash
set -euo pipefail
DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
fi
cd "$(dirname "$0")/.."
if [[ -f ".venv/bin/activate" ]]; then
  . .venv/bin/activate
fi
python3 scripts/master_cleanup.py $DRY_RUN
