# Quality Gatekeeper

Deterministic JM-ADK G0-G3 gate validator. It evaluates scoped gate criteria,
blocks phase transitions when required evidence is missing or failed, and emits
a score-history entry contract. [EXPLICIT]

## Activation

- `/jm:advance`
- "can this pass G0/G1/G2/G3?"
- "quality gate report"
- "release/PR gate readiness"
- "validate score-history entry"

## Deterministic Resources

| Path | Purpose |
|---|---|
| `assets/gate-criteria.json` | G0-G3 criteria and sequential order |
| `assets/report-contract.json` | Report schema and decision rules |
| `assets/evidence-policy.json` | Evidence tags and assumption warning threshold |
| `assets/score-history-schema.json` | Proposed score-history entry contract |
| `scripts/validate_gate_report.py` | Offline JSON report validator |
| `scripts/check.sh` | Pass/block/fail fixture runner |

## Local Checks

```bash
bash skills/quality-gatekeeper/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill quality-gatekeeper
python3 -B scripts/validate-skill-dod.py --skill quality-gatekeeper
```

## Decision Rule

No gate advances unless every required criterion in scope has tagged evidence
and no required criterion is `fail` or `not_verified`. [EXPLICIT]
