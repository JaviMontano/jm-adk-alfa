#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/knowledge-management/scripts/validate_knowledge_management_report.py"
FIXTURES="$ROOT_DIR/skills/knowledge-management/scripts/fixtures"

python3 -B "$SCRIPT" "$FIXTURES/valid-knowledge-audit.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-decay-warning-report.json"

invalid=(
  invalid-missing-evidence-tag.json
  invalid-missing-retrieval-terms.json
  invalid-stale-without-action.json
  invalid-future-reviewed-date.json
  invalid-network-source.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >/tmp/knowledge-management-check.out 2>&1; then
    cat /tmp/knowledge-management-check.out
    echo "expected failure for $fixture"
    exit 1
  fi
done

echo "knowledge-management check passed: valid=2 invalid=${#invalid[@]}"
