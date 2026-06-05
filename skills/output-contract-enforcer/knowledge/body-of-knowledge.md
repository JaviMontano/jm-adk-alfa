# Output Contract Enforcer - Body Of Knowledge

## Canon

Output contract enforcement is a post-generation quality gate. It does not design new output schemas; it validates a generated artifact against a declared contract and blocks mismatches.

## Evidence Tags

Allowed evidence tags:

- `[CÓDIGO]`
- `[CONFIG]`
- `[DOC]`
- `[INFERENCIA]`
- `[SUPUESTO]`

Analysis outputs that require evidence tags fail when none of these tags are present.

## Check Families

| Check | Purpose | Failure Mode |
|---|---|---|
| contract_loaded | Confirm the contract source exists and parses. | blocked |
| format | Confirm markdown/json/html type expectations. | fail |
| markdown_sections | Confirm required headings. | fail |
| required_fields | Confirm JSON fields. | fail |
| evidence_tags | Confirm allowed evidence tags. | fail |
| naming | Confirm file naming convention. | fail with suggestion |
| machine_readable_packet | Confirm validation packet schema. | fail |

## Anti-Patterns

| Anti-Pattern | Risk | Deterministic Response |
|---|---|---|
| Pass with missing tags | False confidence. | `status: fail`. |
| Guessing a contract | Validates unstated preferences. | `status: blocked`. |
| Auto-renaming files | Changes user artifacts without approval. | Suggest corrected name only. |
| Mixed tag vocabularies | Inconsistent evidence quality. | Enforce canonical tag list. |
| Subjective validation | Unrepeatable gate. | Use declared checks and fixtures. |
