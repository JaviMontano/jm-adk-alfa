---
name: brand-xlsx-primary
type: execution
version: 2.1.0
description: "Execute deterministic Brand XLSX generation."
triad:
  lead: "brand-xlsx-lead"
  support: "brand-xlsx-support"
  guardian: "brand-xlsx-guardian"
---

# Brand XLSX - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `workbook_type` | Report, KPI dashboard, inventory table, or financial summary | Yes | User |
| `title` | Workbook title and core property title | Yes | User |
| `sheet_name` | Meaningful sheet name | Yes | User/codebase |
| `headers` | Column headers | Yes | User/data |
| `rows` | Data rows | Yes | User/data |
| `brand_config` | Path or inline brand tokens | No | User/codebase |
| `artifact_date` | Date shown in metadata | No | User |
| `year` | Footer year | No | User |
| `domain` | Footer domain | No | User |

## Execution

1. Read `assets/activation-policy.json`.
2. Read `assets/brand-xlsx-contract.json`.
3. Resolve supplied brand config or `assets/fallback-brand-config.json`.
4. Generate exactly one real XLSX artifact when output is requested.
5. Validate package parts, core properties, sheet names, tab color, brand
   styles, merged regions, freeze panes, auto filter, footer, placeholders, and
   dependency boundaries.
6. Return artifact path, validation evidence, and limits.

## Validation Gate

For skill changes, run:

```bash
bash skills/brand-xlsx/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill brand-xlsx
```
