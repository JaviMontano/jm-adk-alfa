# Find Skills Scripts

## `validate_find_skills_report.py`

Validates a frozen JSON recommendation report against local assets:

- source scope and source type rules;
- bounded candidate count;
- score totals and score breakdown dimensions;
- remote snapshot date requirements;
- Tier F recommendation block;
- install confirmation and no-auto-install policy;
- evidence tags and exact dates.

## `check.sh`

Runs offline fixtures. It accepts valid reports and rejects reports with auto-installation, live remote claims, unscored candidates, Tier F recommendations, missing evidence, or unbounded candidate lists.
