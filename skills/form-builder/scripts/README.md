# Form Builder Scripts

Deterministic local rendering for semantic, accessible form HTML.

## Entry Points

- `render-form-schema.py`: renders a multi-step form from structured JSON.
- `check.sh`: validates schema fixtures, rendered fragments, conditional logic, and invalid-schema failure.

## Contract

- The renderer writes files only with `--output`; stdout is the default.
- The renderer rejects duplicate field names, unsupported types, unlabeled fields, invalid conditionals, and malformed steps.
- The renderer uses `assets/form-control.css`, `assets/form-step-template.html`, and `assets/validation-policy.json`.
