#!/bin/bash
# workspace-manager.sh v4.0.0 — Single CRUD entry point for workspace operations
#
# Design: No jq dependency (portability). Flat JSON only (schema-controlled here).
#   Hooks and model both call this script → single write path → no state divergence.
#   Concurrent writes unsafe (acceptable: Claude Code is single-threaded per session).
#   sed-based JSON is fragile for nested structures, but workspace JSON is flat by design.
#
# Limits: slug ≤40 chars | ≤99 same-slug/day | maxActive enforced by caller (CLAUDE.md)

set -euo pipefail

PROJECT_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
WS_ROOT="$PROJECT_ROOT/workspace"
REGISTRY="$WS_ROOT/.workspace-registry.json"
TODAY=$(date +%Y-%m-%d)
NOW_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
NOW_TIME=$(date +"%H:%M")
ACTION="${1:-help}"

# Canonical naming (single source of truth). Provides slugify().
# shellcheck disable=SC1091
[ -f "$(dirname "$0")/lib/naming.sh" ] && . "$(dirname "$0")/lib/naming.sh"

# ── Helpers ──

ensure_registry() {
  mkdir -p "$WS_ROOT" "$WS_ROOT/archive"
  if [ ! -f "$REGISTRY" ] || ! grep -q '"activeWorkspace"' "$REGISTRY" 2>/dev/null; then
    write_registry "" "null" 0 0
  fi
}

# Portable JSON field reader. Usage: json_field file key → value (without quotes)
json_field() {
  grep -o "\"$2\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$1" 2>/dev/null | head -1 | \
    sed "s/.*\"$2\"[[:space:]]*:[[:space:]]*\"//" | sed 's/".*//' || true
}

# Portable JSON numeric field. Usage: json_num file key → integer
json_num() {
  local VAL
  VAL=$(grep -o "\"$2\"[[:space:]]*:[[:space:]]*[0-9]*" "$1" 2>/dev/null | \
    tr -d '[:space:]' | grep -o '[0-9]*$' || echo "0")
  echo "${VAL:-0}"
}

# slugify() comes from lib/naming.sh when sourced. Fallback kept for resilience
# if the lib is missing (degraded but functional).
if ! type slugify >/dev/null 2>&1; then
  slugify() {
    local SLUG
    SLUG=$(echo "$1" | tr '[:upper:]' '[:lower:]' | \
      sed 's/[áàäâã]/a/g; s/[éèëê]/e/g; s/[íìïî]/i/g; s/[óòöôõ]/o/g; s/[úùüû]/u/g; s/ñ/n/g; s/ç/c/g' | \
      sed 's/[^a-z0-9]/-/g; s/--*/-/g; s/^-//; s/-$//' | cut -c1-40)
    echo "${SLUG:-unnamed}"
  }
fi

get_active() {
  [ ! -f "$REGISTRY" ] && echo "" && return
  local A; A=$(json_field "$REGISTRY" "activeWorkspace"); echo "${A:-}"
}

count_active() {
  local N=0
  for d in "$WS_ROOT"/20*/; do
    [ -d "$d" ] && [ -f "$d/.workspace.json" ] && \
      grep -q '"status": "active"' "$d/.workspace.json" 2>/dev/null && N=$((N + 1))
  done
  echo "$N"
}

# Rewrite registry from scratch. Safer than sed-patching JSON.
write_registry() {
  local ENTRIES="$1" ACTIVE="$2" TOTAL="$3" ARCHIVED="$4"
  if [ "$ACTIVE" = "null" ]; then
    cat > "$REGISTRY" << EOF
{
  "workspaces": [${ENTRIES}],
  "activeWorkspace": null,
  "totalCreated": ${TOTAL},
  "totalArchived": ${ARCHIVED}
}
EOF
  else
    cat > "$REGISTRY" << EOF
{
  "workspaces": [${ENTRIES}],
  "activeWorkspace": "${ACTIVE}",
  "totalCreated": ${TOTAL},
  "totalArchived": ${ARCHIVED}
}
EOF
  fi
}

require_active() {
  local A; A=$(get_active)
  if [ -z "$A" ] || [ "$A" = "null" ]; then
    echo "ERROR: No active workspace"; return 1
  fi
  echo "$A"
}

require_dir() {
  [ -d "$WS_ROOT/$1" ] && return 0
  echo "ERROR: Workspace not found: $1 (run: workspace-manager.sh list)"
  return 1
}

# Gate ordering for regression guard
gate_ordinal() {
  case "$1" in G0) echo 0;; G1) echo 1;; G2) echo 2;; G3) echo 3;; *) echo -1;; esac
}

# ── Commands ──

cmd_create() {
  local RAW="${2:-unnamed}"
  local SLUG; SLUG=$(slugify "$RAW")
  local ID="$TODAY-$SLUG"

  if [ -d "$WS_ROOT/$ID" ]; then
    local C=2
    while [ -d "$WS_ROOT/$TODAY-$SLUG-$C" ]; do
      C=$((C + 1)); [ "$C" -gt 99 ] && { echo "ERROR: >99 workspaces with slug '$SLUG' today"; return 1; }
    done
    ID="$TODAY-$SLUG-$C"
  fi

  ensure_registry
  local DIR="$WS_ROOT/$ID"
  mkdir -p "$DIR/artifacts"

  # Escape double quotes in title for JSON safety
  local SAFE_TITLE; SAFE_TITLE=$(echo "$RAW" | sed 's/"/\\"/g')

  cat > "$DIR/.workspace.json" << WSJSON
{
  "schema": 1,
  "id": "$ID",
  "title": "$SAFE_TITLE",
  "slug": "$SLUG",
  "created": "$NOW_ISO",
  "updated": "$NOW_ISO",
  "status": "active",
  "tags": [],
  "triad": {"lead": null, "support": null, "guardian": "quality-guardian"},
  "metrics": {"toolCalls": 0, "filesCreated": 0, "filesModified": 0, "qualityGate": "G0", "errors": 0}
}
WSJSON

  cat > "$DIR/tasklog.md" << TASKLOG
# Tasklog: $RAW

| Field | Value |
|-------|-------|
| Workspace | \`$ID\` |
| Created | $TODAY $NOW_TIME |
| Status | active |

---

## Actions

### $NOW_TIME — Workspace created
- Task: $RAW
- Gate: G0 (pre-flight)
TASKLOG

  cat > "$DIR/changelog.md" << CHANGELOG
# Changelog: $RAW

> Workspace: \`$ID\` | Format: [Keep a Changelog](https://keepachangelog.com/)

## [0.1.0] — $TODAY

### Added
- Workspace initialized for: $RAW
CHANGELOG

  cat > "$DIR/plan.md" << PLAN
# Plan: $RAW

| Field | Value |
|-------|-------|
| Workspace | \`$ID\` |
| Created | $TODAY |
| Status | draft |

## Objective

(Pristino fills after analyzing request)

## Scope

### In Scope
- (pending)

### Out of Scope
- (pending)

### Assumptions
- (tag each \`[ASSUMPTION]\`)

## Tasks

- [ ] (pending)

## Acceptance Criteria

- [ ] (derived from objective)

## Quality Gates

- [ ] G0: Pre-flight — secrets scan, Constitution compliance
- [ ] G1: Post-spec — requirements complete, acceptance criteria, evidence tags
- [ ] G2: Post-plan — architecture documented, tests written
- [ ] G3: Deploy-ready — all tests pass, Lighthouse ≥ 90, a11y + security clean

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| (pending) | — | — |
PLAN

  # Rebuild registry with new entry
  local OLD_TOTAL; OLD_TOTAL=$(json_num "$REGISTRY" "totalCreated")
  local OLD_ARCHIVED; OLD_ARCHIVED=$(json_num "$REGISTRY" "totalArchived")
  local NEW_TOTAL=$((OLD_TOTAL + 1))

  # Collect existing entries
  local ENTRIES=""
  for d in "$WS_ROOT"/20*/; do
    [ -d "$d" ] || continue
    local M="$d/.workspace.json"
    [ -f "$M" ] || continue
    local EID; EID=$(json_field "$M" "id")
    local EST; EST=$(json_field "$M" "status")
    local ECR; ECR=$(json_field "$M" "created")
    local ETI; ETI=$(json_field "$M" "title")
    [ -n "$ENTRIES" ] && ENTRIES="$ENTRIES,"
    ENTRIES="${ENTRIES}{\"id\":\"$EID\",\"status\":\"$EST\",\"created\":\"$ECR\",\"title\":\"$(echo "$ETI" | sed 's/"/\\"/g')\"}"
  done

  write_registry "$ENTRIES" "$ID" "$NEW_TOTAL" "$OLD_ARCHIVED"

  echo "WORKSPACE-CREATED: $ID"
  echo "PATH: $DIR"
  echo "ACTIVE-COUNT: $(count_active)"
}

cmd_ensure() {
  # Idempotent: reuse the active workspace if one exists, else create.
  # Used by the placement guard's deny→create→retry loop so the model never
  # has to branch on "is there an active workspace?" — it just calls ensure.
  ensure_registry
  local A; A=$(get_active)
  if [ -n "$A" ] && [ "$A" != "null" ] && [ -d "$WS_ROOT/$A" ]; then
    echo "WORKSPACE-ACTIVE: $A"
    echo "PATH: $WS_ROOT/$A"
    return 0
  fi
  cmd_create "create" "${2:-unnamed}"
}

cmd_status() {
  ensure_registry
  local A; A=$(get_active)
  if [ -z "$A" ] || [ "$A" = "null" ]; then
    echo "STATUS: no-active-workspace"
    return
  fi

  if [ ! -d "$WS_ROOT/$A" ]; then
    echo "STATUS: orphaned ($A — directory missing, clearing pointer)"
    write_registry "" "null" "$(json_num "$REGISTRY" "totalCreated")" "$(json_num "$REGISTRY" "totalArchived")"
    return
  fi

  local M="$WS_ROOT/$A/.workspace.json"
  echo "STATUS: active"
  echo "WORKSPACE: $A"
  echo "PATH: $WS_ROOT/$A"

  local WS_DATE; WS_DATE=$(echo "$A" | grep -o '^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
  [ "$WS_DATE" != "$TODAY" ] && echo "STALE: true ($WS_DATE)" || echo "STALE: false"

  if [ -f "$M" ]; then
    echo "TOOL-CALLS: $(json_num "$M" "toolCalls")"
    echo "QUALITY-GATE: $(json_field "$M" "qualityGate")"
  fi
  echo "ACTIVE-COUNT: $(count_active)"
}

cmd_list() {
  ensure_registry
  local A; A=$(get_active)
  local N=0

  echo "=== JM-ADK Workspaces ==="
  echo ""
  for d in "$WS_ROOT"/20*/; do
    [ -d "$d" ] || continue
    local NAME; NAME=$(basename "$d")
    local M="$d/.workspace.json"
    local ST="?"; local GT="?"
    [ -f "$M" ] && ST=$(json_field "$M" "status") && GT=$(json_field "$M" "qualityGate")
    local MK=""; [ "$NAME" = "$A" ] && MK=" ← active"
    echo "  $NAME [${ST:-?}] ${GT:-?}${MK}"
    N=$((N + 1))
  done

  local AR=0
  for d in "$WS_ROOT/archive"/20*/; do [ -d "$d" ] && AR=$((AR + 1)); done

  [ "$N" -eq 0 ] && echo "  (none)"
  echo ""
  echo "Total: $N workspace(s), $AR archived"
}

cmd_complete() {
  local ID="${2:-}"
  [ -z "$ID" ] && ID=$(require_active) || true
  [ -z "$ID" ] && return 1
  require_dir "$ID" || return 1

  local M="$WS_ROOT/$ID/.workspace.json"
  if grep -q '"status": "completed"' "$M" 2>/dev/null; then
    echo "ALREADY-COMPLETED: $ID"; return 0
  fi

  sed 's/"status": "active"/"status": "completed"/' "$M" > "$M.tmp" && mv "$M.tmp" "$M"
  sed "s/\"updated\": \"[^\"]*\"/\"updated\": \"$NOW_ISO\"/" "$M" > "$M.tmp" && mv "$M.tmp" "$M"

  local TL="$WS_ROOT/$ID/tasklog.md"
  if [ -f "$TL" ]; then
    local CALLS; CALLS=$(json_num "$M" "toolCalls")
    local GATE; GATE=$(json_field "$M" "qualityGate")
    printf "\n---\n\n### %s — Workspace completed\n- Tool calls: %s\n- Final gate: %s\n" \
      "$NOW_TIME" "${CALLS:-0}" "${GATE:-G0}" >> "$TL"
  fi

  local CUR; CUR=$(get_active)
  [ "$CUR" = "$ID" ] && { sed "s/\"activeWorkspace\": \"$ID\"/\"activeWorkspace\": null/" "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"; }

  echo "WORKSPACE-COMPLETED: $ID"
}

cmd_archive() {
  local ID="${2:-}"
  [ -z "$ID" ] && { echo "ERROR: Specify workspace ID (run: list)"; return 1; }
  require_dir "$ID" || return 1

  local CUR; CUR=$(get_active)
  [ "$CUR" = "$ID" ] && { echo "ERROR: Complete active workspace first: workspace-manager.sh complete"; return 1; }
  [ -d "$WS_ROOT/archive/$ID" ] && { echo "ERROR: Archive already contains $ID"; return 1; }

  mv "$WS_ROOT/$ID" "$WS_ROOT/archive/$ID"

  local AR; AR=$(json_num "$REGISTRY" "totalArchived")
  AR=$((AR + 1))
  sed "s/\"totalArchived\": *[0-9]*/\"totalArchived\": $AR/" "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"

  echo "WORKSPACE-ARCHIVED: $ID → archive/$ID"
}

cmd_switch() {
  local ID="${2:-}"
  [ -z "$ID" ] && { echo "ERROR: Specify workspace ID (run: list)"; return 1; }
  require_dir "$ID" || return 1

  local M="$WS_ROOT/$ID/.workspace.json"
  grep -q '"status": "completed"' "$M" 2>/dev/null && { echo "ERROR: Cannot switch to completed workspace. Use reopen."; return 1; }

  ensure_registry
  local PREV; PREV=$(get_active)
  if [ -n "$PREV" ] && [ "$PREV" != "null" ]; then
    sed "s/\"activeWorkspace\": \"$PREV\"/\"activeWorkspace\": \"$ID\"/" "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
  else
    sed "s/\"activeWorkspace\":null/\"activeWorkspace\": \"$ID\"/" "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
    # Handle both null (no quotes) and "null" formats
    sed "s/\"activeWorkspace\": null/\"activeWorkspace\": \"$ID\"/" "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
  fi

  echo "WORKSPACE-SWITCHED: $ID (previous: ${PREV:-none})"
}

cmd_reopen() {
  local ID="${2:-}"
  [ -z "$ID" ] && { echo "ERROR: Specify completed workspace ID to reopen"; return 1; }
  require_dir "$ID" || return 1

  local M="$WS_ROOT/$ID/.workspace.json"
  if ! grep -q '"status": "completed"' "$M" 2>/dev/null; then
    echo "ERROR: Workspace $ID is not completed (current status: $(json_field "$M" "status"))"
    return 1
  fi

  sed 's/"status": "completed"/"status": "active"/' "$M" > "$M.tmp" && mv "$M.tmp" "$M"
  sed "s/\"updated\": \"[^\"]*\"/\"updated\": \"$NOW_ISO\"/" "$M" > "$M.tmp" && mv "$M.tmp" "$M"

  # Set as active
  cmd_switch "switch" "$ID" 2>/dev/null

  local TL="$WS_ROOT/$ID/tasklog.md"
  [ -f "$TL" ] && printf "\n### %s — Workspace reopened\n" "$NOW_TIME" >> "$TL"

  echo "WORKSPACE-REOPENED: $ID"
}

cmd_log() {
  local TOOL="${2:-unknown}" INPUT="${3:-}"
  local A; A=$(get_active)
  [ -z "$A" ] || [ "$A" = "null" ] && return 0

  local TL="$WS_ROOT/$A/tasklog.md"
  [ ! -f "$TL" ] && return 0

  {
    echo ""
    echo "### $NOW_TIME — $TOOL"
    [ -n "$INPUT" ] && echo "- Input: \`$(echo "$INPUT" | head -c 120 | tr '\n' ' ')\`"
  } >> "$TL"

  # Increment counter
  local M="$WS_ROOT/$A/.workspace.json"
  if [ -f "$M" ]; then
    local C; C=$(json_num "$M" "toolCalls")
    sed "s/\"toolCalls\": $C/\"toolCalls\": $((C + 1))/" "$M" > "$M.tmp" && mv "$M.tmp" "$M" 2>/dev/null
  fi
}

cmd_gate() {
  local NEW="${2:-}"
  case "$NEW" in G0|G1|G2|G3) ;; *) echo "ERROR: Gate must be G0, G1, G2, or G3"; return 1;; esac

  local A; A=$(require_active) || return 1
  local M="$WS_ROOT/$A/.workspace.json"
  [ ! -f "$M" ] && { echo "ERROR: Metadata missing for $A"; return 1; }

  local OLD; OLD=$(json_field "$M" "qualityGate")
  OLD="${OLD:-G0}"

  # Regression guard: gates are sequential, no going backwards
  local OLD_N; OLD_N=$(gate_ordinal "$OLD")
  local NEW_N; NEW_N=$(gate_ordinal "$NEW")
  if [ "$NEW_N" -lt "$OLD_N" ]; then
    echo "ERROR: Gate regression not allowed ($OLD → $NEW). Gates are sequential: G0 → G1 → G2 → G3."
    return 1
  fi
  if [ "$NEW_N" -eq "$OLD_N" ]; then
    echo "ALREADY-AT: $NEW"; return 0
  fi

  sed "s/\"qualityGate\": \"$OLD\"/\"qualityGate\": \"$NEW\"/" "$M" > "$M.tmp" && mv "$M.tmp" "$M"
  cmd_log "QualityGate" "$OLD → $NEW"
  echo "GATE-UPDATED: $OLD → $NEW (workspace: $A)"
}

cmd_report() {
  local ID="${2:-}"
  [ -z "$ID" ] && ID=$(require_active) || true
  [ -z "$ID" ] && return 1
  require_dir "$ID" || return 1

  local M="$WS_ROOT/$ID/.workspace.json"
  echo "=== Workspace Report: $ID ==="
  echo ""

  if [ -f "$M" ]; then
    echo "Title:   $(json_field "$M" "title")"
    echo "Status:  $(json_field "$M" "status")"
    echo "Created: $(json_field "$M" "created")"
    echo "Updated: $(json_field "$M" "updated")"
    echo "Gate:    $(json_field "$M" "qualityGate")"
    echo "Tools:   $(json_num "$M" "toolCalls") calls"
    echo "Errors:  $(json_num "$M" "errors")"
  fi

  local AC=0
  [ -d "$WS_ROOT/$ID/artifacts" ] && AC=$(find "$WS_ROOT/$ID/artifacts" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "Artifacts: $AC file(s)"

  [ -f "$WS_ROOT/$ID/tasklog.md" ] && echo "Actions: $(grep -c '^### ' "$WS_ROOT/$ID/tasklog.md" 2>/dev/null || echo 0) logged"
}

cmd_help() {
  cat << 'HELP'
JM-ADK Workspace Manager v4.0.0

Usage: workspace-manager.sh <command> [args]

CRUD:
  create <name>       Create workspace (YYYY-MM-DD-slug). Deduplicates.
  ensure <name>       Reuse active workspace if any, else create. Idempotent.
  status              Active workspace info, metrics, staleness.
  list                All workspaces with status + gate.
  complete [id]       Mark completed (default: active). Writes stats to tasklog.
  archive <id>        Move completed workspace to archive/.
  switch <id>         Change active (target must be status=active).
  reopen <id>         Reactivate a completed workspace.

Tracking:
  log <tool> [input]  Append to active tasklog + increment counter.
  gate <G0-G3>        Advance quality gate (sequential only, no regression).
  report [id]         Metrics summary (default: active).

  help                This message.
HELP
}

# ── Router ──

case "$ACTION" in
  create)   cmd_create "$@" ;;
  ensure)   cmd_ensure "$@" ;;
  status)   cmd_status ;;
  list)     cmd_list ;;
  complete) cmd_complete "$@" ;;
  archive)  cmd_archive "$@" ;;
  switch)   cmd_switch "$@" ;;
  reopen)   cmd_reopen "$@" ;;
  log)      cmd_log "$@" ;;
  gate)     cmd_gate "$@" ;;
  report)   cmd_report "$@" ;;
  help|*)   cmd_help ;;
esac
