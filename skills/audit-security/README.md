# Audit Security

Deterministic read-only static security audit for plugin artifacts.

Use this skill when a plugin, skill bundle, hook directory, or explicit file
list needs a security report for secrets, unsafe paths, hook injection,
sensitive files, script safety, or external network risks.

## Local Resources

- `assets/activation-policy.json`: activation and refusal routing
- `assets/scan-policy.json`: six categories, severities, statuses, placeholders
- `assets/report-contract.json`: required report sections and fields
- `assets/evidence-policy.json`: evidence and remediation requirements
- `references/security-patterns.md`: human-readable pattern catalog
- `scripts/validate_security_report.py`: offline report validator
- `scripts/check.sh`: deterministic fixture test

## Local Checks

```bash
bash skills/audit-security/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill audit-security
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill audit-security
```

## Decision Rule

All six categories must be executed. CRITICAL/WARNING findings require
remediation plan entries. Placeholder secrets are INFO, not CRITICAL.
