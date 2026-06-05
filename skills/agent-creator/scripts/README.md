# Agent Creator Scripts

## Entry Points

- `compile-agent.py`: validates a structured agent spec and renders a Markdown
  agent definition.
- `check.sh`: runs positive and negative fixture checks offline.

## Guarantees

- No network access.
- No writes outside the caller's requested output path.
- No runtime installation into `.claude/agents/` or `~/.claude/agents/`.
- Invalid names, wildcard tools, missing trigger descriptions, weak process
  steps, missing negative boundaries, and built-in collisions fail fast.

## Example

```bash
python3 skills/agent-creator/scripts/compile-agent.py \
  --input skills/agent-creator/scripts/fixtures/agent-spec-input.json
```
