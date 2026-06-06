#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/git-workflow/scripts/validate_git_workflow_plan.py"
FIXTURES="$ROOT_DIR/skills/git-workflow/scripts/fixtures"
TMP_OUT="${TMPDIR:-/tmp}/git-workflow-check.out"

python3 -B "$SCRIPT" "$FIXTURES/valid-feature-pr-plan.json"
python3 -B "$SCRIPT" "$FIXTURES/valid-release-tag-plan.json"

invalid=(
  invalid-dirty-tree-proceed.json
  invalid-main-not-aligned.json
  invalid-unsafe-force-push.json
  invalid-missing-validation.json
  invalid-bad-branch-name.json
  invalid-release-without-tag-evidence.json
)

for fixture in "${invalid[@]}"; do
  if python3 -B "$SCRIPT" "$FIXTURES/$fixture" >"$TMP_OUT" 2>&1; then
    cat "$TMP_OUT"
    echo "expected failure for $fixture"
    exit 1
  fi
done

rm -f "$TMP_OUT"
echo "git-workflow check passed: valid=2 invalid=${#invalid[@]}"
