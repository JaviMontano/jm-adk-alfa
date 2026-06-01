#!/bin/bash
# session-init.sh v4.0.0 — SessionStart hook
#
# Emits structured KEY: VALUE lines for model consumption. Read-only: never writes to disk.
# Always exits 0 (a failing SessionStart hook blocks the entire session).

PROJECT_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
TODAY=$(date +%Y-%m-%d)

# ── System integrity (existence checks only — fast) ──

P="false"; C="false"; I="false"; H="false"
[ -f "$PROJECT_ROOT/PRISTINO.md" ] && P="true"
[ -f "$PROJECT_ROOT/references/ontology/constitution-v6.0.0.md" ] && C="true"
[ -f "$PROJECT_ROOT/PRISTINO-INDEX.md" ] && I="true"
[ -f "$PROJECT_ROOT/hooks/hooks.json" ] && H="true"

SK=$(find "$PROJECT_ROOT/skills" -mindepth 2 -maxdepth 2 -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
AG=$(find "$PROJECT_ROOT/agents" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
CM=$(find "$PROJECT_ROOT/commands" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
PR=$(find "$PROJECT_ROOT/prompts" -mindepth 2 -maxdepth 2 -name "*.md" -not -path "*/.catalog/*" 2>/dev/null | wc -l | tr -d ' ')

DEGRADED=""
[ "$P" = "false" ] && DEGRADED="${DEGRADED}PRISTINO "
[ "$C" = "false" ] && DEGRADED="${DEGRADED}Constitution "
[ "$I" = "false" ] && DEGRADED="${DEGRADED}Index "

# ── Workspace state ──

WS="disabled"
WS_ID=""
WS_STALE="false"
WS_COUNT=0

if [ -f "$PROJECT_ROOT/.jm-adk.json" ]; then
  REG="$PROJECT_ROOT/workspace/.workspace-registry.json"
  if [ -f "$REG" ]; then
    WS_ID=$(grep -o '"activeWorkspace"[[:space:]]*:[[:space:]]*"[^"]*"' "$REG" 2>/dev/null | \
      sed 's/.*"activeWorkspace"[[:space:]]*:[[:space:]]*"//' | sed 's/"//') || true

    if [ -n "$WS_ID" ] && [ "$WS_ID" != "null" ]; then
      if [ -d "$PROJECT_ROOT/workspace/$WS_ID" ]; then
        WS="active"
        WD=$(echo "$WS_ID" | grep -o '^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
        [ -n "$WD" ] && [ "$WD" != "$TODAY" ] && WS_STALE="true"
      else
        WS="orphaned"
      fi
    else
      WS="idle"
      WS_ID=""
    fi

    for d in "$PROJECT_ROOT/workspace"/20*/; do
      [ -d "$d" ] && [ -f "$d/.workspace.json" ] && \
        grep -q '"status": "active"' "$d/.workspace.json" 2>/dev/null && WS_COUNT=$((WS_COUNT + 1))
    done
  else
    WS="no-registry"
  fi
fi

# ── Governance ──

PL=$(find "$PROJECT_ROOT/.specify/plans" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
AD=$(find "$PROJECT_ROOT/.specify/adr" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

# ── Output (model-parseable) ──

echo "VERSION: 5.2.0"
echo "SYSTEM: PRISTINO=$P CONSTITUTION=$C INDEX=$I HOOKS=$H"
echo "COMPONENTS: $SK skills, $AG agents, $CM commands, $PR prompts"
echo "GOVERNANCE: $PL plans, $AD ADRs"
[ -n "$DEGRADED" ] && echo "DEGRADED: $DEGRADED"
echo "WORKSPACE: $WS"
[ -n "$WS_ID" ] && echo "WORKSPACE-ID: $WS_ID"
echo "WORKSPACE-STALE: $WS_STALE"
echo "WORKSPACE-ACTIVE-COUNT: $WS_COUNT"
echo "---"
echo "MetodologIA · JM Labs"
