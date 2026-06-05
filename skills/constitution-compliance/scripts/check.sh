#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/constitution-compliance"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

PRINCIPLES="$SKILL_DIR/assets/constitution-v6-principles.json"
CONTRACT="$SKILL_DIR/assets/compliance-report-contract.json"
SEVERITY="$SKILL_DIR/assets/severity-policy.json"
SCRIPT="$SKILL_DIR/scripts/validate_constitution_report.py"

python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$PRINCIPLES" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$SEVERITY" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/evals/evals.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/knowledge/knowledge-graph.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/valid-pass-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/valid-blocked-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-false-pass-report.json" >/dev/null

python3 -m py_compile "$SCRIPT"

python3 -B "$SCRIPT" \
  --principles "$PRINCIPLES" \
  --contract "$CONTRACT" \
  --severity "$SEVERITY" \
  --report "$SKILL_DIR/scripts/fixtures/valid-pass-report.json" \
  --expect pass >/dev/null

python3 -B "$SCRIPT" \
  --principles "$PRINCIPLES" \
  --contract "$CONTRACT" \
  --severity "$SEVERITY" \
  --report "$SKILL_DIR/scripts/fixtures/valid-blocked-report.json" \
  --expect pass >/dev/null

python3 -B "$SCRIPT" \
  --principles "$PRINCIPLES" \
  --contract "$CONTRACT" \
  --severity "$SEVERITY" \
  --report "$SKILL_DIR/scripts/fixtures/invalid-false-pass-report.json" \
  --expect fail >/dev/null

echo "OK: constitution-compliance reports validated deterministically"
