#!/bin/bash
# antigravity.sh — Adapter: Core → Antigravity Kit (.agent/)
#
# Reads from canonical skills/ via ACL. Writes to .agent/ structure.
# Never modifies core files. Antigravity is a derived view.
#
# What it produces:
#   .agent/skills_index.json    — regenerated from skills/ frontmatter
#   .agent/skills/              — symlinked to root skills/ (not copied)
#   .agent/rules/GEMINI.md      — regenerated from PRISTINO.md + environment protocol
#   .agent/ARCHITECTURE.md      — regenerated with current counts

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$SCRIPT_DIR/acl.sh"

AGENT_DIR="$PROJECT_ROOT/.agent"
VERSION=$(acl_version)
SKILLS_COUNT=$(acl_count_skills)
AGENTS_COUNT=$(acl_count_agents)
COMMANDS_COUNT=$(acl_count_commands)
CONSTITUTION=$(acl_constitution_version)

echo "Adapter: Core → Antigravity"

# 1. Regenerate skills_index.json via existing Python script (it reads from skills/)
if [ -f "$AGENT_DIR/scripts/generate_index.py" ]; then
  python3 "$AGENT_DIR/scripts/generate_index.py" \
    --skills-dir "$PROJECT_ROOT/skills" \
    --output "$AGENT_DIR/skills_index.json" 2>&1 | sed 's/^/  /'
else
  echo "  WARN: generate_index.py not found, building JSON manually"
  # Fallback: build index from ACL
  echo "[" > "$AGENT_DIR/skills_index.json"
  FIRST=true
  acl_list_skills | while read -r SKILL_ID; do
    DESC=""
    DESC=$(acl_skill_description "$PROJECT_ROOT/skills/$SKILL_ID")
    NAME=""
    NAME=$(echo "$SKILL_ID" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
    [ "$FIRST" = "true" ] && FIRST=false || echo "," >> "$AGENT_DIR/skills_index.json"
    printf '  {"id":"%s","path":"skills/%s","name":"%s","description":"%s"}' \
      "$SKILL_ID" "$SKILL_ID" "$NAME" "$(echo "$DESC" | sed 's/"/\\"/g' | head -c 200)" >> "$AGENT_DIR/skills_index.json"
  done
  echo "" >> "$AGENT_DIR/skills_index.json"
  echo "]" >> "$AGENT_DIR/skills_index.json"
fi

# 2. Ensure .agent/skills/ points to root skills/ (symlink, not copy)
if [ -L "$AGENT_DIR/skills" ]; then
  echo "  Skills symlink: OK"
elif [ -d "$AGENT_DIR/skills" ]; then
  echo "  WARN: .agent/skills/ is a real directory (not symlink). Skipping to avoid data loss."
  echo "  To convert: rm -rf .agent/skills && ln -s ../skills .agent/skills"
else
  ln -s ../skills "$AGENT_DIR/skills"
  echo "  Skills symlink: created → ../skills"
fi

# 3. Regenerate .agent/rules/GEMINI.md from current state
mkdir -p "$AGENT_DIR/rules"
cat > "$AGENT_DIR/rules/GEMINI.md" << GEMRULES
# JM-ADK v$VERSION — Antigravity Rules (Gemini Agents)

## Environment

IDE: antigravity | Triad: full (Gemini agents) | Tools: limited | Hooks: no | MCP: no | Multimodal: yes

## Awakening

Load: PRISTINO.md → Constitution $CONSTITUTION → skills_index.json → greet
Components: $SKILLS_COUNT skills · $AGENTS_COUNT agents · $COMMANDS_COUNT commands

## Input Tolerance

- Typos: fuzzy-match intent, never correct spelling
- Voice (Gemini mobile): strip filler, handle phonetic spelling, mixed ES/EN
- Dyslexia: short sentences, bullet points, clear structure
- Multilingual: respond in user's language, process in English internally

## Auto-Prompt Matching

Auto-select best skill via skills_index.json. Confidence ≥ 0.85 → execute. 0.60-0.84 → offer options. < 0.60 → ask.

## Triad Pattern

Antigravity supports full triad via Gemini agent framework:
- Lead (domain specialist) → Support (cross-cutting) → Guardian (quality)
- Sequential execution: Lead produces → Support reviews → Guardian validates
- Full composition matrix: see PRISTINO.md

## Core Rules

$(acl_core_rules | sed 's/^/- /')

## Quality Gates

$(acl_quality_gates)

## Stack

Firebase + HTML/CSS/JS + Angular/React + Hostinger
No SSR, no Docker, no custom servers.

## Brand

$(acl_brand_palette | tr ' ' '\n' | paste - - | sed 's/^/- /')

## Skill Loading

\`skills_index.json\` for fast lookup → load full SKILL.md on demand via \`skills/{id}/SKILL.md\`

## References

- Soul: \`PRISTINO.md\` | Constitution: \`references/ontology/constitution-$CONSTITUTION.md\`
- Index: \`skills_index.json\` | Brand: \`references/brand/design-tokens.json\`

## Requires

- **IDE**: Antigravity Kit (Gemini agent framework)
- **Model**: Gemini 2.5 Pro (recommended) or Flash
- **Capability**: Function calling required
- **Not supported**: Hooks, MCP servers, workspace management (Claude Code only)
GEMRULES

echo "  Rules: .agent/rules/GEMINI.md regenerated"

# 4. Update .agent/ARCHITECTURE.md counts
if [ -f "$AGENT_DIR/ARCHITECTURE.md" ]; then
  sed -i '' "s/[0-9]* agents/$AGENTS_COUNT agents/g" "$AGENT_DIR/ARCHITECTURE.md" 2>/dev/null
  sed -i '' "s/[0-9]* skills/$SKILLS_COUNT skills/g" "$AGENT_DIR/ARCHITECTURE.md" 2>/dev/null
  echo "  Architecture: counts updated"
fi

echo "ADAPTER-COMPLETE: antigravity ($SKILLS_COUNT skills indexed)"
