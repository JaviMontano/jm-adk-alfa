# Output Contract Validation

status: pass
contract_id: billing-summary-markdown
artifact: artifacts/billing-summary.md

## Checks

| Check | Status | Expected | Observed | Repair |
|---|---|---|---|---|
| contract_loaded | pass | JSON contract parses | contract_id present | none |
| format | pass | markdown | markdown headings detected | none |
| markdown_sections | pass | Summary, Evidence, Result, Validation, Risks and Limits | all present | none |
| evidence_tags | pass | at least one allowed tag | `[CÓDIGO]`, `[DOC]` | none |
| naming | pass | kebab-case | billing-summary.md | none |

## Violations

- None.

## Evidence

- [CÓDIGO] Contract required five Markdown sections.
- [CÓDIGO] Artifact path used kebab-case.

## Repair Suggestions

- None.
