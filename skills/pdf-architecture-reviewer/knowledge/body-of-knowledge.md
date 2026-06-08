# Pdf Architecture Reviewer Body of Knowledge

## Evidence Hierarchy

| Evidence Type | Role | Can Authorize Change |
|---|---|---|
| Read PDF page excerpt | Source of document claim | No |
| Repository code, config, or docs | Confirms repo state | No by itself |
| Official vendor/framework/source docs | Confirms external behavior | Yes, when linked to a verified claim |
| User summary of attachment | Context only | No |
| File name or unreviewed page | Not evidence | No |

## Deterministic Review Rules

- A claim is valid only when it links to one or more page evidence IDs.
- Page evidence must include page number, excerpt, extraction method, and linked claim IDs.
- Repo mapping is required for every implementation-impacting claim.
- A contradiction exists when PDF evidence and repo evidence disagree or when the repo lacks a required component.
- Required official sources must be named before implementation is authorized.
- Guardian pass is impossible when the PDF is unread, evidence is unpaginated, repo mapping is missing, contradictions are unresolved, or official sources are still required.

## Common Anti-Patterns

- Approving a change because the PDF title sounds authoritative.
- Treating OCR output with no page number as verified evidence.
- Merging multiple claims from different pages into one untraceable summary.
- Reporting repo alignment without naming paths or observed state.
- Calling a decision complete while official source requirements remain open.

## Quality Signals

| Signal | Target |
|---|---|
| Page traceability | Every claim has page evidence |
| Repo traceability | Every impactful claim maps to repo state |
| Conflict handling | Contradictions are explicit and blocking |
| Official source readiness | Required official sources are named or satisfied |
| Determinism | Structured report passes the offline validator |
