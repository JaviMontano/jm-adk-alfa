# Prompting And Meta Prompting Assets

These assets define the deterministic contract for reusable prompt-system reports.

- `prompting-and-meta-prompting-contract.json`: required top-level fields and Guardian decisions.
- `prompt-component-policy.json`: required prompt fields and missing-data modes.
- `meta-prompt-policy.json`: required meta-prompt review dimensions.
- `acceptance-criteria-policy.json`: verifiable acceptance criteria rules.
- `eval-case-policy.json`: required eval coverage for prompt reuse.
- `safety-anti-drift-policy.json`: safety and anti-drift gates.

The offline validator consumes these files directly; changes to policy files must be paired with fixture updates.
