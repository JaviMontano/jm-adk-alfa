---
name: brand-docx-primary
type: execution
version: 2.1.0
description: "Execute deterministic Brand DOCX generation."
triad:
  lead: "brand-docx-lead"
  support: "brand-docx-support"
  guardian: "brand-docx-guardian"
---

# Brand DOCX - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `document_type` | Proposal, report, memo, case study, brief, or cover page | Yes | User |
| `title` | DOCX title and core property title | Yes | User |
| `content_outline` | Sections, paragraphs, tables, and footer needs | Yes | User |
| `brand_config` | Path or inline brand tokens | No | User/codebase |
| `artifact_date` | Date shown in metadata | No | User |
| `year` | Footer year | No | User |
| `confidential` | Footer confidentiality flag | No | User |

## Execution

1. Read `assets/activation-policy.json`.
2. Read `assets/brand-docx-contract.json`.
3. Resolve supplied brand config or `assets/fallback-brand-config.json`.
4. Generate exactly one real DOCX artifact when output is requested.
5. Validate package parts, core properties, brand tokens, tables, footer,
   placeholders, and dependency boundaries.
6. Return artifact path, validation evidence, and limits.

## Validation Gate

For skill changes, run:

```bash
bash skills/brand-docx/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill brand-docx
```
