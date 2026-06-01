# Form UX Advanced Assets

These assets support deterministic audits of advanced form user experience.

| Asset | Purpose |
|---|---|
| `ux-heuristics.json` | Friction scoring thresholds and required journey capabilities. |
| `inline-validation-copy.json` | Field-level copy patterns that avoid vague or punitive messages. |
| `wizard-progress-template.html` | Accessible progress indicator baseline for multi-step forms. |
| `error-recovery-checklist.md` | Recovery baseline for validation, network, server, and upload failures. |

Use `scripts/audit-form-ux.py` to turn a structured journey into a reproducible UX audit.
