---
name: knowledge-management-deep
type: variation
version: 2.0.0
description: "Knowledge Management — deep analysis mode. Exhaustive coverage."
---

# Knowledge Management — Deep Mode

## When to Use

Use deep mode when thoroughness matters more than speed: architecture decisions, security audits, compliance reviews, critical deliverables.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load `knowledge/body-of-knowledge.md` and all files listed in
   `assets/manifest.json`
2. Check guardrails when present and keep missing guardrails as an explicit gap
3. Lead executes with exhaustive analysis:
   - Cover ALL edge cases, not just common path
   - Build a full register with source paths, owners, retrieval terms, aliases,
     freshness dates, status, and next actions
   - Document every assumption with `[SUPUESTO]`
4. Support reviews with expanded scope:
   - Searchability, decay, duplication, contradictions, orphan knowledge,
     ownership, compliance, and handoff viability
   - Adversarial scenarios: what could go wrong?
5. Guardian validates with strict criteria:
   - Evidence tags 100% coverage (no untagged claims)
   - Quality gate fully met
   - JSON output passes `scripts/validate_knowledge_management_report.py`

## Output

- Exhaustive deliverable with full evidence trail
- Register, searchability map, decay review, gap log, owner-bound actions,
  validation evidence, risks, and confidence rationale
