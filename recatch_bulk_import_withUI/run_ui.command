#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null
python -m pip install -e . >/dev/null

(
  sleep 2
  open "http://127.0.0.1:8877" >/dev/null 2>&1 || true
) &

exec recatch-bulk-import-ui
