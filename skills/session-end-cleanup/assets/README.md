# Session End Cleanup Assets

These assets make the closeout workflow deterministic and auditable.

| Asset | Purpose |
|---|---|
| `activation-policy.json` | Defines activation triggers, false positives, and routing boundaries. |
| `output-contract.json` | Defines required Markdown and JSON closeout sections. |
| `evidence-policy.json` | Defines evidence tags, proof requirements, and forbidden claims. |
| `closure-checklist.json` | Defines guardian checks before pass/block decisions. |
| `update-policy.json` | Defines tasklog/changelog write boundaries. |

The script validator in `scripts/validate_session_cleanup_report.py` checks JSON
fixtures against the output and evidence contract.
