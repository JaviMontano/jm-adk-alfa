---
name: brand-html-primary
type: execution
version: 2.1.0
description: "Execute deterministic Brand HTML generation."
triad:
  lead: "brand-html-lead"
  support: "brand-html-support"
  guardian: "brand-html-guardian"
---

# Brand HTML - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{page_type}}` | Landing page, report, microsite section, or static page | Yes | User |
| `{{content_outline}}` | Sections, copy, or data to render | Yes | User |
| `{{brand_config}}` | Path or inline tokens | No | User/codebase |
| `{{language}}` | Language code | No | User |
| `{{direction}}` | `ltr` or `rtl` | No | User/content |
| `{{artifact_date}}` | Date shown in artifact | No | User |
| `{{favicon_href}}` | URL-encoded SVG data URI or relative `favicon.svg` path | No | Brand config/fallback |

## When To Activate

Activate only when the user asks for a branded HTML artifact. Route DOCX, XLSX,
PDF, slides, and token-only requests away.

## Execution

1. Read `assets/activation-policy.json`.
2. Read `assets/brand-html-contract.json`.
3. Resolve supplied brand config or `assets/fallback-brand-config.json`.
4. Generate exactly one single-file HTML artifact.
5. Validate semantic landmarks, token variables, SVG favicon link, responsive
   CSS, dependency boundaries, placeholders, and contrast gate.
6. Return validation evidence and risks.

## Validation Gate

For skill changes, run:

```bash
bash skills/brand-html/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill brand-html
```
