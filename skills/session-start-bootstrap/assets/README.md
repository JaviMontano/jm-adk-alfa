# Session Start Bootstrap Assets

These assets make session startup deterministic and auditable.

| Asset | Purpose |
|---|---|
| `bootstrap-contract.json` | Required Markdown and JSON startup packet fields. |
| `environment-policy.json` | Repo, branch, dirty-tree, and PR checks. |
| `context-loading-policy.json` | Minimal source-loading boundaries. |
| `guardrails-policy.json` | Stop conditions and hard-rule requirements. |
| `source-priority.json` | Source precedence for conflicts. |

The script validator checks startup packet fixtures offline.
