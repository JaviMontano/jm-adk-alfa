---
name: discovery-orchestration-deep
type: variation
version: 2.0.0
description: "Discovery Orchestration — deep analysis mode. Exhaustive coverage."
---

# Discovery Orchestration — Deep Mode

## When to Use

Use deep mode when thoroughness matters more than speed: architecture decisions, security audits, compliance reviews, critical deliverables.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load `knowledge/body-of-knowledge.md` and every file listed in
   `assets/manifest.json`
2. Check guardrails when present
3. Lead executes with exhaustive analysis:
   - Cover ALL edge cases, not just common path
   - Build dependency graph, phase gates, deliverable register, blockers,
     dashboard summary, and validation evidence
   - Document every assumption with `[SUPUESTO]`
4. Support reviews with expanded scope:
   - Cycles, unsafe parallelism, missing owners, unvalidated deliverables,
     inconsistent cross-references, and blocked transitions
5. Guardian validates with strict criteria:
   - Evidence tags 100% coverage (no untagged claims)
   - Quality gate fully met
   - JSON output passes `scripts/validate_discovery_orchestration_packet.py`

## Output

- Exhaustive deliverable with full evidence trail
- Edge cases, dashboard, validation evidence, risks, and confidence rationale
