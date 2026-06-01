<!--
generated-by: scripts/scaffold-skill.py
generated-for: functional-toolbelt
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Run the full functional toolbelt for a Loan Origination domain:

- Event storming: application submitted, credit checked, offer accepted.
- Story mapping: applicant starts an application, uploads income evidence, officer reviews risk, officer resolves exceptions.
- Business rules: missing income evidence blocks credit review; low score routes to manual review.
- Acceptance criteria: complete applications become submitted; incomplete evidence is blocked.
- Traceability: map each requirement to use case, flow, test, and acceptance criteria.
- Anti-pattern scan: flag ambiguous "qualified applicant" and missing manual-review exception paths.

Run the deterministic compiler if the toolbelt input can be represented as JSON.
