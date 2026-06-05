# Agent Constitution Delivery

## Constitution

Use the Markdown produced from `assets/agent-constitution-template.md`.

## Source Map

| Claim | Evidence Tag | Source |
|---|---|---|
| Agent role | [EXPLICIT] | User request |
| Tool registry | [EXPLICIT] or [OPEN] | Supplied registry or missing context |
| Peer agents | [EXPLICIT] or [OPEN] | Existing `agents/*/agent.md` files |

## Validation

- Validator: `scripts/validate_agent_constitution.py`
- Result: `pass` or `fail`
- Open items: list unresolved `[OPEN]` fields

## Risks and Limits

- Do not grant tools, agents, memory, or approval rights not present in supplied context.
