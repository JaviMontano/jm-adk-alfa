# Example Output

# XLSX Template Spec: Delivery Workflow Tracker

## Summary

- Template type: `tracking-matrix`
- Locale: `es-CO`
- Sheets: `3`
- Named ranges: `3`
- Validation checks: `6`

## Sheets

| Sheet | Purpose | Columns | Print area |
|---|---|---|---|
| Tracker | Track delivery work items, owners, status, priority, dates, completion, and notes. | 9 | A1:I200 |
| Summary | Auto-calculated dashboard from Tracker data. | 4 | A1:D20 |
| Config | Editable dropdown values for owners, statuses, and priorities. | 3 | A1:C50 |

## Columns

| Sheet | Header | Type | Width | Formula/source |
|---|---|---|---|---|
| Tracker | Owner | dropdown | 20 | Config!A2:A50 |
| Tracker | Status | dropdown | 16 | Config!B2:B20 |
| Summary | Completion Rate | formula | 16 | =IF(B3=0,0,B4/B3) |

## Validation

| Status | Check | Evidence |
|---|---|---|
| pass | formula-guards | Division formulas use IF guards. |
| pass | dropdown-sources | Dropdowns reference Config sheet ranges. |

## Handoff

- Renderer: `xlsx-renderer`
- Output format: `.xlsx`
- Notes: Add native workbook styles and freeze panes after this spec passes validation.
