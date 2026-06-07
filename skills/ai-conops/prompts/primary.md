---
name: ai-conops-primary
type: execution
version: 2.1.0
description: "Execute deterministic AI CONOPS with stakeholder, value, metric, and mode validation."
triad:
  lead: "ai-conops-lead"
  support: "ai-conops-support"
  guardian: "ai-conops-guardian"
---

# AI CONOPS - Execute

## Dynamic Parameters
| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{system_name}}` | AI system or project name | Yes | User input |
| `{{context}}` | Problem, stakeholders, constraints, data readiness | Yes | User or discovery docs |
| `{{mode}}` | piloto-auto / desatendido / supervisado / paso-a-paso | No | User or default |
| `{{format}}` | markdown / json / dual | No | User or default |
| `{{scope}}` | ejecutiva / tecnica | No | User or default |

## Execution
1. Load `references/interaction-spectrum.md`, `references/success-metrics.md`, and `references/business-value-matrix.md`.
2. Load `assets/` policies and the report contract.
3. Lead drafts the six CONOPS sections.
4. Support checks stakeholder, metric, interaction, value, and mode completeness.
5. Specialist joins for high-stakes, regulated, or autonomy Level 4-5 scenarios.
6. Guardian validates the packet and runs `scripts/validate_ai_conops_report.py` when JSON is produced.

## Output
- System vision and objectives.
- Stakeholder and actor map.
- AI-human interaction design.
- Business value assessment.
- Success metrics framework.
- Operational modes and transitions.
- Assumptions, risks, validation status, and evidence trail.
