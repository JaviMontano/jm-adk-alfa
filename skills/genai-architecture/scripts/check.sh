#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/genai-architecture"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/genai-architecture-report.md"

python3 "$SKILL_DIR/scripts/compile-genai-architecture.py" \
  --input "$SKILL_DIR/scripts/fixtures/genai-architecture-input.json" \
  --output "$OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-report-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

if python3 "$SKILL_DIR/scripts/compile-genai-architecture.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-retrieval.json" \
  >"$TMP_DIR/invalid.out" 2>"$TMP_DIR/invalid.err"; then
  echo "ERROR: invalid fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "rag_pipeline missing required stage ids" "$TMP_DIR/invalid.err"

echo "OK: genai-architecture scripts are deterministic"
