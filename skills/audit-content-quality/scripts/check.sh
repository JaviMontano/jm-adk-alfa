#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

SKILL="skills/audit-content-quality"
VALIDATOR="$SKILL/scripts/validate_content_quality_report.py"
CONTRACT="$SKILL/assets/report-contract.json"
RUBRIC="$SKILL/assets/scoring-rubric.json"
EVIDENCE="$SKILL/assets/evidence-policy.json"

python3 -m json.tool "$SKILL/assets/manifest.json" >/dev/null
python3 -m json.tool "$SKILL/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$RUBRIC" >/dev/null
python3 -m json.tool "$EVIDENCE" >/dev/null
python3 -m json.tool "$SKILL/evals/evals.json" >/dev/null
python3 -B "$VALIDATOR" --help >/dev/null

python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --rubric "$RUBRIC" \
  --evidence-policy "$EVIDENCE" \
  --report "$SKILL/scripts/fixtures/valid-content-quality-report.json" >/dev/null

if python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --rubric "$RUBRIC" \
  --evidence-policy "$EVIDENCE" \
  --report "$SKILL/scripts/fixtures/invalid-wrong-grade.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-wrong-grade fixture passed unexpectedly"
  exit 1
fi

if python3 -B "$VALIDATOR" \
  --contract "$CONTRACT" \
  --rubric "$RUBRIC" \
  --evidence-policy "$EVIDENCE" \
  --report "$SKILL/scripts/fixtures/invalid-missing-bottom.json" >/dev/null 2>&1; then
  echo "ERROR: invalid-missing-bottom fixture passed unexpectedly"
  exit 1
fi

echo "OK: audit-content-quality reports validated deterministically"
