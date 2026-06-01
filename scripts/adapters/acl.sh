#!/bin/bash
# acl.sh — Anti-Corruption Layer for JM-ADK
#
# Reads canonical skill/runtime-contract sources and exposes
# a clean API for adapters. Adapters NEVER read core files directly — they call
# these functions. This protects the core from IDE-specific concerns leaking in.
#
# Design: skills/ and Pristino contracts are the source of truth. Runtime
# mirrors stay homologated through shared ACL sections.

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

# Read core rules from the homologated CLAUDE mirror (IDE-agnostic extraction)
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

acl_input_tolerance() {
  cat <<'EOF'
- Typos: fuzzy-match intent, never correct the user's spelling.
- Voice or rough transcription: strip filler, handle phonetic spelling, and preserve intent.
- Dyslexia: prefer short sentences, clear bullets, and stable structure.
- Multilingual: respond in the user's language unless the deliverable requires another language.
EOF
}

acl_sequential_triad() {
  cat <<'EOF'
- Lead: produce the primary domain answer or implementation.
- Support: review for security, accessibility, maintainability, and cross-cutting risks.
- Guardian: validate evidence, Constitution compliance, quality gates, and residual assumptions.
- If the runtime has no subagent tool, apply the three perspectives in one response.
EOF
}

acl_request_classification() {
  cat <<'EOF'
| Type | Action |
|------|--------|
| QUESTION | Direct answer with evidence tags when making claims |
| ANALYSIS | Discovery first, then concise report |
| SIMPLE CODE | Read before write, make the smallest safe edit |
| COMPLEX CODE | Plan, then implement, then verify |
| DESIGN/UI | Use brand tokens, accessibility, and validation |
| SCAFFOLD | Dry-run or preview first, then apply only when intended |
| DEPLOY | Build, validate, then deploy or provide deploy-ready output |
EOF
}

acl_runtime_context_contract() {
  cat <<'EOF'
- Confirm repo identity before edits; if Alfa is not confirmed, report `Dato requerido` and do not edit.
- Run `python3 scripts/diagnose-first-use.py --dry-run` for first-use or cold-start diagnosis.
- Run `python3 scripts/diagnose-user-context.py --dry-run` before relying on durable user context.
- Run `python3 scripts/diagnose-personal-skills.py --dry-run` before relying on personal skills.
- Treat `user-context/` as the in-kit context repo because `user-context/.jm-adk-context.json` declares `jm-adk-user-context`; private files do not define the role.
- Read `user-context/_INDICE.md` first, then only task-relevant context files; never bulk-load `user-context/sources/` or `user-context/resources/`.
- Treat `user-context/resources/` as private curated resources and open only indexed, task-relevant items.
- Treat `user-context/personal-skills/skills/` as the canonical private source for user-authored skills; never store them in root `skills/`.
- Create or improve personal skills with `python3 scripts/scaffold-skill.py --personal`; sync copies with `python3 scripts/sync-personal-skills.py --dry-run` before `--apply`.
- Keep `.local/skills/` as an ignored experiment or mirror cache, not durable source.
- Write to `user-context/` only after an explicit remember/update-context instruction from the user; hook-enabled writes require `JM_ADK_CONTEXT_WRITE=1`.
- Put task artifacts in `workspace/{active}/artifacts/`; never mix workspace runtime state, kit internals, durable context, and personal skill mirrors.
- Do not commit private state: `.jm-adk.local.json`, `.env*`, `.local/`, `.codex/`, `workspace/`, or private `user-context/` content.
EOF
}

export -f acl_skill_field acl_skill_description acl_list_skills acl_count_skills acl_count_agents acl_count_commands acl_count_prompts acl_version acl_constitution_version acl_skill_tools acl_core_rules acl_brand_palette acl_quality_gates acl_input_tolerance acl_sequential_triad acl_request_classification acl_runtime_context_contract 2>/dev/null || true
