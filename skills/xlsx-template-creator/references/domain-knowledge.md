# Domain Knowledge -- XLSX Template Creator

## Workbook Specification Pattern

A stable workbook spec separates spreadsheet intent from binary rendering. The skill should first produce a JSON-compatible contract, validate it locally, and only then hand the contract to a renderer.

## Required Template Families

| Template | Main Use | Required Sheets |
|---|---|---|
| `tracking-matrix` | Row-level work tracking, compliance matrices, status reviews | `Tracker`, `Summary`, `Config` |
| `metrics-dashboard` | KPI monitoring, thresholds, alert queues, executive summaries | `KPIs`, `Trends`, `Alerts`, `Config` |

## Formula Safety

- Start formulas with `=`.
- Guard division formulas with `IF`, for example `=IF(C2=0,0,B2/C2)`.
- Avoid volatile or external functions in templates unless a renderer policy explicitly allows them.
- Prefer named ranges and `Config` references for values users edit.

## Spreadsheet Handoff

The final response should make clear which features are structural and which belong to the renderer. Structural features include sheets, columns, formulas, dropdown sources, named ranges, and validation evidence. Renderer features include binary workbook generation, native charts, freeze panes, Excel table styles, and file metadata.
