# AI CONOPS Assets

These assets define the deterministic contract for AI CONOPS outputs.

## Files
- `conops-report-contract.json`: required JSON shape for machine-checkable CONOPS packets.
- `interaction-level-policy.json`: Level 1-5 autonomy policy and controls.
- `stakeholder-policy.json`: stakeholder coverage and decision-right requirements.
- `value-matrix-policy.json`: value/effort quadrant contract.
- `metrics-policy.json`: three-pillar success metric requirements.
- `operational-mode-policy.json`: required modes and transition fields.

The offline validator in `scripts/validate_ai_conops_report.py` enforces the
same contract against deterministic fixtures.
