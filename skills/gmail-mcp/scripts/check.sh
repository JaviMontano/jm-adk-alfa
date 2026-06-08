#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/gmail-mcp"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/gmail-mcp.md"

python3 "$SKILL_DIR/scripts/compile-gmail-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/gmail-mcp-input.json" \
  --output "$OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-gmail-mcp-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

if python3 "$SKILL_DIR/scripts/compile-gmail-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-direct-send-without-confirmation.json" \
  >"$TMP_DIR/invalid.out" 2>"$TMP_DIR/invalid.err"; then
  echo "ERROR: invalid fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "requires human confirmation" "$TMP_DIR/invalid.err"

echo "OK: gmail-mcp scripts are deterministic and offline"
