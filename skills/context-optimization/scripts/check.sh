#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="$skill_dir/scripts/validate_context_optimization_report.py"
fixtures="$skill_dir/scripts/fixtures"

python3 -B "$validator" "$fixtures/valid-standard-report.json"
python3 -B "$validator" "$fixtures/valid-lazy-load-report.json"

if python3 -B "$validator" "$fixtures/invalid-two-l3.json" >/tmp/context-opt-two-l3.log 2>&1; then
  echo "ERROR: invalid-two-l3.json unexpectedly passed"
  cat /tmp/context-opt-two-l3.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-low-relevance-l3.json" >/tmp/context-opt-low-l3.log 2>&1; then
  echo "ERROR: invalid-low-relevance-l3.json unexpectedly passed"
  cat /tmp/context-opt-low-l3.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-risky-prune.json" >/tmp/context-opt-risky-prune.log 2>&1; then
  echo "ERROR: invalid-risky-prune.json unexpectedly passed"
  cat /tmp/context-opt-risky-prune.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-no-improvement.json" >/tmp/context-opt-no-improvement.log 2>&1; then
  echo "ERROR: invalid-no-improvement.json unexpectedly passed"
  cat /tmp/context-opt-no-improvement.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-unauthorized-persist.json" >/tmp/context-opt-unauthorized.log 2>&1; then
  echo "ERROR: invalid-unauthorized-persist.json unexpectedly passed"
  cat /tmp/context-opt-unauthorized.log
  exit 1
fi

echo "context-optimization fixture validation passed"
