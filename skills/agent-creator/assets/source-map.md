# Agent Creator Source Map

| Source | Consumed By | Purpose |
|---|---|---|
| `assets/agent-spec-schema.json` | `scripts/compile-agent.py`, `SKILL.md` | Required fields and validation thresholds |
| `assets/tool-policy.json` | `scripts/compile-agent.py`, `knowledge/body-of-knowledge.md` | Least-privilege tool validation |
| `assets/model-selection-policy.json` | `scripts/compile-agent.py`, `SKILL.md` | Model selection guardrails |
| `assets/description-trigger-policy.json` | `scripts/compile-agent.py`, `prompts/primary.md` | Trigger-description validation |
| `assets/agent-template.md` | `scripts/compile-agent.py`, `templates/output.md` | Stable Markdown section order |
| `scripts/fixtures/*.json` | `scripts/check.sh` | Positive and negative offline validation |
