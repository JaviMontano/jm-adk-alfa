#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/quality-gatekeeper"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

GATES="$SKILL_DIR/assets/gate-criteria.json"
CONTRACT="$SKILL_DIR/assets/report-contract.json"
EVIDENCE="$SKILL_DIR/assets/evidence-policy.json"
SCORE_SCHEMA="$SKILL_DIR/assets/score-history-schema.json"
SCRIPT="$SKILL_DIR/scripts/validate_gate_report.py"

python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$GATES" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$EVIDENCE" >/dev/null
python3 -m json.tool "$SCORE_SCHEMA" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/evals/evals.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/knowledge/knowledge-graph.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/g1-pass-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/g3-blocked-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-false-pass-report.json" >/dev/null

python3 -m py_compile "$SCRIPT"

python3 -B "$SCRIPT" \
  --gates "$GATES" \
  --contract "$CONTRACT" \
  --evidence "$EVIDENCE" \
  --score-schema "$SCORE_SCHEMA" \
  --report "$SKILL_DIR/scripts/fixtures/g1-pass-report.json" \
  --expect pass >/dev/null

python3 -B "$SCRIPT" \
  --gates "$GATES" \
  --contract "$CONTRACT" \
  --evidence "$EVIDENCE" \
  --score-schema "$SCORE_SCHEMA" \
  --report "$SKILL_DIR/scripts/fixtures/g3-blocked-report.json" \
  --expect pass >/dev/null

python3 -B "$SCRIPT" \
  --gates "$GATES" \
  --contract "$CONTRACT" \
  --evidence "$EVIDENCE" \
  --score-schema "$SCORE_SCHEMA" \
  --report "$SKILL_DIR/scripts/fixtures/invalid-false-pass-report.json" \
  --expect fail >/dev/null

echo "OK: quality-gatekeeper reports validated deterministically"
