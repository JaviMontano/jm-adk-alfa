<!--
generated-by: scripts/scaffold-skill.py
generated-for: discovery-orchestration
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Orchestrate discovery for a customer support modernization project.

Inputs:

- `briefs/support-modernization.md`
- `docs/current-ticketing.md`
- `docs/stakeholder-notes.md`

Required discovery outputs:

- input analysis summary
- stakeholder map
- requirements brief
- system context diagram
- risk register
- validated discovery report

Rules:

- Input analysis must finish before requirements.
- Stakeholder map can run in parallel with current-state review.
- Architecture work cannot start until requirements gate passes.
- Reference date: 2026-06-06.
