#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$SKILL_DIR/scripts/validate_dsvsr_packet.py"
CONTRACT="$SKILL_DIR/assets/dsvsr-packet-contract.json"

python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-full-dsvsr-packet.md" --scenario full-dsvsr --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-missing-context-packet.md" --scenario missing-context --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-low-confidence-packet.md" --scenario low-confidence --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/valid-false-positive-packet.md" --scenario false-positive --expect pass >/dev/null
python3 -B "$SCRIPT" --contract "$CONTRACT" --packet "$SKILL_DIR/scripts/fixtures/invalid-no-verify-packet.md" --scenario invalid-no-verify --expect fail >/dev/null

echo "OK: task-engine DSVSR packets validated"
