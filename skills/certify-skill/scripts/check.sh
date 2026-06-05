#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/certify-skill"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

PHASES="$SKILL_DIR/assets/certification-phases.json"
LEVEL_POLICY="$SKILL_DIR/assets/certification-level-policy.json"
CONTRACT="$SKILL_DIR/assets/report-contract.json"
EVIDENCE="$SKILL_DIR/assets/evidence-policy.json"
SCRIPT="$SKILL_DIR/scripts/validate_certification_report.py"

python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$PHASES" >/dev/null
python3 -m json.tool "$LEVEL_POLICY" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$EVIDENCE" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/evals/evals.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/knowledge/knowledge-graph.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/moat-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/conditional-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-false-certified-report.json" >/dev/null

python3 -m py_compile "$SCRIPT"

python3 -B "$SCRIPT" \
  --phases "$PHASES" \
  --level-policy "$LEVEL_POLICY" \
  --contract "$CONTRACT" \
  --evidence "$EVIDENCE" \
  --report "$SKILL_DIR/scripts/fixtures/moat-report.json" \
  --expect pass >/dev/null

python3 -B "$SCRIPT" \
  --phases "$PHASES" \
  --level-policy "$LEVEL_POLICY" \
  --contract "$CONTRACT" \
  --evidence "$EVIDENCE" \
  --report "$SKILL_DIR/scripts/fixtures/conditional-report.json" \
  --expect pass >/dev/null

python3 -B "$SCRIPT" \
  --phases "$PHASES" \
  --level-policy "$LEVEL_POLICY" \
  --contract "$CONTRACT" \
  --evidence "$EVIDENCE" \
  --report "$SKILL_DIR/scripts/fixtures/invalid-false-certified-report.json" \
  --expect fail >/dev/null

echo "OK: certify-skill reports validated deterministically"
