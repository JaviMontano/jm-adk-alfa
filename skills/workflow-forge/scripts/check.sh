#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/workflow-forge"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/workflow-forge-schema.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/workflow-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/skill-audit-workflow.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-single-phase.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-missing-verification.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-prohibited-stack.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/expected-workflow-fragments.json" >/dev/null

python3 -m py_compile "$SKILL_DIR/scripts/compile-workflow-forge.py"

python3 "$SKILL_DIR/scripts/compile-workflow-forge.py" \
  --input "$SKILL_DIR/scripts/fixtures/skill-audit-workflow.json" \
  --output "$TMP_DIR/workflow.md"

python3 "$SKILL_DIR/scripts/compile-workflow-forge.py" \
  --input "$SKILL_DIR/scripts/fixtures/skill-audit-workflow.json" \
  --format json \
  --output "$TMP_DIR/workflow.json"

python3 - "$SKILL_DIR/scripts/fixtures/expected-workflow-fragments.json" "$TMP_DIR/workflow.md" "$TMP_DIR/workflow.json" <<'PY'
import json
import sys
from pathlib import Path

expected = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
markdown = Path(sys.argv[2]).read_text(encoding="utf-8")
data = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))

for fragment in expected["markdown"]:
    if fragment not in markdown:
        raise SystemExit(f"missing markdown fragment: {fragment}")
for section in expected["json_sections"]:
    if section not in data:
        raise SystemExit(f"missing JSON section: {section}")
if not data["validation"]["valid"]:
    raise SystemExit("valid fixture returned validation.valid=false")
PY

if python3 "$SKILL_DIR/scripts/compile-workflow-forge.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-single-phase.json" \
  --output "$TMP_DIR/invalid-single.md" 2>"$TMP_DIR/invalid-single.err"; then
  echo "ERROR: invalid-single-phase fixture passed unexpectedly" >&2
  exit 1
fi
grep -q "workflow must have at least 2 phases" "$TMP_DIR/invalid-single.err"

if python3 "$SKILL_DIR/scripts/compile-workflow-forge.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-missing-verification.json" \
  --output "$TMP_DIR/invalid-verification.md" 2>"$TMP_DIR/invalid-verification.err"; then
  echo "ERROR: invalid-missing-verification fixture passed unexpectedly" >&2
  exit 1
fi
grep -q "final phase kind must be verification" "$TMP_DIR/invalid-verification.err"

if python3 "$SKILL_DIR/scripts/compile-workflow-forge.py" \
  --input "$SKILL_DIR/scripts/fixtures/invalid-prohibited-stack.json" \
  --output "$TMP_DIR/invalid-stack.md" 2>"$TMP_DIR/invalid-stack.err"; then
  echo "ERROR: invalid-prohibited-stack fixture passed unexpectedly" >&2
  exit 1
fi
grep -q "prohibited stack reference: Docker" "$TMP_DIR/invalid-stack.err"

echo "OK: workflow-forge scripts are deterministic"
