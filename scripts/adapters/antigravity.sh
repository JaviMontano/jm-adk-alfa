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
PROMPTS_COUNT=$(acl_count_prompts)
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
  echo "  To convert safely: back up or move .agent/skills, then create a symlink to ../skills."
else
  ln -s ../skills "$AGENT_DIR/skills"
  echo "  Skills symlink: created → ../skills"
fi

# 3. Regenerate .agent/rules/GEMINI.md from current state
mkdir -p "$AGENT_DIR/rules"
cat > "$AGENT_DIR/rules/GEMINI.md" << GEMRULES
# JM-ADK v$VERSION — Antigravity Rules (Gemini Agents)

## Environment

IDE: antigravity | Triad: adapter-guided | Tools: limited | Hooks: no | MCP: no | Multimodal: validation pending

## Awakening

Load: PRISTINO.md → Constitution $CONSTITUTION → skills_index.json → greet
Components: $SKILLS_COUNT skills · $AGENTS_COUNT agents · $COMMANDS_COUNT commands · $PROMPTS_COUNT prompts

## First Use

- Greeting-only or empty input: run guided setup before technical work.
- Explicit task: collect only missing critical context, then proceed.
- Repo not confirmed as Alfa: report \`Dato requerido\` and do not edit.
- Diagnosis command: \`python3 scripts/diagnose-first-use.py --dry-run\`.

## Input Tolerance

- Typos: fuzzy-match intent, never correct spelling
- Voice (Gemini mobile): strip filler, handle phonetic spelling, mixed ES/EN
- Dyslexia: short sentences, bullet points, clear structure
- Multilingual: respond in user's language, process in English internally

## Auto-Prompt Matching

Auto-select best skill via skills_index.json. Confidence ≥ 0.85 → execute. 0.60-0.84 → offer options. < 0.60 → ask.

## Triad Pattern

This adapter exposes Alfa's triad pattern to Antigravity-compatible rules. Runtime execution support must be validated in the target environment:
- Lead (domain specialist) → Support (cross-cutting) → Guardian (quality)
- Sequential fallback: Lead produces → Support reviews → Guardian validates
- Full composition matrix: see PRISTINO.md

## Core Rules

$(acl_core_rules | sed 's/^/- /')

## Local State Boundary

- Do not commit \`workspace/\`, \`.local/\`, \`.codex/\`, \`.env*\`, or \`.jm-adk.local.json\`.
- Use \`scripts/setup-workspace-profile.py --dry-run\` before creating local profile state.

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

- **IDE**: Antigravity-compatible Gemini agent environment
- **Model**: configured by the target runtime
- **Capability**: validation pending until executed in the target runtime
- **Not supported**: Hooks, MCP servers, workspace management (Claude Code only)
GEMRULES

echo "  Rules: .agent/rules/GEMINI.md regenerated"

# 4. Regenerate .agent/ARCHITECTURE.md as a concise derived view
cat > "$AGENT_DIR/ARCHITECTURE.md" << AGARCH
# JM Agentic Development Kit — Antigravity Derived View

<!-- Auto-generated by scripts/adapters/antigravity.sh. Do not edit manually. -->

## Component Counts

| Component | Count |
|---|---:|
| Skills | $SKILLS_COUNT |
| Agents | $AGENTS_COUNT |
| Commands | $COMMANDS_COUNT |
| Prompts | $PROMPTS_COUNT |

## Source Of Truth

- Core repo instructions: \`PRISTINO.md\`, \`CLAUDE.md\`, \`AGENTS.md\`, \`GEMINI.md\`.
- Antigravity rules: \`.agent/rules/GEMINI.md\`.
- Skill index: \`.agent/skills_index.json\`.
- Canonical skills: root \`skills/\`.

## Runtime Boundary

This directory is a derived adapter view. Runtime support for Antigravity-specific execution, function calling, multimodal behavior, hooks, MCP, and workspace management is validation pending until checked in the target Antigravity environment.

## First Use

Run:

\`\`\`bash
python3 scripts/diagnose-first-use.py --dry-run
\`\`\`

Greeting-only or empty input routes to \`/jm-adk:first-use\`. Explicit tasks route through minimal task intake and should not be blocked by full onboarding.
AGARCH
echo "  Architecture: regenerated"

echo "ADAPTER-COMPLETE: antigravity ($SKILLS_COUNT skills indexed)"
