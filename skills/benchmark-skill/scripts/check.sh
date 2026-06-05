#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/benchmark-skill"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

RUBRIC="$SKILL_DIR/assets/benchmark-rubric.json"
GATES="$SKILL_DIR/assets/gate-policy.json"
POLICY="$SKILL_DIR/assets/net-assessment-policy.json"
CONTRACT="$SKILL_DIR/assets/report-contract.json"
SCRIPT="$SKILL_DIR/scripts/validate_benchmark_report.py"

python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$RUBRIC" >/dev/null
python3 -m json.tool "$GATES" >/dev/null
python3 -m json.tool "$POLICY" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$SKILL_DIR/evals/evals.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/knowledge/knowledge-graph.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/valid-improved-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-inflated-improved-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-missing-baseline-report.json" >/dev/null

python3 -m py_compile "$SCRIPT"

python3 -B "$SCRIPT" \
  --rubric "$RUBRIC" \
  --gates "$GATES" \
  --policy "$POLICY" \
  --contract "$CONTRACT" \
  --report "$SKILL_DIR/scripts/fixtures/valid-improved-report.json" \
  --expect pass >/dev/null

python3 -B "$SCRIPT" \
  --rubric "$RUBRIC" \
  --gates "$GATES" \
  --policy "$POLICY" \
  --contract "$CONTRACT" \
  --report "$SKILL_DIR/scripts/fixtures/invalid-inflated-improved-report.json" \
  --expect fail >/dev/null

python3 -B "$SCRIPT" \
  --rubric "$RUBRIC" \
  --gates "$GATES" \
  --policy "$POLICY" \
  --contract "$CONTRACT" \
  --report "$SKILL_DIR/scripts/fixtures/invalid-missing-baseline-report.json" \
  --expect fail >/dev/null

echo "OK: benchmark-skill reports validated deterministically"
