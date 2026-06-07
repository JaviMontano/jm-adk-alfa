# Example Input

Create an AI CONOPS packet for `Claims Copilot`, an insurance claims assistant.

Context:
- Business problem: adjusters spend too much time triaging routine claims.
- Candidate AI capability: summarize claim documents, classify severity, and recommend next action.
- Decision stakes: medium; incorrect routing can delay payment but does not automatically approve claims.
- Constraints: human adjuster remains accountable, audit trail required, fairness checks required.
- Known stakeholders: claims director, adjuster, compliance officer, data science lead, operations manager.

Required output:
- JSON packet using `jm-labs.ai-conops.report.v1`.
- Level 2 or Level 3 interaction rationale.
- Metrics across technical, business, and UX/ethics pillars.
- Operational modes including degraded and recovery.
