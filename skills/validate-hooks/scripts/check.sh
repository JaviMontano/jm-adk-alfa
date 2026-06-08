#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/validate-hooks"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/validate-hooks.md"

python3 "$SKILL_DIR/scripts/compile-validate-hooks.py" \
  --input "$SKILL_DIR/scripts/fixtures/valid-hooks-audit-input.json" \
  --output "$OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-hooks-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

if python3 "$SKILL_DIR/scripts/compile-validate-hooks.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-tooluse-context.json" \
  >"$TMP_DIR/invalid-tooluse.out" 2>"$TMP_DIR/invalid-tooluse.err"; then
  echo "ERROR: invalid ToolUseContext fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "does not provide ToolUseContext" "$TMP_DIR/invalid-tooluse.out"
grep -q "Command string can discard local work" "$TMP_DIR/invalid-tooluse.out"

if python3 "$SKILL_DIR/scripts/compile-validate-hooks.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-flat-array-hooks.json" \
  >"$TMP_DIR/invalid-flat.out" 2>"$TMP_DIR/invalid-flat.err"; then
  echo "ERROR: invalid flat-array fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "canonical hooks.json requires an event-keyed object" "$TMP_DIR/invalid-flat.out"

echo "OK: validate-hooks scripts are deterministic"
