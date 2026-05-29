#!/bin/bash
# acl.sh — Anti-Corruption Layer for JM-ADK
#
# Reads the canonical core format (SKILL.md, CLAUDE.md, PRISTINO.md) and exposes
# a clean API for adapters. Adapters NEVER read core files directly — they call
# these functions. This protects the core from IDE-specific concerns leaking in.
#
# Design: The core is SKILL.md YAML frontmatter + markdown. That's the source of truth.
# Everything else is a derived view. If it can't be derived from core, it doesn't exist.

# shellcheck source=/dev/null
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# ── Core readers (ACL boundary — only these touch SKILL.md files) ──

# Extract YAML frontmatter field from a SKILL.md
# Usage: acl_skill_field <skill_dir> <field> → value
acl_skill_field() {
  local SKILL_FILE="$1/SKILL.md"
  local FIELD="$2"
  [ ! -f "$SKILL_FILE" ] && return
  grep -A1 "^${FIELD}:" "$SKILL_FILE" | head -1 | sed "s/^${FIELD}:[[:space:]]*//" | sed 's/^["\x27]//;s/["\x27]$//' | sed 's/^>//' | tr -s ' '
}

# Extract multi-line description (handles YAML > continuation)
acl_skill_description() {
  local SKILL_FILE="$1/SKILL.md"
  [ ! -f "$SKILL_FILE" ] && return
  # Try single-line first
  local DESC
  DESC=$(sed -n '/^description:/,/^[a-z]/{/^description:/d;/^[a-z]/d;p}' "$SKILL_FILE" | tr '\n' ' ' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | head -c 300)
  [ -z "$DESC" ] && DESC=$(grep "^description:" "$SKILL_FILE" | sed 's/^description:[[:space:]]*//' | sed 's/^>//')
  echo "$DESC" | tr -s ' '
}

# List all skill directories (canonical source)
acl_list_skills() {
  for dir in "$PROJECT_ROOT/skills"/*/; do
    [ -f "$dir/SKILL.md" ] && basename "$dir"
  done
}

# Count components from canonical sources
acl_count_skills() { find "$PROJECT_ROOT/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' '; }
acl_count_agents() { find "$PROJECT_ROOT/agents" -name "*.md" 2>/dev/null | wc -l | tr -d ' '; }
acl_count_commands() { find "$PROJECT_ROOT/commands" -name "*.md" 2>/dev/null | wc -l | tr -d ' '; }
acl_count_prompts() { find "$PROJECT_ROOT/prompts" -name "*.md" -not -path "*/.catalog/*" 2>/dev/null | wc -l | tr -d ' '; }

# Read version from plugin.json
acl_version() {
  grep '"version"' "$PROJECT_ROOT/.claude-plugin/plugin.json" | head -1 | sed 's/.*"version"[[:space:]]*:[[:space:]]*"//' | sed 's/".*//'
}

# Read Constitution version
acl_constitution_version() {
  local LATEST
  LATEST=$(ls "$PROJECT_ROOT/references/ontology/constitution-v"*.md 2>/dev/null | sort -V | tail -1)
  [ -n "$LATEST" ] && basename "$LATEST" .md | sed 's/constitution-//' || echo "unknown"
}

# Extract allowed-tools from a skill
acl_skill_tools() {
  local SKILL_FILE="$1/SKILL.md"
  [ ! -f "$SKILL_FILE" ] && return
  sed -n '/^allowed-tools:/,/^[a-z]/{/^allowed-tools:/d;/^[a-z]/d;s/^[[:space:]]*-[[:space:]]*//;p}' "$SKILL_FILE" | tr '\n' ',' | sed 's/,$//'
}

# Read core rules from CLAUDE.md (IDE-agnostic extraction)
acl_core_rules() {
  awk '/^## Core Rules$/,/^## [^C]/' "$PROJECT_ROOT/CLAUDE.md" | grep -E '^[0-9]+\.' | sed 's/\*\*//g'
}

# Read brand tokens
acl_brand_palette() {
  grep -o '"[a-z]*"[[:space:]]*:[[:space:]]*"#[A-Fa-f0-9]*"' "$PROJECT_ROOT/references/brand/design-tokens.json" 2>/dev/null | \
    sed 's/"//g;s/[[:space:]]*:[[:space:]]*/ /' || echo "navy #0A122A gold #FFD700 cyan #137DC5"
}

# Read quality gates summary
acl_quality_gates() {
  echo "G0 (pre-flight) → G1 (post-spec) → G2 (post-plan) → G3 (deploy-ready)"
}

export -f acl_skill_field acl_skill_description acl_list_skills acl_count_skills acl_count_agents acl_count_commands acl_count_prompts acl_version acl_constitution_version acl_skill_tools acl_core_rules acl_brand_palette acl_quality_gates 2>/dev/null || true
