#!/bin/bash
# cursor.sh — Adapter: Core → Cursor IDE (.cursorrules) + Windsurf (.windsurfrules)
#
# Both IDEs use checklist-mode triad (inline in single response).
# Cursor has MCP support; Windsurf does not. Otherwise identical format.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$SCRIPT_DIR/acl.sh"

VERSION=$(acl_version)
SKILLS_COUNT=$(acl_count_skills)
AGENTS_COUNT=$(acl_count_agents)
COMMANDS_COUNT=$(acl_count_commands)
CONSTITUTION=$(acl_constitution_version)

echo "Adapter: Core → Cursor + Windsurf"

# ── .cursorrules (Cursor has MCP support) ──

cat > "$PROJECT_ROOT/.cursorrules" << CURSORRULES
# JM-ADK v$VERSION — Cursor IDE Rules

# Environment: cursor | Triad: checklist | Tools: Read/Write/Edit/Bash | MCP: yes | Multimodal: images
# Components: $SKILLS_COUNT skills · $AGENTS_COUNT agents · $COMMANDS_COUNT commands

# Awakening: load PRISTINO.md → Constitution $CONSTITUTION → PRISTINO-INDEX.md → greet

# Input Tolerance
# - Typos: fuzzy-match intent, never correct spelling
# - Dyslexia: short sentences, bullet points, clear structure
# - Multilingual: respond in user's language

# Auto-Prompt Matching
# Auto-select best skill for user intent. Apply triad as checklist in single response.
# Lead criteria → Support review → Guardian validation — all inline.

# Core Rules
$(acl_core_rules | head -6 | sed 's/^/# /')

# Quality Gates: $(acl_quality_gates)
# Stack: Firebase + HTML/CSS/JS + Angular/React + Hostinger
# Brand: $(acl_brand_palette | tr '\n' ' ')
# Soul: PRISTINO.md | Index: PRISTINO-INDEX.md

# Placement & Naming Contract
# - Task deliverables → workspace/{active}/artifacts/. Never mix system files with deliverables.
# - Kit internals (skills/agents/scripts) → maintainer mode only.
# - Filenames + slugs = kebab-case, concise, mnemonic, no spaces/accents/CamelCase.
# - Full: references/ontology/placement-naming-contract.md

# Requires: Cursor IDE. Not supported: Agent tool, hooks, workspace management.
CURSORRULES

echo "  Generated: .cursorrules"

# ── .windsurfrules (no MCP) ──

cat > "$PROJECT_ROOT/.windsurfrules" << WINDRULES
# JM-ADK v$VERSION — Windsurf IDE Rules

# Environment: windsurf | Triad: checklist | Tools: Read/Write/Edit/Bash | MCP: no | Multimodal: limited
# Components: $SKILLS_COUNT skills · $AGENTS_COUNT agents · $COMMANDS_COUNT commands

# Awakening: load PRISTINO.md → Constitution $CONSTITUTION → PRISTINO-INDEX.md → greet

# Input Tolerance
# - Typos: fuzzy-match intent, never correct spelling
# - Dyslexia: short sentences, bullet points
# - Multilingual: respond in user's language

# Auto-Prompt Matching
# Auto-select best skill. Apply triad as checklist inline.

# Core Rules
$(acl_core_rules | head -6 | sed 's/^/# /')

# Quality Gates: $(acl_quality_gates)
# Stack: Firebase + HTML/CSS/JS + Angular/React + Hostinger
# Soul: PRISTINO.md | Index: PRISTINO-INDEX.md

# Placement & Naming Contract
# - Task deliverables → workspace/{active}/artifacts/. Never mix system files with deliverables.
# - Kit internals (skills/agents/scripts) → maintainer mode only.
# - Filenames + slugs = kebab-case, concise, mnemonic, no spaces/accents/CamelCase.
# - Full: references/ontology/placement-naming-contract.md

# Requires: Windsurf IDE. Not supported: Agent tool, hooks, MCP, workspace management.
WINDRULES

echo "  Generated: .windsurfrules"
echo "ADAPTER-COMPLETE: cursor+windsurf"
