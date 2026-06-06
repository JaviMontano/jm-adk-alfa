#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="$skill_dir/scripts/validate_changelog_report.py"
fixtures="$skill_dir/scripts/fixtures"

python3 -B "$validator" "$fixtures/valid-decision-report.json"
python3 -B "$validator" "$fixtures/valid-duplicate-block-report.json"

if python3 -B "$validator" "$fixtures/invalid-unknown-type.json" >/tmp/changelog-type.log 2>&1; then
  echo "ERROR: invalid-unknown-type.json unexpectedly passed"
  cat /tmp/changelog-type.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-future-date.json" >/tmp/changelog-future.log 2>&1; then
  echo "ERROR: invalid-future-date.json unexpectedly passed"
  cat /tmp/changelog-future.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-duplicate-append.json" >/tmp/changelog-duplicate.log 2>&1; then
  echo "ERROR: invalid-duplicate-append.json unexpectedly passed"
  cat /tmp/changelog-duplicate.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-missing-principles.json" >/tmp/changelog-principles.log 2>&1; then
  echo "ERROR: invalid-missing-principles.json unexpectedly passed"
  cat /tmp/changelog-principles.log
  exit 1
fi

if python3 -B "$validator" "$fixtures/invalid-unauthorized-entry.json" >/tmp/changelog-unauthorized.log 2>&1; then
  echo "ERROR: invalid-unauthorized-entry.json unexpectedly passed"
  cat /tmp/changelog-unauthorized.log
  exit 1
fi

echo "changelog-management fixture validation passed"
