---
name: agent-constitution-creator-deep
type: variation
variant: deep
---
# Agent Constitution Creator — Deep Mode

Use deep mode when the ecosystem already has multiple agents, known overlap risk, memory policies, security checkpoints, or approval boundaries.

Load only the needed resources:

- `assets/agent-constitution-schema.json`
- `assets/authority-policy.json`
- `references/domain-knowledge.md`
- Existing peer `agents/*/agent.md` files that overlap the requested role

Stop generation when authority conflicts or material overlap remains unresolved.
