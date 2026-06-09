# katas-builtin-tool-selection Assets

These assets define deterministic acceptance rules for built-in tool selection.

- `builtin-tool-selection-report-contract.json` defines required report fields.
- `tool-fit-policy.json` maps intent to the correct built-in tool.
- `read-economy-policy.json` forbids repository-wide upfront reads.
- `edit-anchor-policy.json` requires a unique edit anchor or a safe fallback.
- `evidence-policy.json` defines local evidence and validation requirements.

The offline validator in `scripts/validate_tool_selection_report.py` uses these
assets as the local contract.
