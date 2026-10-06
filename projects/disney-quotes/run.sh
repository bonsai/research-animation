#!/usr/bin/env bash
# DISNEY-QUOTES CORPUS — full pipeline runner.
#
# Usage:
#   ./run.sh          validate + build graph + viz + site + jsonl
#   ./run.sh --init   (re)create the corpus DB from seed data, then build
#
# NOTE: must run under WSL (Linux paths). SQLite misbehaves on
# \\wsl.localhost\ UNC paths, so run this inside the distro, not Windows Python.

set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
scripts="$here/scripts"
py="${PYTHON:-python3}"

if [[ "${1:-}" == "--init" ]]; then
    echo "==> init: seeding corpus DB"
    rm -f "$here/disney-quotes.db"
    "$py" "$scripts/init.py"
fi

echo "==> validate"
"$py" "$scripts/validate.py"

echo "==> graph"
"$py" "$scripts/graph-builder.py"

echo "==> viz"
"$py" "$scripts/build-viz.py"

echo "==> site"
"$py" "$scripts/build-site.py"

echo "==> jsonl export"
"$py" - "$here" <<'PY'
import sys, os
root = sys.argv[1]
sys.path.insert(0, os.path.join(root, 'corpus'))
from database import Corpus
Corpus().export_jsonl(os.path.join(root, 'corpus', 'quotes.jsonl'))
print('exported corpus/quotes.jsonl')
PY

echo "==> done"