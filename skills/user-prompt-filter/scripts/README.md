# User Prompt Filter Scripts

## Entry Points

- `filter-prompt.py`: reads a structured prompt-filter input and emits Markdown
  or stable JSON.
- `check.sh`: runs deterministic positive and adversarial fixture checks.

## Guarantees

- Offline only.
- No MCP, browser, shell action, network, or moderation API calls.
- Redacts secret-like evidence.
- Fails on missing required input fields.
- Same input produces the same output.
