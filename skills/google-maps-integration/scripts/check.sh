#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/google-maps-integration"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

OUT="$TMP_DIR/google-maps-platform-plan.md"

python3 "$SKILL_DIR/scripts/compile-google-maps-plan.py" \
  --input "$SKILL_DIR/scripts/fixtures/google-maps-plan-input.json" \
  --output "$OUT"

python3 - "$OUT" "$SKILL_DIR/scripts/fixtures/expected-maps-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
fragments = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["fragments"]
missing = [fragment for fragment in fragments if fragment not in report]
if missing:
    raise SystemExit(f"missing expected fragments: {missing}")
PY

if python3 "$SKILL_DIR/scripts/compile-google-maps-plan.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-confirmation.json" \
  >"$TMP_DIR/invalid-confirmation.out" 2>"$TMP_DIR/invalid-confirmation.err"; then
  echo "ERROR: invalid missing-confirmation fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "human_confirmation.status must be confirmed" "$TMP_DIR/invalid-confirmation.err"

if python3 "$SKILL_DIR/scripts/compile-google-maps-plan.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-unrestricted-client-key.json" \
  >"$TMP_DIR/invalid-key.out" 2>"$TMP_DIR/invalid-key.err"; then
  echo "ERROR: invalid unrestricted-client-key fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "browser key requires allowed_referrers" "$TMP_DIR/invalid-key.err"

if python3 "$SKILL_DIR/scripts/compile-google-maps-plan.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-price-amount.json" \
  >"$TMP_DIR/invalid-price.out" 2>"$TMP_DIR/invalid-price.err"; then
  echo "ERROR: invalid price fixture unexpectedly passed" >&2
  exit 1
fi

grep -q "monetary prices are not allowed" "$TMP_DIR/invalid-price.err"

echo "OK: google-maps-integration scripts are deterministic and offline"
