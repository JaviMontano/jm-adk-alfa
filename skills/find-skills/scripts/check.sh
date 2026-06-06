#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/find-skills/scripts/validate_find_skills_report.py"
FIXTURES="$ROOT_DIR/skills/find-skills/scripts/fixtures"
TMP_OUT="${TMPDIR:-/tmp}/find-skills-check.out"

python3 -B "$SCRIPT" "$FIXTURES/valid-local-recommendation.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-no-match-report.json"

invalid=(
  invalid-auto-install.json
  invalid-remote-live-claim.json
  invalid-unscored-candidate.json
  invalid-f-tier-recommended.json
  invalid-missing-evidence-tags.json
  invalid-too-many-candidates.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >"$TMP_OUT" 2>&1; then
    cat "$TMP_OUT"
    echo "expected failure for $fixture"
    exit 1
  fi
done

rm -f "$TMP_OUT"
echo "find-skills check passed: valid=2 invalid=${#invalid[@]}"
