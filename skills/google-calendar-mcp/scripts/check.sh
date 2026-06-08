#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/google-calendar-mcp"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/google-calendar-mcp.md"

python3 "$SKILL_DIR/scripts/compile-google-calendar-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/google-calendar-mcp-input.json" \
  --output "$OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-calendar-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

if python3 "$SKILL_DIR/scripts/compile-google-calendar-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-confirmation.json" \
  >"$TMP_DIR/invalid-confirmation.out" 2>"$TMP_DIR/invalid-confirmation.err"; then
  echo "ERROR: invalid missing-confirmation fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "human_confirmation.status=confirmed" "$TMP_DIR/invalid-confirmation.err"

if python3 "$SKILL_DIR/scripts/compile-google-calendar-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-broad-scope.json" \
  >"$TMP_DIR/invalid-scope.out" 2>"$TMP_DIR/invalid-scope.err"; then
  echo "ERROR: invalid broad-scope fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "requested_scope must be minimum scope" "$TMP_DIR/invalid-scope.err"

echo "OK: google-calendar-mcp scripts are deterministic and offline"
