#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/google-drive-mcp"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/google-drive-mcp.md"

python3 "$SKILL_DIR/scripts/compile-google-drive-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/google-drive-mcp-input.json" \
  --output "$OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-drive-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

if python3 "$SKILL_DIR/scripts/compile-google-drive-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-trashed.json" \
  >"$TMP_DIR/invalid-trashed.out" 2>"$TMP_DIR/invalid-trashed.err"; then
  echo "ERROR: invalid missing trashed fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "search.q must include trashed = false" "$TMP_DIR/invalid-trashed.err"

if python3 "$SKILL_DIR/scripts/compile-google-drive-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-share-no-confirmation.json" \
  >"$TMP_DIR/invalid-share.out" 2>"$TMP_DIR/invalid-share.err"; then
  echo "ERROR: invalid sharing fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "sharing permissions require human confirmation" "$TMP_DIR/invalid-share.err"

echo "OK: google-drive-mcp scripts are deterministic"
