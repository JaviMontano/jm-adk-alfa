# Audit Security Scripts

Deterministic local checks for static plugin security reports.

- `validate_security_report.py` validates report structure, category coverage,
  severity counts, finding IDs, placeholder handling, and remediation coverage.
- `check.sh` runs one valid fixture and two negative fixtures without network,
  current time, random values, provider calls, or file mutation.
