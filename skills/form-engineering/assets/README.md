# Form Engineering Assets

These assets support deterministic form architecture work.

| Asset | Purpose |
|---|---|
| `form-engineering-policy.json` | Required sections for validation parity, accessibility, uploads, optimistic submit, autosave, and telemetry. |
| `error-message-patterns.json` | Stable copy patterns for field, form, upload, network, and server validation errors. |
| `optimistic-submit-template.ts` | TypeScript skeleton for pending/success/failure/retry submit state. |
| `upload-control-template.html` | Accessible upload control markup with progress and retry hooks. |

Use `scripts/compile-form-contract.py` to turn a structured spec into an implementation contract.
