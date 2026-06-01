#!/bin/bash
# adapt.sh v4.0.0 — Master adapter orchestrator
#
# Architecture:
#   Core (skills/, PRISTINO.md, Constitution, runtime contracts)
#     ↓ ACL boundary (acl.sh — only reader of core files)
#     ↓ Adapters (antigravity.sh, vscode.sh, cursor.sh, codex.sh)
#     ↓ Runtime mirrors and bridge outputs (AGENTS.md, GEMINI.md, .agent/, .github/, .cursorrules, etc.)
#
# Runtime mirrors are derived views where practical. If core contracts change, run this to sync.
# Anti-Corruption Layer: adapters read via acl.sh functions, never touch SKILL.md directly.

set -euo pipefail

PROJECT_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
SCRIPT_DIR="$PROJECT_ROOT/scripts"
ADAPTERS_DIR="$SCRIPT_DIR/adapters"

TARGET="${1:-all}"

run_adapter() {
  local NAME="$1"
  local SCRIPT="$ADAPTERS_DIR/$NAME.sh"
  if [ ! -f "$SCRIPT" ]; then
    echo "ERROR: Adapter not found: $NAME"
    echo "Available: antigravity, vscode, cursor, codex, all"
    return 1
  fi
  echo ""
  echo "── $NAME ──"
  bash "$SCRIPT"
}

case "$TARGET" in
  antigravity) run_adapter "antigravity" ;;
  vscode)      run_adapter "vscode" ;;
  cursor)      run_adapter "cursor" ;;
  codex)       run_adapter "codex" ;;
  all)
    echo "=== JM-ADK Adapter System v4.0.0 ==="
    echo "Core → runtime mirrors/adapters via Anti-Corruption Layer"
    run_adapter "antigravity"
    run_adapter "vscode"
    run_adapter "cursor"
    run_adapter "codex"
    echo ""
    echo "=== All adapters complete ==="
    echo "Files regenerated from canonical contracts (skills/, PRISTINO.md, runtime mirrors)"
    echo "Core files were NOT modified."
    ;;
  *)
    echo "Usage: adapt.sh [target]"
    echo ""
    echo "Targets:"
    echo "  all          Run all adapters (default)"
    echo "  antigravity  .agent/skills_index.json + .agent/rules/GEMINI.md"
    echo "  vscode       .github/copilot-instructions.md"
    echo "  cursor       .cursorrules + .windsurfrules"
    echo "  codex        AGENTS.md + GEMINI.md"
    echo ""
    echo "Architecture: Core → ACL → Adapter → IDE output"
    echo "The core (SKILL.md) is the source of truth. Everything else is derived."
    ;;
esac
