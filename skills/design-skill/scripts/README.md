# Design Skill Scripts

## `validate_design_skill_spec.py`

Validates frozen JSON skill design specs against local assets:

- frontmatter required fields and name format;
- procedure step count and structure;
- measurable quality criteria;
- anti-pattern and edge-case minimums;
- least-privilege tool profile and rationale;
- MOAT score threshold;
- evidence tags and exact dates.

## `check.sh`

Runs offline fixtures. It accepts valid specs and rejects bad names, tool overreach, short procedures, generic criteria, missing edge cases, and low MOAT scores.
