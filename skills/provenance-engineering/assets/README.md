# Provenance Engineering Assets

These assets define the deterministic report contract for typed provenance.

- `provenance-engineering-contract.json`: required top-level report fields and Guardian decisions.
- `claim-source-policy.json`: source and claim field requirements.
- `conflict-policy.json`: conflict preservation and forbidden resolution modes.
- `escalation-policy.json`: human escalation requirements.
- `render-policy.json`: visible source/date/conflict render gates.
- `structural-test-policy.json`: required offline structural test flags.

The offline validator consumes these assets directly. If a policy changes, update fixtures and evals in the same skill.
