#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/workflow-creator"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

CONTRACT="$SKILL_DIR/assets/workflow-definition-contract.json"
SCRIPT="$SKILL_DIR/scripts/validate_workflow_spec.py"

python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/quality-gates.json" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$SKILL_DIR/evals/evals.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/knowledge/knowledge-graph.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/valid-agent-handoff-workflow.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-too-few-steps.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-vague-fields.json" >/dev/null

python3 -m py_compile "$SCRIPT"

python3 -B "$SCRIPT" \
  --contract "$CONTRACT" \
  --spec "$SKILL_DIR/scripts/fixtures/valid-agent-handoff-workflow.json" \
  --expect pass >/dev/null

python3 -B "$SCRIPT" \
  --contract "$CONTRACT" \
  --spec "$SKILL_DIR/scripts/fixtures/invalid-too-few-steps.json" \
  --expect fail >/dev/null

python3 -B "$SCRIPT" \
  --contract "$CONTRACT" \
  --spec "$SKILL_DIR/scripts/fixtures/invalid-vague-fields.json" \
  --expect fail >/dev/null

echo "OK: workflow-creator specs validated deterministically"
