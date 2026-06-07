#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/generate-qa-report/scripts/validate_generate_qa_report.py"
FIXTURES="$ROOT_DIR/skills/generate-qa-report/scripts/fixtures"
TMP_OUT="${TMPDIR:-/tmp}/generate-qa-report-check.out"

python3 -B "$SCRIPT" "$FIXTURES/valid-complete-report.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-clean-report.json"

invalid=(
  invalid-bad-severity.json
  invalid-count-mismatch.json
  invalid-missing-finding-evidence.json
  invalid-tldr-too-long.json
  invalid-recommendation-rank-gap.json
  invalid-missing-source-evidence.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >"$TMP_OUT" 2>&1; then
    cat "$TMP_OUT"
    echo "expected failure for $fixture"
    exit 1
  fi
done

rm -f "$TMP_OUT"
echo "generate-qa-report check passed: valid=2 invalid=${#invalid[@]}"
