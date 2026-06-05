# Audit Content Quality

Deterministic structural quality audit for `SKILL.md` files.

Use this skill when a plugin or skill directory needs per-skill scorecards,
plugin averages, bottom-skill priorities, and systematic content gap detection.

## Local Resources

- `assets/activation-policy.json`: activation and false-positive routing
- `assets/scoring-rubric.json`: six dimensions, formula, thresholds, priorities
- `assets/report-contract.json`: required report sections and fields
- `assets/evidence-policy.json`: rationale and evidence-tag requirements
- `references/content-quality-rubric.md`: human-readable rubric mirror
- `scripts/validate_content_quality_report.py`: offline report validator
- `scripts/check.sh`: deterministic fixture test

## Local Checks

```bash
bash skills/audit-content-quality/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill audit-content-quality
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill audit-content-quality
```

## Decision Rule

All score math is formula-derived. Any discovered skill must be scored or
explicitly listed in coverage. Weak skills need specific remediation, not
generic advice.
