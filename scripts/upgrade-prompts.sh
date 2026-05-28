#!/bin/bash
# Upgrade all prompts to production-grade: triad, dynamic params, skill integration
# Usage: bash scripts/upgrade-prompts.sh
set -e
ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
cd "$ROOT"

# Category → default support concern mapping
get_support_concern() {
  case "$1" in
    architecture) echo "security and scalability" ;;
    deployment) echo "security and rollback" ;;
    development) echo "accessibility and performance" ;;
    discovery) echo "business viability and stakeholder alignment" ;;
    meta) echo "consistency and constitutional compliance" ;;
    quality) echo "completeness and edge cases" ;;
    business) echo "competitive positioning and ROI" ;;
    devops) echo "reliability and incident prevention" ;;
    analytics) echo "data accuracy and privacy" ;;
    ai) echo "safety and hallucination prevention" ;;
    automation) echo "error recovery and idempotency" ;;
    enterprise) echo "compliance and audit readiness" ;;
    ux) echo "accessibility and usability" ;;
    content) echo "clarity and audience fit" ;;
    *) echo "quality and evidence completeness" ;;
  esac
}

# Category → default lead agent
get_lead_agent() {
  case "$1" in
    architecture) echo "architecture-designer" ;;
    deployment) echo "deployment-specialist" ;;
    development) echo "frontend-craftsman" ;;
    discovery) echo "requirements-analyst" ;;
    meta) echo "adk-orchestrator" ;;
    quality) echo "quality-engineer" ;;
    business) echo "marketing-context-specialist" ;;
    devops) echo "ci-pipeline-design-specialist" ;;
    analytics) echo "kpi-framework-specialist" ;;
    ai) echo "prompt-engineering-specialist" ;;
    automation) echo "workflow-orchestration-specialist" ;;
    enterprise) echo "compliance-framework-specialist" ;;
    ux) echo "user-testing-specialist" ;;
    content) echo "technical-writing-patterns-specialist" ;;
    *) echo "adk-orchestrator" ;;
  esac
}

# Category → default support agent
get_support_agent() {
  case "$1" in
    architecture) echo "security-architect" ;;
    deployment) echo "security-scanner" ;;
    development) echo "accessibility-designer" ;;
    discovery) echo "domain-modeler" ;;
    meta) echo "integrity-validator" ;;
    quality) echo "code-reviewer" ;;
    business) echo "competitive-positioning-specialist" ;;
    devops) echo "monitoring-setup-specialist" ;;
    analytics) echo "data-privacy-patterns-specialist" ;;
    ai) echo "ai-safety-specialist" ;;
    automation) echo "error-recovery-automation-specialist" ;;
    enterprise) echo "audit-trail-design-specialist" ;;
    ux) echo "accessibility-designer" ;;
    content) echo "accessibility-writing-specialist" ;;
    *) echo "quality-guardian" ;;
  esac
}

echo "=== UPGRADING TOP-LEVEL PROMPTS ==="
count=0
for f in prompts/*/*.md; do
  [ ! -f "$f" ] && continue
  [[ "$f" == *".catalog"* ]] && continue

  # Extract existing frontmatter
  name=$(grep '^name:' "$f" 2>/dev/null | head -1 | sed 's/name: *//')
  category=$(grep '^category:' "$f" 2>/dev/null | head -1 | sed 's/category: *//')
  desc=$(grep '^description:' "$f" 2>/dev/null | head -1 | sed 's/description: *//;s/"//g')
  [ -z "$name" ] && name=$(basename "$f" .md)
  [ -z "$category" ] && category=$(basename "$(dirname "$f")")
  [ -z "$desc" ] && desc="Execute $name workflow"

  HNAME=$(echo "$name" | sed 's/[0-9]*-//;s/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
  LEAD=$(get_lead_agent "$category")
  SUPPORT=$(get_support_agent "$category")
  CONCERN=$(get_support_concern "$category")
  SKILL=$(echo "$name" | sed 's/^[0-9]*-//')

  cat > "$f" << PEOF
---
name: $name
category: $category
version: 2.0.0
description: "$desc"
triad:
  lead: "$LEAD"
  support: "$SUPPORT"
  guardian: "quality-guardian"
skills: ["$SKILL"]
output-formats: ["html", "md"]
---

# $HNAME

> $desc

## Orchestration

| Role | Agent | Responsibility |
|------|-------|---------------|
| Lead | \`$LEAD\` | Produces the primary deliverable |
| Support | \`$SUPPORT\` | Reviews for $CONCERN |
| Guardian | \`quality-guardian\` | Validates evidence, gates, Constitution |

## Dynamic Parameters

| Parameter | Description | Required | Default | Filled By |
|-----------|-------------|----------|---------|-----------|
| \`{{objective}}\` | What to achieve | Yes | — | User input |
| \`{{context}}\` | Background and constraints | Yes | — | User or environment |
| \`{{audience}}\` | Who consumes the output | No | "technical team" | User |
| \`{{depth}}\` | Detail level: quick / standard / deep | No | "standard" | Auto |
| \`{{output_format}}\` | Format: html / docx / xlsx / md | No | "html" | Auto |

## Execution Protocol

### Phase 1: Think First (Constitution XIII)
- Read existing context: \`{{context}}\`
- Load skill guidelines: \`skills/$SKILL/knowledge/body-of-knowledge.md\`
- Check guardrails: \`references/guardrails/*.json\`
- Identify applicable quality gate (G0-G3)

### Phase 2: Execute
- **Lead** (\`$LEAD\`) produces deliverable for \`{{objective}}\`
- Follows skill procedure: Discover → Analyze → Execute → Validate
- Applies evidence tags: \`[CODE]\` \`[CONFIG]\` \`[DOC]\` \`[INFERENCE]\` \`[ASSUMPTION]\`
- Uses brand template if \`{{output_format}}\` = html

### Phase 3: Review
- **Support** (\`$SUPPORT\`) reviews for:
  - $CONCERN
  - Edge cases and uncovered assumptions
  - Evidence tag completeness

### Phase 4: Validate
- **Guardian** checks:
  - [ ] All claims have evidence tags
  - [ ] Quality gate criteria met
  - [ ] Constitution XIII + XIV respected
  - [ ] Output exceeds expectations (insight + next steps included)

## Output Contract

**Delivers**: $desc
**Format**: \`{{output_format}}\` with MetodologIA brand if HTML
**Quality**: Evidence-tagged, gate-compliant, triada-validated
**Surpasses by**: Includes actionable recommendations and next steps beyond the ask
PEOF

  count=$((count + 1))
done
echo "  Upgraded $count top-level prompts"

echo "=== UPGRADING SKILL PRIMARY PROMPTS ==="
count=0
for f in skills/*/prompts/primary.md; do
  [ ! -f "$f" ] && continue
  SKILL=$(echo "$f" | sed 's|skills/||;s|/prompts/primary.md||')
  HNAME=$(echo "$SKILL" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')

  cat > "$f" << PEOF
---
name: ${SKILL}-primary
type: execution
version: 2.0.0
description: "Execute the ${HNAME} workflow with triad orchestration."
triad:
  lead: "${SKILL}-lead"
  support: "${SKILL}-support"
  guardian: "${SKILL}-guardian"
---

# ${HNAME} — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| \`{{task}}\` | What to accomplish | Yes | User input |
| \`{{context}}\` | Background and constraints | Yes | User or codebase |
| \`{{constraints}}\` | Additional rules | No | Guardrails JSON |
| \`{{depth}}\` | quick / standard / deep | No | Auto |
| \`{{output_format}}\` | html / docx / xlsx / md | No | Auto |

## Execution

1. **Load knowledge**: Read \`knowledge/body-of-knowledge.md\`
2. **Check guardrails**: Read \`references/guardrails/*.json\`
3. **Lead** (\`${SKILL}-lead\`): Execute SKILL.md Steps 1-4 for \`{{task}}\`
   - Discover → Analyze → Execute → Validate
   - Apply evidence tags on all claims
4. **Support** (\`${SKILL}-support\`): Review for cross-cutting concerns
   - Edge cases, security, accessibility, performance
5. **Guardian** (\`${SKILL}-guardian\`): Validate
   - Evidence tags complete
   - Quality gate met
   - Constitution XIII + XIV respected
   - Output exceeds expectations

## Output

- Primary deliverable for \`{{task}}\` in \`{{output_format}}\`
- Evidence tags on every claim
- Recommendations beyond the ask
- Confidence score (>= 0.95)
PEOF

  count=$((count + 1))
done
echo "  Upgraded $count skill primary prompts"

echo "=== UPGRADING SKILL META PROMPTS ==="
count=0
for f in skills/*/prompts/meta.md; do
  [ ! -f "$f" ] && continue
  SKILL=$(echo "$f" | sed 's|skills/||;s|/prompts/meta.md||')
  HNAME=$(echo "$SKILL" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')

  cat > "$f" << PEOF
---
name: ${SKILL}-meta
type: self-improvement
version: 2.0.0
description: "Evaluate and improve the ${HNAME} skill."
---

# ${HNAME} — Self-Improvement

## Evaluate

1. Is \`knowledge/body-of-knowledge.md\` current? New standards, deprecated practices?
2. Are the 4 sub-agents (lead, support, guardian, specialist) covering all perspectives?
3. Are templates producing useful deliverables? Test with a real scenario.
4. What edge cases have been encountered that aren't documented?
5. Are there new insights from \`insights/\` that apply to this skill?
6. Has the related skill landscape changed? New cross-references needed?

## Improve

1. Update body of knowledge with new findings (tag with \`[DOC]\`)
2. Add prompt variations for newly discovered use cases
3. Refine quality criteria based on real-world feedback
4. Update knowledge graph: new concepts, new \`[[wikilinks]]\`
5. Test templates with edge-case inputs to verify robustness
6. Propose Constitution amendment if recurring ambiguity found (XVII)

## Trigger

Run this meta-prompt when:
- Skill hasn't been reviewed in 30+ days
- User reports unexpected output quality
- New related skills added to the kit
- Insights file updated with relevant patterns
PEOF

  count=$((count + 1))
done
echo "  Upgraded $count skill meta prompts"

echo "=== UPGRADING SKILL VARIATION PROMPTS ==="
count=0
for f in skills/*/prompts/variations/*.md; do
  [ ! -f "$f" ] && continue
  SKILL=$(echo "$f" | sed 's|skills/||;s|/prompts/.*||')
  VNAME=$(basename "$f" .md)
  HNAME=$(echo "$SKILL" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')

  # Skip already-rich variations (prompt-engineering exemplar)
  if [ "$SKILL" = "prompt-engineering" ] && [ "$VNAME" != "quick" ]; then
    count=$((count + 1))
    continue
  fi

  cat > "$f" << PEOF
---
name: ${SKILL}-${VNAME}
type: variation
version: 2.0.0
description: "${HNAME} — ${VNAME} mode execution."
---

# ${HNAME} — ${VNAME^} Mode

## When to Use
Use this variation when: time-constrained (quick), deeply exploring (deep), or auditing existing work (audit).

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| \`{{task}}\` | Yes | User input |
| \`{{context}}\` | No | Auto-detected |

## Execution (${VNAME} mode)

1. Load skill guidelines: \`knowledge/body-of-knowledge.md\`
2. Execute with ${VNAME} depth — $(case $VNAME in quick) echo "skip deep analysis, apply most common pattern directly";; deep) echo "exhaustive analysis, all edge cases, full evidence";; audit) echo "review existing work against quality criteria";; *) echo "balanced execution with evidence tags";; esac)
3. Evidence tags on all claims
4. Confidence >= 0.95

## Output
- Deliverable calibrated to ${VNAME} depth
- Evidence-tagged, Constitution-compliant
PEOF

  count=$((count + 1))
done
echo "  Upgraded $count skill variation prompts"

echo ""
echo "=== UPGRADE COMPLETE ==="
echo "Total prompts upgraded: $(( $(find prompts -name '*.md' -not -path '*/.catalog/*' | wc -l) + $(find skills -path '*/prompts/*.md' | wc -l) + $(find skills -path '*/prompts/variations/*.md' | wc -l) ))"
