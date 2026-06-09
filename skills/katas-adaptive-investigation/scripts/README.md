# katas-adaptive-investigation Scripts

`check.sh` runs deterministic offline fixtures through
`validate_adaptive_investigation_report.py`.

The validator checks only local JSON reports. It does not call the network,
read wall-clock time, use random values, or inspect files outside this skill.
