<!--
generated-by: scripts/scaffold-skill.py
generated-for: guardrails-management
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

The user says:

"From now on, always include evidence tags on every claim in JM Labs outputs."

Existing files:

- `references/guardrails/guidelines.json` contains `GL-001`: "Use Spanish for
  user-facing status updates when the user writes in Spanish."
- `references/guardrails/constraints.json` is empty.
- `references/guardrails/guardrails.json` contains `GR-001`: "Prefer concise
  summaries after validation."

Reference date: 2026-06-06.

Detect the rule, classify it, check duplicate/conflict risk, ask for explicit
confirmation, and show the JSON entry that would be stored only if confirmed.
