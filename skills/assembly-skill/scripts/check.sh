#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/assembly-skill"
SCRIPT="$SKILL_DIR/scripts/validate_assembly_contract.py"
CONTRACT="$SKILL_DIR/assets/assembly-report-contract.json"
POLICY="$SKILL_DIR/assets/mode-policy.json"

python3 -B "$SCRIPT" --contract "$CONTRACT" --report "$SKILL_DIR/scripts/fixtures/valid-standard-report.md" --mode standard --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --report "$SKILL_DIR/scripts/fixtures/valid-quick-report.md" --mode quick --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --report "$SKILL_DIR/scripts/fixtures/invalid-premature-certified.md" --mode standard --expect fail >/dev/null
python3 -B "$SCRIPT" --policy "$POLICY" --scorecard "$SKILL_DIR/scripts/fixtures/scorecard-polish.json" --expect-mode deep --expect pass >/dev/null
python3 -B "$SCRIPT" --policy "$POLICY" --scorecard "$SKILL_DIR/scripts/fixtures/scorecard-certified.json" --expect-mode quick --expect pass >/dev/null
python3 -B "$SCRIPT" --policy "$POLICY" --scorecard "$SKILL_DIR/scripts/fixtures/scorecard-blocked.json" --expect-mode standard --expect pass >/dev/null

echo "OK: assembly-skill contracts validated"
