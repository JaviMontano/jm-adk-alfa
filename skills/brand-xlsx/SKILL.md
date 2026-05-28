---
name: brand-xlsx
description: 
  This skill should be used when the user asks to "generate a branded spreadsheet",
  "create an Excel file with brand colors", "build an XLSX report",
  "apply brand styling to a spreadsheet", or mentions openpyxl or brand tokens. [EXPLICIT]
  It generates brand-compliant Excel spreadsheets (.xlsx) using openpyxl with
  configurable color fills, typography, layout patterns, KPI boxes, and footers. [EXPLICIT]
  Use this skill whenever the user needs any styled or branded Excel output,
  even if they don't explicitly ask for "brand-xlsx". [EXPLICIT]
argument-hint: "sheet-title [brand-config-path]"
model: opus
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
version: 1.0.0
---

# Brand XLSX — Spreadsheet Generator

Generate brand-compliant Excel spreadsheets (.xlsx) using openpyxl. Reads brand tokens from config and applies consistent colors, typography, layout patterns. [EXPLICIT]

## Prerequisites

- openpyxl installed (`pip install openpyxl`)
- Brand config file (optional; neutral defaults without one)

## Brand Configuration

Search for config: [EXPLICIT]
1. Path passed as argument
2. `./brand-config.json`
3. `~/.claude/brand-config.json`

### Config Fields Used

```json
{
  "brand": { "name": "", "wordmark": "", "tagline": "" },
  "colors": {
    "primary": "#FF7E08",
    "black": "#000000",
    "white": "#FFFFFF",
    "background": "#EFEAE4",
    "muted": "#B8A894",
    "primarySoft": "#FFF0E0"
  },
  "decorative": ["#42D36F", "#06C8C8", "#9747FF", "#FE9CAB"],
  "xlsx": { "year": "2026", "domain": "yourbrand.com" }
}
```

## Color Fills

```python
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

def load_fills(config):
    c = config.get("colors", {})
    return {
        "primary":    PatternFill("solid", fgColor=c.get("primary", "2563EB").lstrip("#")),
        "black":      PatternFill("solid", fgColor=c.get("black", "000000").lstrip("#")),
        "background": PatternFill("solid", fgColor=c.get("background", "F8FAFC").lstrip("#")),
        "white":      PatternFill("solid", fgColor=c.get("white", "FFFFFF").lstrip("#")),
        "muted":      PatternFill("solid", fgColor=c.get("muted", "94A3B8").lstrip("#")),
        "soft":       PatternFill("solid", fgColor=c.get("primarySoft", "EFF6FF").lstrip("#")),
    }
```

## Typography

Brand display fonts are typically unavailable in Excel. Use system fallbacks: [EXPLICIT]

```python
def load_fonts(config):
    c = config.get("colors", {})
    primary = c.get("primary", "2563EB").lstrip("#")
    return {
        "title":  lambda size=18: Font(name="Calibri", bold=True, size=size, color="000000"),
        "header": lambda: Font(name="Calibri", bold=True, size=10, color=primary),
        "body":   lambda: Font(name="Calibri", bold=False, size=10, color="000000"),
        "muted":  lambda: Font(name="Calibri", bold=False, size=8, color=c.get("muted","94A3B8").lstrip("#")),
    }
```

## Sheet Layout Pattern

```
Row 1:   Title bar      primary fill, bold dark text, height 36 [EXPLICIT]
Row 2:   Subtitle       dark fill, small primary-color text, height 18 [EXPLICIT]
Row 3:   Spacer [EXPLICIT]
Row 4+:  Section label  primary fill, white text [EXPLICIT]
Row 5+:  Column headers dark fill, primary-color bold text [EXPLICIT]
Row 6+:  Data rows      alternating white / background [EXPLICIT]
Last:    Footer         dark fill, muted text [EXPLICIT]
```

Tab color: always set to primary color. [EXPLICIT]

## Core Functions

### Sheet Setup
```python
def setup_sheet(ws, title, subtitle="", config={}):
    fills = load_fills(config)
    fonts = load_fonts(config)
    primary = config.get("colors",{}).get("primary","2563EB").lstrip("#")

    ws.sheet_properties.tabColor = primary
    ws.row_dimensions[1].height = 36
    ws.merge_cells('A1:J1')
    c = ws['A1']
    c.value = title
    c.font = fonts["title"]()
    c.fill = fills["primary"]
    c.alignment = Alignment(horizontal="left", vertical="center", indent=2)

    if subtitle:
        ws.row_dimensions[2].height = 18
        ws.merge_cells('A2:J2')
        c2 = ws['A2']
        c2.value = subtitle
        c2.font = Font(name="Calibri", size=9, color=primary)
        c2.fill = fills["black"]
        c2.alignment = Alignment(horizontal="left", vertical="center", indent=2)
```

### Column Headers
```python
def add_headers(ws, row, headers, style="dark", config={}):
    fills = load_fills(config)
    primary = config.get("colors",{}).get("primary","2563EB").lstrip("#")

    fill = fills["black"] if style == "dark" else fills["primary"]
    color = primary if style == "dark" else "000000"
    ws.row_dimensions[row].height = 26
    for i, label in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=label)
        c.font = Font(name="Calibri", bold=True, size=10, color=color)
        c.fill = fill
        c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        c.border = Border(bottom=Side(style="medium", color=primary))
```

### Data Rows
```python
def add_data(ws, start_row, data, config={}):
    fills = load_fills(config)
    fonts = load_fonts(config)
    muted = config.get("colors",{}).get("muted","94A3B8").lstrip("#")

    for i, row_data in enumerate(data):
        fill = fills["white"] if i % 2 == 0 else fills["background"]
        ws.row_dimensions[start_row + i].height = 20
        for j, value in enumerate(row_data, 1):
            c = ws.cell(row=start_row + i, column=j, value=value)
            c.font = fonts["body"]()
            c.fill = fill
            c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
            c.border = Border(bottom=Side(style="hair", color=muted))
```

### Section Divider
```python
def add_section(ws, row, label, col_span=10, config={}):
    fills = load_fills(config)
    ws.row_dimensions[row].height = 22
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_span)
    c = ws.cell(row=row, column=1, value=f"  {label}")
    c.font = Font(name="Calibri", bold=True, size=10, color="FFFFFF")
    c.fill = fills["primary"]
    c.alignment = Alignment(horizontal="left", vertical="center")
```

### KPI Box
```python
def add_kpi(ws, row, col, label, value, unit="", config={}):
    fills = load_fills(config)
    primary = config.get("colors",{}).get("primary","2563EB").lstrip("#")

    ws.row_dimensions[row].height = 16
    lc = ws.cell(row=row, column=col, value=label)
    lc.font = Font(name="Calibri", bold=True, size=8, color=primary)
    lc.fill = fills["black"]
    lc.alignment = Alignment(horizontal="center", vertical="center")

    ws.row_dimensions[row + 1].height = 34
    vc = ws.cell(row=row + 1, column=col, value=f"{value}{unit}")
    vc.font = Font(name="Calibri", bold=True, size=22, color="000000")
    vc.fill = fills["primary"]
    vc.alignment = Alignment(horizontal="center", vertical="center")
```

### Footer
```python
def add_footer(ws, row, col_span=10, config={}):
    fills = load_fills(config)
    fonts = load_fonts(config)
    brand = config.get("brand", {})
    xlsx_cfg = config.get("xlsx", {})
    year = xlsx_cfg.get("year", "2026")
    domain = xlsx_cfg.get("domain", "")
    wordmark = brand.get("wordmark", brand.get("name", ""))
    tagline = brand.get("tagline", "")

    ws.row_dimensions[row].height = 16
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=col_span)
    parts = [p for p in [wordmark, tagline, year, domain] if p]
    c = ws.cell(row=row, column=1, value="  " + "  |  ".join(parts))
    c.font = fonts["muted"]()
    c.fill = fills["black"]
    c.alignment = Alignment(horizontal="left", vertical="center")
```

### Auto Column Width
```python
def auto_fit(ws, min_w=10, max_w=50):
    from openpyxl.utils import get_column_letter
    for col in ws.columns:
        letter = get_column_letter(col[0].column)
        max_len = max((len(str(c.value)) for c in col if c.value), default=0)
        ws.column_dimensions[letter].width = max(min_w, min(max_w, max_len + 4))
```

## Approved Color Combinations

| Use Case | Fill | Font Color |
|----------|------|-----------|
| Sheet title | Primary | Black |
| Column headers | Black | Primary |
| Alt headers | Primary | Black |
| Section dividers | Primary | White |
| KPI label | Black | Primary |
| KPI value | Primary | Black |
| Even rows | White | Black |
| Odd rows | Background | Black |
| Footer | Black | Muted |

## Assumptions & Limits

- Brand display fonts unavailable in Excel; Calibri Bold used as universal fallback
- openpyxl handles .xlsx only (not .xls)
- Conditional formatting uses openpyxl rules; complex formulas may need manual adjustment
- Charts use openpyxl chart module; brand decorative colors applied to series

## Edge Cases

- **No brand config:** Use neutral blue palette with Calibri
- **Wide data (> 10 columns):** Freeze panes at header row + first column
- **Large datasets (> 1000 rows):** Use openpyxl write-only mode for performance
- **Multiple sheets:** Apply setup_sheet to each; consistent tab colors
- **Print layout:** Set print area, page orientation, header/footer for printing

## Validation Gate

- [ ] Brand config loaded (or defaults applied)
- [ ] Tab color set to primary
- [ ] Title bar uses primary fill
- [ ] Column headers use dark fill with primary text (or inverse)
- [ ] Data rows alternate white / background
- [ ] Footer present with wordmark + tagline + year
- [ ] No default Excel blue/grey styles remaining
- [ ] Sheet names are meaningful (not "Sheet1")
- [ ] Column widths auto-fitted

---
**Author:** Javier Montano | **Last updated:** March 18, 2026

## Usage

Example invocations: [EXPLICIT]

- "/brand-xlsx" — Run the full brand xlsx workflow
- "brand xlsx on this project" — Apply to current context

