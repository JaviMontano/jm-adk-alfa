# Structured Output Design Scripts

`check.sh` runs the offline fixture suite through `validate_structured_output_design.py`.

The validator checks:

- closed JSON object schemas;
- grounded `required` fields;
- nullable union modeling for optional fields;
- enum escape values plus `*_details`;
- forced `tool_choice` name matching;
- parsing from `tool_use.input`;
- no free-text fallback;
- explicit retry or escalation route for schema failures.
