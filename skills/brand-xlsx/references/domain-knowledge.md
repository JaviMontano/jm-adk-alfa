# Domain Knowledge - Brand XLSX

## Overview

`brand-xlsx` creates deterministic Microsoft Excel artifacts from explicit brand
tokens. The output should behave like a brand system applied to a workbook, not
a generic CSV/HTML template saved with a `.xlsx` extension.

## Best Practices

1. Resolve brand tokens before creating workbook styles.
2. Declare all date/year/domain values from caller input.
3. Write core properties for title, creator, and artifact date.
4. Use workbook package parts and styles rather than CSV/HTML as a substitute.
5. Apply primary color to sheet tab, title bar, and header borders.
6. Use explicit fallback tokens when no brand config exists.
7. Validate package structure and XML before delivery.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Alternative |
|---|---|---|
| HTML/CSV renamed as XLSX | Workbook package contract is false | Generate a real XLSX ZIP package |
| Remote font/logo URL | Breaks offline deterministic delivery | Use declared font names and local/offline assets |
| Inferred date | Makes output time-dependent | Require caller-supplied `artifact_date` |
| Legacy hardcoded colors | Breaks brand determinism | Use active config or fallback tokens |
| Placeholder leakage | Shows incomplete template resolution | Validate for unresolved `{{...}}` |
| `Sheet1` default | Fails workbook intentionality | Use a meaningful sheet name |
