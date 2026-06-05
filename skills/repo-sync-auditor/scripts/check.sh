#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SCRIPT="$ROOT_DIR/skills/repo-sync-auditor/scripts/audit-repo-sync.py"
FIXTURES="$ROOT_DIR/skills/repo-sync-auditor/scripts/fixtures"
JSON_OUT="$(mktemp "${TMPDIR:-/tmp}/repo-sync-audit-json.XXXXXX")"
MD_OUT="$(mktemp "${TMPDIR:-/tmp}/repo-sync-audit-md.XXXXXX")"
NON_GIT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/repo-sync-not-git.XXXXXX")"
INVALID_OUT="$(mktemp "${TMPDIR:-/tmp}/repo-sync-invalid.XXXXXX")"
trap 'rm -rf "$JSON_OUT" "$MD_OUT" "$NON_GIT_DIR" "$INVALID_OUT"' EXIT

before="$(git -C "$ROOT_DIR" status --porcelain=v1)"

python3 "$SCRIPT" --root "$ROOT_DIR" --format json >"$JSON_OUT"
python3 "$SCRIPT" --root "$ROOT_DIR" --format markdown >"$MD_OUT"

python3 - "$JSON_OUT" "$FIXTURES/expected-report-fragments.json" <<'PY'
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
expected = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))

for key in expected["required_top_level"]:
    assert key in report, f"missing top-level key: {key}"
for key in expected["required_git_fields"]:
    assert key in report["git"], f"missing git key: {key}"
for key in expected["required_ledger_fields"]:
    assert key in report["ledger"], f"missing ledger key: {key}"
assert report["skill"] == "repo-sync-auditor"
assert isinstance(report["blockers"], list)
assert isinstance(report["recommendations"], list) and report["recommendations"]
assert any("[CODE]" in item for item in report["evidence"])
PY

grep -q "# Repo Sync Audit" "$MD_OUT"
grep -q "\[CODE\] Branch" "$MD_OUT"
grep -q "\[INFERENCE\]" "$MD_OUT"

if python3 "$SCRIPT" --root "$NON_GIT_DIR" --format json >"$INVALID_OUT" 2>&1; then
  echo "expected non-git fixture to fail"
  exit 1
fi
grep -q "not a git repository" "$INVALID_OUT"

after="$(git -C "$ROOT_DIR" status --porcelain=v1)"
if [[ "$before" != "$after" ]]; then
  echo "audit mutated working tree"
  exit 1
fi

echo "OK: repo-sync-auditor reports repo drift read-only"
