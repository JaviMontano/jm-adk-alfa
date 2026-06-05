#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

SKILL="skills/assumption-log"
VALIDATOR="$SKILL/scripts/validate_assumption_log.py"
CONTRACT="$SKILL/assets/log-contract.json"
STATUS="$SKILL/assets/status-policy.json"
EVIDENCE="$SKILL/assets/evidence-policy.json"

python3 -m json.tool "$SKILL/assets/manifest.json" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$STATUS" >/dev/null
python3 -m json.tool "$EVIDENCE" >/dev/null
python3 -m json.tool "$SKILL/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$SKILL/evals/evals.json" >/dev/null
python3 -B "$VALIDATOR" --help >/dev/null

python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --status-policy "$STATUS" \
  --evidence-policy "$EVIDENCE" \
  --report "$SKILL/scripts/fixtures/valid-assumption-log.json" >/dev/null

if python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --status-policy "$STATUS" \
  --evidence-policy "$EVIDENCE" \
  --report "$SKILL/scripts/fixtures/invalid-id-gap.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-id-gap fixture passed unexpectedly"
  exit 1
fi

if python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --status-policy "$STATUS" \
  --evidence-policy "$EVIDENCE" \
  --report "$SKILL/scripts/fixtures/invalid-false-validated.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-false-validated fixture passed unexpectedly"
  exit 1
fi

echo "OK: assumption-log reports validated deterministically"
