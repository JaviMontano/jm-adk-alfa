#!/bin/bash
# user-prompt-filter.sh v4.0.0 — UserPromptSubmit hook
#
# Injection detection (stderr warnings) + workspace signal (stdout).
# Always exits 0: blocking user input is worse than any false positive.
# Pattern matching is intentionally basic — sophisticated attacks are the model's concern.

PROMPT="${CLAUDE_USER_PROMPT:-}"
PROJECT_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"

# ── Injection patterns (warn, never block) ──

for P in "ignore previous instructions" "ignore all instructions" "you are now" \
         "disregard your" "forget everything" "new persona" "jailbreak" "DAN mode" \
         "system prompt" "reveal your instructions" "act as if" "pretend you are"; do
  echo "$PROMPT" | grep -qi "$P" && echo "INJECTION-WARNING: '$P'" >&2
done

# ── Workspace signal ──

if [ -f "$PROJECT_ROOT/.jm-adk.json" ]; then
  REG="$PROJECT_ROOT/workspace/.workspace-registry.json"
  if [ -f "$REG" ]; then
    A=$(grep -o '"activeWorkspace"[[:space:]]*:[[:space:]]*"[^"]*"' "$REG" 2>/dev/null | \
      sed 's/.*"activeWorkspace"[[:space:]]*:[[:space:]]*"//' | sed 's/"//') || true
    if [ -z "$A" ] || [ "$A" = "null" ]; then
      echo "WORKSPACE-SIGNAL: no-active-workspace"
    elif [ ! -d "$PROJECT_ROOT/workspace/$A" ]; then
      echo "WORKSPACE-SIGNAL: orphaned ($A)"
    fi
  else
    echo "WORKSPACE-SIGNAL: no-registry"
  fi
fi

exit 0
