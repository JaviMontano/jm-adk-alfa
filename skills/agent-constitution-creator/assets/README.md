# Assets

These assets make `agent-constitution-creator` deterministic.

## Files

- `agent-constitution-template.md`: canonical `agent.md` skeleton with the 22 required headings.
- `agent-constitution-schema.json`: machine-readable field, evidence, and validation contract.
- `authority-policy.json`: least-privilege and no-invention policy for tools, agents, memory, and decisions.
- `constitution-checklist.md`: manual review checklist that mirrors the validator.

Use the template for generation, then validate the produced Markdown with `scripts/validate_agent_constitution.py`.
