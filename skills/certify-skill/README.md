# Certify Skill

Final read-only certification gate for JM-ADK skills. It evaluates a target
skill with structural checks, content checks, systemic coherence, rubric
scoring, MOAT checks, and formula-based certification levels. [EXPLICIT]

## Activation

- "certify this skill"
- "is this skill ready to ship?"
- "grade this skill"
- "run quality gate on `skills/<slug>`"

Do not use for certificate documents, legal certifications, employment letters,
or generic non-skill quality review. [EXPLICIT]

## Deterministic Resources

| Path | Purpose |
|---|---|
| `assets/certification-phases.json` | Phase and check inventory |
| `assets/certification-level-policy.json` | Certification formulas |
| `assets/report-contract.json` | Report schema |
| `assets/evidence-policy.json` | Evidence tags |
| `scripts/validate_certification_report.py` | Offline report validator |
| `scripts/check.sh` | Fixture runner |

## Local Checks

```bash
bash skills/certify-skill/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill certify-skill
python3 -B scripts/validate-skill-dod.py --skill certify-skill
```

## Decision Rule

Certification level is formula-derived, not assigned by feel. Missing
`SKILL.md`, any rubric dimension below 6, or three or more structural failures
is `BLOCKED`. [EXPLICIT]
