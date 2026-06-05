#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SKILL_DIR="$ROOT/skills/agent-constitution-creator"
SCRIPT="$SKILL_DIR/scripts/validate_agent_constitution.py"
SCHEMA="$SKILL_DIR/assets/agent-constitution-schema.json"
REGISTRY="Read,Grep,Glob"

python3 -B "$SCRIPT" --schema "$SCHEMA" --constitution "$SKILL_DIR/scripts/fixtures/valid-constitution.md" --tool-registry "$REGISTRY" --expect pass >/dev/null
python3 -B "$SCRIPT" --schema "$SCHEMA" --constitution "$SKILL_DIR/scripts/fixtures/invalid-missing-section.md" --tool-registry "$REGISTRY" --expect fail >/dev/null
python3 -B "$SCRIPT" --schema "$SCHEMA" --constitution "$SKILL_DIR/scripts/fixtures/invalid-overbroad-authority.md" --tool-registry "$REGISTRY" --expect fail >/dev/null
python3 -B "$SCRIPT" --schema "$SCHEMA" --constitution "$SKILL_DIR/scripts/fixtures/invalid-missing-evidence.md" --tool-registry "$REGISTRY" --expect fail >/dev/null

echo "OK: agent-constitution-creator validator fixtures passed"
