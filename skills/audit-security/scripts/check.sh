#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

SKILL="skills/audit-security"
VALIDATOR="$SKILL/scripts/validate_security_report.py"
CONTRACT="$SKILL/assets/report-contract.json"
SCAN="$SKILL/assets/scan-policy.json"
EVIDENCE="$SKILL/assets/evidence-policy.json"

python3 -m json.tool "$SKILL/assets/manifest.json" >/dev/null
python3 -m json.tool "$SKILL/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$SCAN" >/dev/null
python3 -m json.tool "$EVIDENCE" >/dev/null
python3 -m json.tool "$SKILL/evals/evals.json" >/dev/null
python3 -B "$VALIDATOR" --help >/dev/null

python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --scan-policy "$SCAN" \
  --evidence-policy "$EVIDENCE" \
  --report "$SKILL/scripts/fixtures/valid-security-report.json" >/dev/null

if python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --scan-policy "$SCAN" \
  --evidence-policy "$EVIDENCE" \
  --report "$SKILL/scripts/fixtures/invalid-placeholder-critical.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-placeholder-critical fixture passed unexpectedly"
  exit 1
fi

if python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --scan-policy "$SCAN" \
  --evidence-policy "$EVIDENCE" \
  --report "$SKILL/scripts/fixtures/invalid-missing-category.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-missing-category fixture passed unexpectedly"
  exit 1
fi

echo "OK: audit-security reports validated deterministically"
