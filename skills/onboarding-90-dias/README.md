# Onboarding 90 Dias

`onboarding-90-dias` creates and validates sustainable 30/60/90 plans for new roles with role evidence, bounded priorities, measurable deliverables, stakeholder actions, and anti-burnout limits.

## Triggers

- `onboarding-90-dias`
- `plan-30-60-90`
- `onboarding`

## Deterministic Contract

- Require exactly three phases: 30, 60, and 90.
- Require role context, weekly-hour capacity, and supplied evidence.
- Allow at most four priorities per phase.
- Block sustained plans above 45 hours/week.
- Require deliverable and validation signal for every priority.
- Block always-on, hustle, and guaranteed-outcome language.

## Local Validation

```bash
bash skills/onboarding-90-dias/scripts/check.sh
python3 skills/onboarding-90-dias/scripts/plan_30_60_90.py --input skills/onboarding-90-dias/scripts/fixtures/valid-role-transition.json
```

## Assets

- `assets/phase-contract.json`
- `assets/burnout-policy.json`
- `assets/evidence-policy.json`
- `assets/validation-policy.json`
- `assets/output-contract.json`
