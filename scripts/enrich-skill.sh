#!/bin/bash
# Enrich a skill directory with sub-agents, knowledge, prompts, and templates
# Usage: bash scripts/enrich-skill.sh <skill-name>
# Batch: for s in skills/*/; do bash scripts/enrich-skill.sh "$(basename $s)"; done

set -euo pipefail
ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
cd "$ROOT"

SKILL="$1"
DIR="skills/$SKILL"

if [ -z "$SKILL" ] || [ ! -d "$DIR" ]; then
  echo "Usage: bash scripts/enrich-skill.sh <skill-name>"
  echo "Skill directory '$DIR' not found."
  exit 1
fi

# Skip if already enriched (has agents/ subdir)
if [ -d "$DIR/agents" ]; then
  exit 0
fi

# Extract description from SKILL.md frontmatter
DESC=$(sed -n '/^description:/,/^[a-z]/p' "$DIR/SKILL.md" | head -3 | tail -2 | tr -d '\n' | sed 's/^ *//')
[ -z "$DESC" ] && DESC="Specialist skill for $SKILL domain."

# Human-readable name
HNAME=$(echo "$SKILL" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')

# Create structure
mkdir -p "$DIR/agents" "$DIR/knowledge" "$DIR/prompts/variations" "$DIR/templates"

# ---- SUB-AGENTS ----
cat > "$DIR/agents/lead.md" << AEOF
---
name: ${SKILL}-lead
role: Lead
description: "Primary execution agent for ${HNAME}."
tools: [Read, Write, Glob, Grep]
---
# ${HNAME} Lead
Produces the primary deliverable for this skill domain.
Follows RCTF pattern: Role → Context → Task → Format.
AEOF

cat > "$DIR/agents/support.md" << AEOF
---
name: ${SKILL}-support
role: Support
description: "Cross-cutting review for ${HNAME}: security, accessibility, edge cases."
tools: [Read, Glob, Grep]
---
# ${HNAME} Support
Reviews Lead output for blind spots: security implications,
accessibility concerns, edge cases, and Constitution compliance.
AEOF

cat > "$DIR/agents/guardian.md" << AEOF
---
name: ${SKILL}-guardian
role: Guardian
description: "Quality validation for ${HNAME} deliverables."
tools: [Read, Glob, Grep]
---
# ${HNAME} Guardian
Validates: evidence tags present, quality gate criteria met,
output format compliant, Constitution principles respected.
Blocks delivery if confidence < 0.95.
AEOF

cat > "$DIR/agents/specialist.md" << AEOF
---
name: ${SKILL}-specialist
role: Specialist
description: "Deep domain expert for ${HNAME}."
tools: [Read, Write, Glob, Grep]
---
# ${HNAME} Specialist
Deep expertise in advanced patterns and edge cases for this domain.
Activated when Lead or Support identify need for specialized knowledge.
AEOF

# ---- KNOWLEDGE ----
cat > "$DIR/knowledge/knowledge-graph.md" << KEOF
# ${HNAME} — Knowledge Graph
<!-- Zettelkasten-ready: use [[wikilinks]] for Obsidian -->

## Core Concepts
- [[${SKILL}]] — Primary concept
- [[${SKILL}-patterns]] — Common patterns and approaches
- [[${SKILL}-anti-patterns]] — What to avoid

## Tags
#${SKILL} #jm-adk #zettelkasten

## Cross-References
- Related skills in this domain
KEOF

cat > "$DIR/knowledge/body-of-knowledge.md" << KEOF
# ${HNAME} — Body of Knowledge

## Canon
Key standards, references, and best practices for ${HNAME}.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Accuracy | >= 90% | Correct outputs / total |
| Evidence coverage | 100% | All claims tagged |
| Constitution compliance | 100% | Principles respected |

## References
- Industry standards for this domain
- Best practice guides
KEOF

# ---- PROMPTS ----
cat > "$DIR/prompts/primary.md" << PEOF
---
name: ${SKILL}-primary
type: execution
description: "Execute the primary workflow for ${HNAME}."
---
# ${HNAME} — Primary Prompt
## Input
- **Task**: {{task_description}}
- **Context**: {{context}}
- **Constraints**: {{constraints}}
## Execution
1. Discover: gather requirements and context
2. Analyze: select approach per Constitution XIII/XIV
3. Execute: implement with evidence tags
4. Validate: verify quality criteria
## Output
Deliverable with evidence tags and quality gate compliance.
PEOF

cat > "$DIR/prompts/meta.md" << PEOF
---
name: ${SKILL}-meta
type: meta
description: "Self-improvement prompt for ${HNAME} skill."
---
# ${HNAME} — Meta-Prompt
## Self-Evaluation
1. Are the patterns in body-of-knowledge still current?
2. Are there new techniques not yet cataloged?
3. What edge cases have been encountered?
4. Do the templates produce useful output?
## Improvement: update knowledge, add variations, refine templates.
PEOF

cat > "$DIR/prompts/variations/quick.md" << PEOF
---
name: ${SKILL}-quick
type: variation
audience: general
description: "Quick execution mode for ${HNAME} — minimal overhead."
---
# ${HNAME} — Quick Mode
Skip deep analysis. Apply the most common pattern directly.
Use when the task is well-defined and time-constrained.
PEOF

# ---- TEMPLATES ----
cat > "$DIR/templates/output.html" << TEOF
<!-- MetodologIA Brand Template: ${HNAME} -->
<!-- Uses: references/brand/design-tokens.json + html-template.html -->
<!-- Replace: {{TITLE}}, {{SUBTITLE}}, {{CONTENT}}, {{DATE}} -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}} | ${HNAME} | MetodologIA</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Montserrat:wght@300;400;500&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>
:root{--navy:#0A122A;--surface:#1E293B;--gold:#FFD700;--cyan:#137DC5;--text:#FFF;--muted:#94A3B8}
body{font-family:'Montserrat',sans-serif;background:var(--navy);color:var(--text);margin:0;padding:2rem}
.c{max-width:1000px;margin:0 auto}
h1{font-family:'Poppins',sans-serif;background:linear-gradient(135deg,#fff,var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
h2{font-family:'Poppins',sans-serif;color:var(--gold);border-bottom:1px solid rgba(255,255,255,.05);padding-bottom:.5rem}
.card{background:rgba(30,41,59,.4);backdrop-filter:blur(24px);border:1px solid rgba(255,255,255,.05);border-radius:12px;padding:1.5rem;margin:1rem 0}
table{width:100%;border-collapse:collapse}
th{font-family:'Poppins',sans-serif;color:var(--gold);text-align:left;padding:.75rem;border-bottom:2px solid var(--gold)}
td{padding:.75rem;border-bottom:1px solid rgba(255,255,255,.05)}
footer{text-align:center;margin-top:3rem;border-top:2px solid var(--gold);padding:1.5rem;font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--muted)}
@media print{body{background:#fff;color:#1a1a1a}h1{-webkit-text-fill-color:#0A122A}h2{color:#0A122A}}
</style>
</head>
<body><div class="c">
<h1>{{TITLE}}</h1>
<p style="color:var(--muted);font-family:'JetBrains Mono',monospace;font-size:.85rem">{{SUBTITLE}}</p>
<hr style="border:none;height:4px;background:linear-gradient(90deg,var(--gold),var(--cyan));border-radius:2px;margin:1.5rem 0">
{{CONTENT}}
<footer><span style="color:var(--gold)">MetodologIA</span> — {{DATE}}<br>Made with Pristino Agent</footer>
</div></body></html>
TEOF

cat > "$DIR/templates/output.docx.md" << TEOF
# DOCX Template — ${HNAME}
## Structure
- Title: "${HNAME} Report"
- Section 1: Executive Summary
- Section 2: Findings / Deliverables
- Section 3: Recommendations
- Footer: "MetodologIA — {{date}}"
## Formatting: Poppins headings, Montserrat body, JetBrains Mono code
TEOF
