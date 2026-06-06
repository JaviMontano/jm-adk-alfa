<!--
generated-by: scripts/scaffold-skill.py
generated-for: input-analysis
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

The input is incomplete for implementation planning. It contains one direct contradiction about login, four material gaps, and one ambiguity around public access vs PII handling. Completeness score: 58/100.

## Findings

| Type | Finding | Evidence | Action |
|---|---|---|---|
| Contradiction | Login is optional in one source but mandatory in another. | [DOC] email says optional; RFP says mandatory | Decide MVP authentication requirement before architecture. |
| Gap | Data retention is not specified. | [DOC] brief has no retention policy | Ask owner for retention and deletion requirements. |
| Gap | Success metrics are missing. | [DOC] brief omits target KPIs | Define adoption, deflection, and SLA metrics. |
| Ambiguity | Public portal conflicts with private PII unless access boundaries are explicit. | [INFERENCE] public access plus private PII | Define anonymous vs authenticated surfaces. |

## Completeness

- Score: 58/100
- Assumption ratio: 25%
- Warning banner required: no

## Validation

- All findings carry evidence tags.
- Firebase feasibility requires authentication and security rule clarification.
- No implementation plan is included; this is analysis-only.
- Recommendations are actionable questions or decisions.

## Risks

- If authentication remains unresolved, architecture choices may be invalidated.
- If retention is unstated, compliance risk remains open.

## Validation

- Skill activated intentionally.
- Output follows the requested format.
- Risks and assumptions are explicit.
