# Structured Output Design Assets

These assets make the skill output deterministic and locally checkable.

- `structured-output-design-contract.json` defines the JSON package accepted by the offline validator.
- `json-schema-policy.json` requires closed object schemas with grounded required fields.
- `nullable-policy.json` requires optional fields to use union types with `null` and forbids false defaults.
- `enum-escape-policy.json` requires escape values and sibling details fields for enum properties.
- `tool-choice-policy.json` requires forced `tool_choice` when the only valid action is structured emission.
- `refusal-error-policy.json` requires typed parsing from `tool_use.input` and an explicit failure route.

The local validator in `scripts/validate_structured_output_design.py` reads these files and runs without network access, wall-clock input, or randomness.
