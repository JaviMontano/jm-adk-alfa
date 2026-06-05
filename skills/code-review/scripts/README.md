# Code Review Scripts

`check.sh` validates deterministic report fixtures using
`validate_code_review_report.py`.

The validator checks required sections, finding fields, severity/category
values, gapless finding IDs, evidence tags, file-line evidence, decision rules,
positive-pattern requirements for approvals, and forbidden rubber-stamp phrases.
