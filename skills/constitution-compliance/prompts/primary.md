# Constitution Compliance Primary Prompt

## Objective

Audit one artifact against JM-ADK Constitution v6.0.0 using the local
18-principle asset map and fail-closed evidence rules. [EXPLICIT]

## Required Inputs

- Artifact text or path.
- Gate context: `G0`, `G1`, `G2`, `G3`, or an explicitly tagged inference.
- Evidence sources: files, command output, PR checks, review docs, or a note that
  evidence is missing.

## Process

1. Confirm the task is a JM-ADK or Pristino compliance audit.
2. Load `assets/constitution-v6-principles.json`,
   `assets/compliance-report-contract.json`, and `assets/severity-policy.json`.
3. Inspect the artifact and evidence sources before scoring.
4. Produce all 18 principle rows exactly once.
5. Mark unsupported principles as `not_verified`, not `pass`.
6. Map findings to G0-G3 and severity.
7. Block delivery for P0/P1 failures or missing required gate evidence.

## Output

Return `templates/output.md`. Use evidence tags on factual claims and include
explicit caveats for any inference.
