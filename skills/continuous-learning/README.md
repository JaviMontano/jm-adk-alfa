# Continuous Learning

Extract reusable insights from debates, discoveries, incidents, and decisions.
The skill turns one-time learning into deterministic updates for
`insights/<domain>.md`, `insights/README.md`, and optional constitution
amendment proposals when ambiguity recurs.

## Triggers

- "extract insight"
- "learn from debate"
- "continuous learning"
- "prevent re-debate"
- "capture discovery"
- "propose constitution amendment"

## Allowed Tools

- Read
- Glob
- Grep
- Bash
- Write
- Edit

## Deterministic Contract

- Always search existing insights before creating a new one.
- Extract the three debate outputs: answer, question refinements, and coverage gaps.
- Every insight must include domain, pattern, rationale, triggers, constitutional anchor, status, and evidence.
- Do not create duplicate active insights; refine or supersede existing ones.
- Propose a constitution amendment only when the same ambiguity class appears at least 3 times.
- Machine-readable learning reports must validate with `scripts/check.sh`.

## Output Format

Markdown or JSON with source event, prior insight search, extracted insights, amendment candidates, update plan, validation, and risks.
