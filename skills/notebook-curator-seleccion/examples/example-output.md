# Example Output

## Summary

`SEL-ACME` is complete for the offline `SEL-EMPRESA` archetype because all eight canonical slots are present exactly once.

## Slot Table

| Slot | Source | Evidence |
| --- | --- | --- |
| job-description | ACME role description | exported document supplied by user |
| empresa-research | ACME research notes | manual research notes |
| proceso-log | Selection timeline | user process log |
| entrevista-notas | Panel interview notes | interview notes excerpt |
| material-prep | Prep matrix | user-created preparation matrix |
| oferta-precontrato | Offer draft | exported offer draft |
| notas-gratitud | Thank-you drafts | post-interview drafts |
| post-mortem | Process retrospective | lessons learned notes |

## Curation Actions

- Keep benefits appendix as optional source.
- Do not fetch external URLs during deterministic validation.

## Validation

`validate_archetype.py --input <packet>` returned complete.

## Risks

- Source content was not summarized beyond supplied evidence.
- Live NotebookLM sync remains out of scope.
