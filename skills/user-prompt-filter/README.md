# User Prompt Filter

Pre-execution prompt filtering for agentic systems.

## Triggers

- User asks to sanitize, filter, classify, or harden a prompt.
- User asks to detect prompt injection or tool override attempts.
- User needs a gate before agent handoff, shell, browser, MCP, hook, or other
  tool execution.

## Deterministic Assets

- `assets/filter-input-schema.json` defines required input fields.
- `assets/threat-taxonomy.json` defines threat classes and evidence patterns.
- `assets/risk-scoring-policy.json` maps matched threats to decisions.
- `assets/sanitization-policy.json` defines safe transformation rules.
- `assets/output-schema.json` defines report shape.

## Quick Use

```bash
python3 skills/user-prompt-filter/scripts/filter-prompt.py \
  --input skills/user-prompt-filter/scripts/fixtures/prompt-injection.json
```

Validate with:

```bash
bash skills/user-prompt-filter/scripts/check.sh
```
