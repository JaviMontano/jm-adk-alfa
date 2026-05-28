---
name: brand-docx
description:  [EXPLICIT]
  This skill should be used when the user asks to "generate a Word document", [EXPLICIT]
  "create a branded DOCX", "build a proposal in Word format", [EXPLICIT]
  "make a brand-compliant report", or "produce a cover page", [EXPLICIT]
  or mentions python-docx, Word templates, or DOCX generation. [EXPLICIT]
  It generates brand-compliant Word documents using python-docx with configurable [EXPLICIT]
  brand tokens for colors, fonts, cover pages, headers, callouts, tables, and footers. [EXPLICIT]
  Use this skill whenever the user needs a .docx file with branded styling, [EXPLICIT]
  even if they don't explicitly ask for "brand DOCX". [EXPLICIT]
argument-hint: "document-type title [brand-config-path]" [EXPLICIT]
model: opus [EXPLICIT]
context: fork [EXPLICIT]
allowed-tools: [EXPLICIT]
  - Read [EXPLICIT]
  - Grep [EXPLICIT]
  - Glob [EXPLICIT]
  - Write [EXPLICIT]
  - Edit [EXPLICIT]
  - Bash [EXPLICIT]
version: 1.0.0
---
 [EXPLICIT]
# Brand DOCX — Word Document Generator [EXPLICIT]
 [EXPLICIT]
Generate brand-compliant Word documents (.docx) using python-docx. Reads brand tokens from config and applies colors, typography, layout patterns, and structural elements. [EXPLICIT]
 [EXPLICIT]
## Prerequisites [EXPLICIT]
 [EXPLICIT]
- python-docx installed (`pip install python-docx`) [EXPLICIT]
- Brand config file (optional; uses neutral defaults without one) [EXPLICIT]
 [EXPLICIT]
## Brand Configuration [EXPLICIT]
 [EXPLICIT]
Search for config: [EXPLICIT]
1. Path passed as argument [EXPLICIT]
2. `./brand-config.json` [EXPLICIT]
3. `~/.claude/brand-config.json` [EXPLICIT]
 [EXPLICIT]
### Config Fields Used [EXPLICIT]
 [EXPLICIT]
```json [EXPLICIT]
{ [EXPLICIT]
  "brand": { "name": "", "wordmark": "", "wordmarkAccent": "", "tagline": "", "positioning": "" }, [EXPLICIT]
  "colors": { "primary": "#FF7E08", "black": "#000000", "white": "#FFFFFF", "background": "#EFEAE4", "muted": "#B8A894" }, [EXPLICIT]
  "decorative": ["#42D36F", "#06C8C8", "#9747FF", "#FE9CAB"], [EXPLICIT]
  "typography": { "display": "Clash Grotesk", "displayFallback": "Calibri", "body": "Inter", "bodyFallback": "Calibri" }, [EXPLICIT]
  "docx": { "year": "2026", "confidential": true } [EXPLICIT]
} [EXPLICIT]
``` [EXPLICIT]
 [EXPLICIT]
## Color Palette (python-docx) [EXPLICIT]
 [EXPLICIT]
```python [EXPLICIT]
from docx.shared import RGBColor [EXPLICIT]
 [EXPLICIT]
def load_brand_colors(config): [EXPLICIT]
    """Load colors from brand config, with defaults."""
    c = config.get("colors", {})
    return {
        "primary":    RGBColor.from_string(c.get("primary", "2563EB").lstrip("#")),
        "black":      RGBColor.from_string(c.get("black", "000000").lstrip("#")),
        "white":      RGBColor.from_string(c.get("white", "FFFFFF").lstrip("#")),
        "background": RGBColor.from_string(c.get("background", "F8FAFC").lstrip("#")),
        "muted":      RGBColor.from_string(c.get("muted", "94A3B8").lstrip("#")),
    }
```

## Typography

Brand display font with system fallback: [EXPLICIT]

```python
from docx.shared import Pt

def get_fonts(config):
    t = config.get("typography", {})
    return {
        "display": t.get("display", "Calibri"),
        "displayFallback": t.get("displayFallback", "Calibri"),
        "body": t.get("body", "Calibri"),
        "bodyFallback": t.get("bodyFallback", "Calibri"),
    }

def style_heading(run, fonts, colors, level=1):
    sizes = {1: 32, 2: 24, 3: 18, 4: 14}
    run.font.name = fonts["display"]
    run.font.size = Pt(sizes.get(level, 16))
    run.font.bold = True
    run.font.color.rgb = colors["black"]

def style_body(run, fonts, colors):
    run.font.name = fonts["body"]
    run.font.size = Pt(10)
    run.font.color.rgb = colors["black"]

def style_label(run, fonts, colors):
    run.font.name = fonts["body"]
    run.font.size = Pt(8)
    run.font.color.rgb = colors["primary"]
    run.font.bold = True
```

## Page Setup

```python
from docx.shared import Inches, Cm

def setup_page(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.27)   # A4
    section.page_height = Inches(11.69)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.8)
    section.right_margin = Cm(2.8)
```

## Document Components

### Cover Page
```python
def add_cover(doc, title, subtitle="", doc_type="", config={}):
    fonts = get_fonts(config)
    colors = load_brand_colors(config)
    brand = config.get("brand", {})

    # Wordmark
    logo_p = doc.add_paragraph()
    logo_run = logo_p.add_run(brand.get("wordmark", brand.get("name", "")))
    logo_run.font.name = fonts["display"]
    logo_run.font.size = Pt(20)
    logo_run.font.bold = True
    logo_run.font.color.rgb = colors["black"]
    if brand.get("wordmarkAccent"):
        accent = logo_p.add_run(brand["wordmarkAccent"])
        accent.font.name = fonts["display"]
        accent.font.size = Pt(20)
        accent.font.bold = True
        accent.font.color.rgb = colors["primary"]

    doc.add_paragraph()  # spacing

    if doc_type:
        lp = doc.add_paragraph()
        lr = lp.add_run(doc_type.upper())
        style_label(lr, fonts, colors)

    tp = doc.add_paragraph()
    tr = tp.add_run(title)
    style_heading(tr, fonts, colors, level=1)

    if subtitle:
        sp = doc.add_paragraph()
        sr = sp.add_run(subtitle)
        sr.font.name = fonts["body"]
        sr.font.size = Pt(14)
        sr.font.color.rgb = colors["muted"]

    # Tagline
    if brand.get("tagline"):
        doc.add_paragraph()
        tag_p = doc.add_paragraph()
        tag_r = tag_p.add_run(brand["tagline"])
        tag_r.font.name = fonts["display"]
        tag_r.font.size = Pt(14)
        tag_r.font.bold = True
        tag_r.font.color.rgb = colors["primary"]

    doc.add_page_break()
```

### Section Header (with primary-color underline)
```python
def add_section_header(doc, title, label="", config={}):
    fonts = get_fonts(config)
    colors = load_brand_colors(config)
    primary_hex = config.get("colors", {}).get("primary", "2563EB").lstrip("#")

    if label:
        lp = doc.add_paragraph()
        lr = lp.add_run(label)
        style_label(lr, fonts, colors)

    h = doc.add_paragraph()
    hr = h.add_run(title)
    style_heading(hr, fonts, colors, level=2)

    # Primary-color underline via bottom border
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    pPr = h._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), primary_hex)
    pBdr.append(bottom)
    pPr.append(pBdr)
```

### Callout Box
```python
def add_callout(doc, text, variant="primary", config={}):
    colors_map = {
        "primary": (config.get("colors",{}).get("primary","2563EB").lstrip("#"), "000000"),
        "dark":    ("000000", "FFFFFF"),
        "light":   (config.get("colors",{}).get("background","F8FAFC").lstrip("#"), "000000"),
    }
    bg, fg = colors_map.get(variant, colors_map["primary"])
    # Implementation: 1-cell table with background fill
    # (same pattern as original, using bg/fg from config)
```

### Data Table
```python
def add_data_table(doc, headers, rows, config={}):
    """Table with primary-color header row, alternating row backgrounds."""
    colors = config.get("colors", {})
    primary = colors.get("primary", "2563EB").lstrip("#")
    bg_alt = colors.get("background", "F8FAFC").lstrip("#")
    # Header: primary bg, white text
    # Data: alternating white / background color
```

### Header & Footer
```python
def add_header_footer(doc, title="", config={}):
    brand = config.get("brand", {})
    docx_cfg = config.get("docx", {})
    year = docx_cfg.get("year", "2026")
    # Header: wordmark left, doc title right
    # Footer: confidential label + year + page number
```

## Document Types

| Type | Cover | Accent | Header Style |
|------|-------|--------|-------------|
| Proposal | Background color | Primary | Display H1 |
| Technical report | White | Primary | Display H1 |
| Case study | Dark | Primary | White headline |
| Internal memo | White | Primary left border | Compact |
| Event materials | Decorative color | Primary/White | Bold display |

## Writing Tone

- Direct: lead with key message
- Confident but humble
- Action-oriented: active verbs
- Human-centered: connect to human impact
- Integrate tagline in section closings

## Assumptions & Limits

- Brand display font may not be installed on all systems; fallback font always specified
- python-docx does not support all Word features (e.g., advanced shapes, SmartArt)
- Colors are applied via XML manipulation for backgrounds; some features require OxmlElement
- A4 default; Letter available by changing page dimensions

## Edge Cases

- **Font not installed:** Fallback to Calibri/Arial automatically
- **Long tables (> 20 rows):** Split across pages; repeat header row
- **Multi-language:** Set paragraph language attribute for spell-check
- **Landscape sections:** Add new section with `WD_ORIENT.LANDSCAPE`

## Validation Gate

- [ ] Brand config loaded (or defaults applied)
- [ ] All colors from config (no hardcoded values)
- [ ] Typography uses configured fonts with fallbacks
- [ ] Cover page has wordmark, title, tagline
- [ ] Section headers have primary-color underline
- [ ] Tables have branded header row
- [ ] Header shows wordmark; footer shows year + confidential
- [ ] Page margins are generous (brand breathing room)

version: 1.0.0
---
**Author:** Javier Montano | **Last updated:** March 18, 2026

## Usage

Example invocations: [EXPLICIT]

- "/brand-docx" — Run the full brand docx workflow
- "brand docx on this project" — Apply to current context

