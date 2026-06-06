---
name: ai-workflow-automation-deep
type: variation
version: 2.0.0
description: "Ai Workflow Automation — deep analysis mode. Exhaustive coverage."
---

# AI Workflow Automation — Deep Mode

## When to Use

Use deep mode when thoroughness matters more than speed: architecture decisions, security audits, compliance reviews, critical deliverables.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load `knowledge/body-of-knowledge.md` and every file in
   `assets/manifest.json`
2. Check existing guardrails when present
3. Lead executes with exhaustive analysis:
   - Cover ALL edge cases, not just common path
   - Model each actor, step, input, output, approval, handoff, fallback,
     validation check, and operational risk
   - Document every assumption with `[SUPUESTO]`
4. Support reviews with expanded scope:
   - Missing approval gates, AI hallucination containment, handoff gaps,
     bounded retries, data exposure, and rollback paths
5. Guardian validates with strict criteria:
   - Evidence tags 100% coverage (no untagged claims)
   - Quality gate fully met
   - JSON output passes `scripts/validate_ai_workflow_plan.py`

## Output

- Exhaustive workflow plan with gates, handoffs, fallback paths, validation
  evidence, risks, and confidence rationale
