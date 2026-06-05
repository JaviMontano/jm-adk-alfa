# Example Input

Create a Claude Project system prompt for a billing-support assistant.

The assistant may answer only from uploaded invoice records, contract excerpts, and support policy snippets. It must return JSON with `severity`, `reason`, `source_ids`, and `coverage_gap`. If a claim is not in the provided sources, it must refuse or report `coverage_gap`.

Use Prompt Forge Playbook format, include a rubric scorecard, and add happy path, edge case, and adversarial tests.
