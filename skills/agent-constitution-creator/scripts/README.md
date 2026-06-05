# Scripts

`validate_agent_constitution.py` validates generated `agent.md` constitutions against the deterministic contract in `assets/agent-constitution-schema.json`.

## Usage

```bash
python3 -B skills/agent-constitution-creator/scripts/validate_agent_constitution.py \
  --schema skills/agent-constitution-creator/assets/agent-constitution-schema.json \
  --constitution agents/data-quality-agent/agent.md \
  --tool-registry Read,Grep,Glob
```

Run the bundled smoke suite with:

```bash
bash skills/agent-constitution-creator/scripts/check.sh
```
