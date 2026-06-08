#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/google-workspace-apis"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/google-workspace-apis.md"

python3 "$SKILL_DIR/scripts/compile-google-workspace-apis.py" \
  --input "$SKILL_DIR/scripts/fixtures/google-workspace-apis-input.json" \
  --output "$OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-workspace-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

if python3 "$SKILL_DIR/scripts/compile-google-workspace-apis.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-consent.json" \
  >"$TMP_DIR/invalid-consent.out" 2>"$TMP_DIR/invalid-consent.err"; then
  echo "ERROR: invalid missing-consent fixture unexpectedly passed" >&2
  exit 1
fi
grep -q "human_consent.status=confirmed" "$TMP_DIR/invalid-consent.err"

if python3 "$SKILL_DIR/scripts/compile-google-workspace-apis.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-broad-scope.json" \
  >"$TMP_DIR/invalid-scope.out" 2>"$TMP_DIR/invalid-scope.err"; then
  echo "ERROR: invalid broad-scope fixture unexpectedly passed" >&2
  exit 1
fi
grep -q "does not match operation access" "$TMP_DIR/invalid-scope.err"

if python3 "$SKILL_DIR/scripts/compile-google-workspace-apis.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-mutation-without-read.json" \
  >"$TMP_DIR/invalid-read.out" 2>"$TMP_DIR/invalid-read.err"; then
  echo "ERROR: invalid mutation-without-read fixture unexpectedly passed" >&2
  exit 1
fi
grep -q "requires read_before_write=true" "$TMP_DIR/invalid-read.err"

if python3 "$SKILL_DIR/scripts/compile-google-workspace-apis.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-mcp-tool-mismatch.json" \
  >"$TMP_DIR/invalid-tool.out" 2>"$TMP_DIR/invalid-tool.err"; then
  echo "ERROR: invalid mcp-tool-mismatch fixture unexpectedly passed" >&2
  exit 1
fi
grep -q "belongs to drive, not calendar" "$TMP_DIR/invalid-tool.err"

echo "OK: google-workspace-apis scripts are deterministic and offline"
