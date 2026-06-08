#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/google-analytics"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/google-analytics.md"

python3 "$SKILL_DIR/scripts/compile-google-analytics.py" \
  --input "$SKILL_DIR/scripts/fixtures/google-analytics-input.json" \
  --output "$OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-analytics-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

if python3 "$SKILL_DIR/scripts/compile-google-analytics.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-confirmation.json" \
  >"$TMP_DIR/invalid-confirmation.out" 2>"$TMP_DIR/invalid-confirmation.err"; then
  echo "ERROR: invalid missing-confirmation fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "human_confirmation.status=confirmed" "$TMP_DIR/invalid-confirmation.err"

if python3 "$SKILL_DIR/scripts/compile-google-analytics.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-event-naming.json" \
  >"$TMP_DIR/invalid-naming.out" 2>"$TMP_DIR/invalid-naming.err"; then
  echo "ERROR: invalid event naming fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "event_name must match lowercase_snake_case" "$TMP_DIR/invalid-naming.err"

if python3 "$SKILL_DIR/scripts/compile-google-analytics.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-pii-parameter.json" \
  >"$TMP_DIR/invalid-pii.out" 2>"$TMP_DIR/invalid-pii.err"; then
  echo "ERROR: invalid PII fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "PII risk high is blocking" "$TMP_DIR/invalid-pii.err"

if python3 "$SKILL_DIR/scripts/compile-google-analytics.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-measurement-protocol-only.json" \
  >"$TMP_DIR/invalid-mp.out" 2>"$TMP_DIR/invalid-mp.err"; then
  echo "ERROR: invalid Measurement Protocol-only fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "measurement_protocol_only is blocked" "$TMP_DIR/invalid-mp.err"

echo "OK: google-analytics scripts are deterministic and offline"
