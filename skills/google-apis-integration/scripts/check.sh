#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/google-apis-integration"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/google-apis-integration.md"
JSON_OUT="$TMP_DIR/google-apis-integration.json"

python3 "$SKILL_DIR/scripts/compile-google-apis-integration.py" \
  --input "$SKILL_DIR/scripts/fixtures/google-apis-integration-input.json" \
  --output "$OUT"

python3 "$SKILL_DIR/scripts/compile-google-apis-integration.py" \
  --format json \
  --input "$SKILL_DIR/scripts/fixtures/google-apis-integration-input.json" \
  --output "$JSON_OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-google-apis-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

python3 - "$JSON_OUT" <<'PY'
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert data["plan_schema"] == "google-apis-integration-plan/v1"
assert data["skill"] == "google-apis-integration"
assert data["service_count"] == 5
assert data["mutation_count"] == 3
assert data["validation"]["offline"] is True
PY

if python3 "$SKILL_DIR/scripts/compile-google-apis-integration.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-consent.json" \
  >"$TMP_DIR/invalid-consent.out" 2>"$TMP_DIR/invalid-consent.err"; then
  echo "ERROR: invalid missing-consent fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "human_consent.status=confirmed" "$TMP_DIR/invalid-consent.err"

if python3 "$SKILL_DIR/scripts/compile-google-apis-integration.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-broad-scope.json" \
  >"$TMP_DIR/invalid-scope.out" 2>"$TMP_DIR/invalid-scope.err"; then
  echo "ERROR: invalid broad-scope fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "auth_profile sheets_full_write is broader than needed" "$TMP_DIR/invalid-scope.err"

if python3 "$SKILL_DIR/scripts/compile-google-apis-integration.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-idempotency.json" \
  >"$TMP_DIR/invalid-idempotency.out" 2>"$TMP_DIR/invalid-idempotency.err"; then
  echo "ERROR: invalid missing-idempotency fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "requires idempotency_key" "$TMP_DIR/invalid-idempotency.err"

echo "OK: google-apis-integration scripts are deterministic and offline"
