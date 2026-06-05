# Example Input

Create workflow YAML for `skill-hardening-handoff`, owned by
`workflow-creator`.

The workflow should coordinate a Coordinator, Determinism Auditor, Integrator,
and Guardian for one active skill. Include:

- exactly one active skill branch at a time
- 3-7 ordered steps
- DoD, QA checklist, RACI, KPIs, fallback, and escalation
- local validation evidence using `validate-skill-dod.py` and
  `validate-skill-scripts.py`
- no network dependency unless a maintainer explicitly requests source lookup
