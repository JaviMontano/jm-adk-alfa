# Pre Compact Context Assets

These assets make context preservation before compaction deterministic.

| Asset | Purpose |
|---|---|
| `retention-policy.json` | Defines P0/P1/P2/DROP classes and unsafe drop rules. |
| `output-contract.json` | Defines required Markdown and JSON packet fields. |
| `evidence-policy.json` | Defines evidence tags and source requirements. |
| `rehydration-checklist.json` | Defines guardian resume-readiness checks. |
| `compaction-risk-policy.json` | Defines loss modes and blockers. |

The script validator checks JSON packet fixtures against these rules offline.
