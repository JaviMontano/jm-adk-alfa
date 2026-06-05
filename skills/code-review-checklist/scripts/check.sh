#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/code-review-checklist"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

SCRIPT="$SKILL_DIR/scripts/validate_code_review_checklist_report.py"
TAXONOMY="$SKILL_DIR/assets/checklist-taxonomy.json"
CONTRACT="$SKILL_DIR/assets/report-contract.json"
EVIDENCE="$SKILL_DIR/assets/evidence-policy.json"
BOUNDARY="$SKILL_DIR/assets/source-boundary-policy.json"

python3 -m json.tool "$SKILL_DIR/assets/activation-policy.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/assets/manifest.json" >/dev/null
python3 -m json.tool "$TAXONOMY" >/dev/null
python3 -m json.tool "$CONTRACT" >/dev/null
python3 -m json.tool "$EVIDENCE" >/dev/null
python3 -m json.tool "$BOUNDARY" >/dev/null
python3 -m json.tool "$SKILL_DIR/evals/evals.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/knowledge/knowledge-graph.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/valid-blocking-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/valid-clean-report.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-approve-with-blocker.json" >/dev/null
python3 -m json.tool "$SKILL_DIR/scripts/fixtures/invalid-untagged-check.json" >/dev/null

python3 -m py_compile "$SCRIPT"

python3 -B "$SCRIPT" --taxonomy "$TAXONOMY" --contract "$CONTRACT" --evidence "$EVIDENCE" --boundary "$BOUNDARY" --report "$SKILL_DIR/scripts/fixtures/valid-blocking-report.json" --expect pass >/dev/null
python3 -B "$SCRIPT" --taxonomy "$TAXONOMY" --contract "$CONTRACT" --evidence "$EVIDENCE" --boundary "$BOUNDARY" --report "$SKILL_DIR/scripts/fixtures/valid-clean-report.json" --expect pass >/dev/null
python3 -B "$SCRIPT" --taxonomy "$TAXONOMY" --contract "$CONTRACT" --evidence "$EVIDENCE" --boundary "$BOUNDARY" --report "$SKILL_DIR/scripts/fixtures/invalid-approve-with-blocker.json" --expect fail >/dev/null
python3 -B "$SCRIPT" --taxonomy "$TAXONOMY" --contract "$CONTRACT" --evidence "$EVIDENCE" --boundary "$BOUNDARY" --report "$SKILL_DIR/scripts/fixtures/invalid-untagged-check.json" --expect fail >/dev/null

echo "OK: code-review-checklist reports validated deterministically"
