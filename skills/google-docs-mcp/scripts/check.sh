#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/google-docs-mcp"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/google-docs-mcp.md"

python3 "$SKILL_DIR/scripts/compile-google-docs-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/google-docs-mcp-input.json" \
  --output "$OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-docs-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

if python3 "$SKILL_DIR/scripts/compile-google-docs-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-confirmation.json" \
  >"$TMP_DIR/invalid-confirmation.out" 2>"$TMP_DIR/invalid-confirmation.err"; then
  echo "ERROR: invalid missing confirmation fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "human_confirmation.status=confirmed" "$TMP_DIR/invalid-confirmation.err"

if python3 "$SKILL_DIR/scripts/compile-google-docs-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-create-with-content.json" \
  >"$TMP_DIR/invalid-create.out" 2>"$TMP_DIR/invalid-create.err"; then
  echo "ERROR: invalid create-with-content fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "documents.create cannot include body content" "$TMP_DIR/invalid-create.err"

if python3 "$SKILL_DIR/scripts/compile-google-docs-mcp.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-batch-without-get.json" \
  >"$TMP_DIR/invalid-batch.out" 2>"$TMP_DIR/invalid-batch.err"; then
  echo "ERROR: invalid batch-without-get fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "documents.batchUpdate requires a prior documents.get" "$TMP_DIR/invalid-batch.err"

echo "OK: google-docs-mcp scripts are deterministic"
