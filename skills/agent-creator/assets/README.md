# Agent Creator Assets

These files make custom-agent generation deterministic and auditable.

| Asset | Purpose |
|---|---|
| `agent-spec-schema.json` | Required structured input shape for compiling an agent definition |
| `tool-policy.json` | Least-privilege tool tiers and forbidden wildcard rules |
| `model-selection-policy.json` | Complexity-to-model mapping |
| `description-trigger-policy.json` | Rules for writing routing descriptions and negative triggers |
| `agent-template.md` | Canonical Markdown section order |
| `source-map.md` | Trace of which files consume each asset |

The assets are read-only inputs for `scripts/compile-agent.py`; runtime
installation of generated agents is a separate user-approved action.
