# Quality Gatekeeper DOCX Template

Use this Markdown structure when a quality gate report must be converted to
DOCX. [EXPLICIT]

## Document Metadata

- Title: Quality Gate Report - `{gate_scope}`
- Author: JM Labs
- Gate scope: `{G0|G1|G2|G3|multi-gate}`
- Decision: `{allow|block|needs_evidence}`

## Required Sections

1. Summary table.
2. Gate results.
3. Criteria results.
4. Violations.
5. Missing evidence.
6. Remediation plan.
7. Proposed score-history entry.
8. Decision.
9. Caveats.

## Formatting Rules

- Use system fonts only.
- Preserve evidence tags in all factual claims.
- Do not omit empty sections; use `none` with tagged evidence when applicable.
- Never mark the document ready when the source report is blocked or
  `not_verified`.
