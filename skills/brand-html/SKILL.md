---
name: brand-html
description: 
  This skill should be used when the user asks to "generate branded HTML",
  "create a landing page", "build a brand-compliant web page",
  "produce a styled HTML report", or "design a responsive page",
  or mentions brand tokens, CSS variables, or HTML generation. [EXPLICIT]
  It generates brand-compliant HTML/CSS by reading brand tokens from config
  and applying colors, fonts, spacing, component templates, and responsive patterns. [EXPLICIT]
  Use this skill whenever the user needs a self-contained branded web page,
  even if they don't explicitly ask for "brand HTML". [EXPLICIT]
argument-hint: "page-type [brand-config-path]"
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

# Brand HTML / Web Generation

Generate brand-compliant HTML/CSS for any brand. Reads brand tokens (colors, fonts, spacing) from a config file and produces self-contained, accessible, responsive web pages. [EXPLICIT]

## Brand Configuration

Search for brand config: [EXPLICIT]
1. Path passed as argument
2. `./brand-config.json` in working directory
3. `~/.claude/brand-config.json`

Config schema: see `design-system` skill for full schema. Key fields used here: [EXPLICIT]

```json
{
  "brand": { "name": "", "wordmark": "", "wordmarkAccent": "", "tagline": "", "positioning": "" },
  "colors": { "primary": "", "black": "", "white": "", "background": "", "muted": "" },
  "typography": { "display": "", "body": "", "fontLinks": [] },
  "spacing": { "radiusSm": "", "radiusMd": "", "radiusLg": "" }
}
```

**If no config:** Use neutral blue palette (#2563EB primary, #F8FAFC bg), system fonts.

## Color System

Define as CSS variables from config: [EXPLICIT]

```css
:root {
  --brand-primary: [colors.primary];
  --brand-black: [colors.black];
  --brand-white: [colors.white];
  --brand-bg: [colors.background];
  --brand-muted: [colors.muted];
}
```

**Rules:**
- `--brand-primary` is always the accent: CTAs, headline highlights, borders, icons
- Page backgrounds: `--brand-bg` for light mode, `--brand-black` for dark sections
- Secondary/decorative colors differentiate sections — never as hero color
- Never place wordmark on primary-color background (contrast issue)
- Text contrast: >= 4.5:1 body, >= 3:1 large text

## Typography

```css
:root {
  --font-display: [typography.display];
  --font-body: [typography.body];
}
h1, h2, h3, .headline { font-family: var(--font-display); }
body, p, span, label { font-family: var(--font-body); }
```

- Display font for ALL headlines, section titles, taglines, hero copy
- Body font for body copy, captions, labels, UI text
- Max 3 font sizes/weights per layout
- Headlines sentence case (not ALL CAPS)
- Large hero: `clamp(2.5rem, 6vw, 5.5rem)`, line-height 1.05

## Logo / Wordmark

```html
<span class="brand-wordmark" style="
  font-family: var(--font-display);
  font-weight: 600; font-size: 1.5rem;
  color: var(--brand-black);
">[wordmark]<span style="color: var(--brand-primary);">[wordmarkAccent]</span></span>
```

- Light bg: dark wordmark. Dark bg: white wordmark.
- Accent character always in primary color.
- Min size: 20px tall. Clear space: 1x logo height on all sides.

## Layout

```css
.brand-page {
  background: var(--brand-bg);
  padding: clamp(24px, 4vw, 64px);
  font-family: var(--font-body);
}
.brand-grid {
  display: grid;
  gap: clamp(16px, 2.5vw, 40px);
}
```

- Card border-radius: 12-24px
- Generous breathing room (brand should not feel crowded)
- Max-width: 1100px, centered

## Component Templates

### Hero (Dark)
Black bg, primary-color accent on key headline word, CTA button in primary color, positioning label above headline. [EXPLICIT]

### Hero (Primary Color)
Primary bg, dark text, white accent on key phrase, wordmark at bottom. [EXPLICIT]

### Card (Light)
White bg, rounded corners, shadow, heading in display font, body in body font. Optional tag chip in corner. [EXPLICIT]

### Stat Block
Primary-color left border (4px), large number in display font, label in body font. [EXPLICIT]

### Navigation
Flex row: wordmark left, links center, CTA button right in primary color. [EXPLICIT]

## Approved Color Combinations

| Background | Text | Accent | Use Case |
|-----------|------|--------|----------|
| `--brand-bg` | `--brand-black` | `--brand-primary` | Default pages |
| `--brand-black` | `--brand-white` | `--brand-primary` | Dark hero |
| `--brand-primary` | `--brand-black` | `--brand-white` | Highlight sections |
| `--brand-white` | `--brand-black` | `--brand-primary` | Cards, clean UI |

## Assumptions & Limits

- Output is single-file HTML with inline CSS (font links are the only external dependency)
- Does not handle routing or state management (use a framework for SPAs)
- No base64 inline images (bloat); use relative paths or CDN URLs
- Component library covers common patterns; custom components follow the token system

## Edge Cases

- **No brand config:** Generate with neutral defaults; add comment noting customization needed
- **Missing font links:** Fall back to system-ui sans-serif
- **Dark mode preference:** Support `prefers-color-scheme: dark` media query if config includes dark mode tokens
- **RTL languages:** Add `dir="rtl"` to html element; mirror layout accordingly

## Validation Gate

- [ ] All colors from brand config (no hardcoded hex outside tokens)
- [ ] Typography uses configured display + body fonts
- [ ] Wordmark renders correctly on both light and dark backgrounds
- [ ] WCAG AA contrast on all text
- [ ] Responsive at mobile, tablet, desktop
- [ ] Single-file HTML, no external dependencies besides fonts
- [ ] No ALL CAPS headlines
- [ ] Brand accent used for CTAs, highlights, borders consistently

---
**Author:** Javier Montano | **Last updated:** March 18, 2026

## Usage

Example invocations: [EXPLICIT]

- "/brand-html" — Run the full brand html workflow
- "brand html on this project" — Apply to current context

