---
name: guardrails-management-deep
type: variation
version: 2.0.0
description: "Guardrails Management — deep analysis mode. Exhaustive coverage."
---

# Guardrails Management — Deep Mode

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
2. Check existing `references/guardrails/*.json` when present
3. Lead executes with exhaustive analysis:
   - Cover ALL edge cases, not just common path
   - Classify proposal, verify target file, generate next ID, review duplicates,
     review conflicts, require explicit confirmation, and preserve removals as
     deactivations
   - Document every assumption with `[SUPUESTO]`
4. Support reviews with expanded scope:
   - Unconfirmed writes, wrong file, duplicate active rule, unverifiable rule,
     conflicting constraint/guideline, and deletion instead of deactivation
5. Guardian validates with strict criteria:
   - Evidence tags 100% coverage (no untagged claims)
   - Quality gate fully met
   - JSON output passes `scripts/validate_guardrails_packet.py`

## Output

- Full operation packet with proposal, confirmation, conflict review, storage
  action, validation evidence, risks, and confidence rationale
