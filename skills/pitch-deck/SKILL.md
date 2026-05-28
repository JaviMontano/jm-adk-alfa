---
name: pitch-deck
description: >
  Triggers on "pitch deck", "investor deck", "presentation slides", "crear presentacion".
  Generates a self-contained HTML slide deck with JM Labs brand identity following the standard
  pitch sequence Cover-Problem-Solution-Market-Model-Team-Ask. Output: single HTML file with
  slide navigation, bilingual support, and print-ready styles. [EXPLICIT]
argument-hint: "company name, problem statement, solution, market size, business model, team, ask amount"
model: opus
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Pitch Deck

> TL;DR — Produces a complete investor-grade pitch deck as a single self-contained HTML file.
> Follows the proven 10-slide sequence, applies JM Labs brand tokens (navy, gold, blue,
> Poppins/Inter, dark-first), includes keyboard navigation, bilingual ES/EN toggle, and
> print-to-PDF styles.

---

## When to Activate

| Signal | Example |
|--------|---------|
| Deck creation request | "Build me a pitch deck for investors" |
| Slide-specific ask | "I need a problem-solution slide" |
| Spanish variant | "Necesito crear una presentacion para inversionistas" |
| Fundraising context | "We're raising a seed round, need a deck" |
| Demo day prep | "Help me prepare slides for demo day" |

Activate when the user needs a structured presentation deck for pitching a business, product,
or idea. Do NOT activate for internal meeting presentations (use `presentation-design`) or
keynote talks (use `workshop-proposal`).

---

## S1 — Content Architecture

### Standard Slide Sequence

| Slide | Title | Purpose | Max Duration |
|-------|-------|---------|-------------|
| 1 | Cover | Company name, tagline, presenter | 15s |
| 2 | Problem | Pain point with evidence | 60s |
| 3 | Solution | Product/service and how it solves the problem | 60s |
| 4 | Demo/Product | Screenshots, workflow, key features | 90s |
| 5 | Market | TAM, SAM, SOM with sources | 45s |
| 6 | Business Model | Revenue streams, pricing, unit economics | 60s |
| 7 | Traction | Metrics, milestones, growth curves | 45s |
| 8 | Competition | Positioning matrix (NOT a feature grid) | 45s |
| 9 | Team | Key members with relevant credentials | 30s |
| 10 | Ask | Funding amount, use of funds, timeline | 30s |

Total target: 8-10 minutes. Each slide should convey ONE idea.

### Content Extraction Protocol

For each slide, extract from user input:
1. **Core message** — single sentence the audience must remember.
2. **Supporting data** — 1-3 data points, metrics, or proof elements.
3. **Visual anchor** — chart type, diagram, or image recommendation.

If the user provides insufficient data for a slide, mark it with `[NEEDS INPUT]` and list
specific questions to resolve.

---

## S2 — Visual Design System

### Brand Tokens

```css
:root {
  --navy:    #122562;
  --gold:    #FFD700;
  --blue:    #137DC5;
  --bg:      #0D1B2A;
  --surface: #1B2D45;
  --text:    #F0F0F0;
  --muted:   #8892A0;
  --font-heading: 'Poppins', sans-serif;
  --font-body:    'Inter', sans-serif;
}
```

### Slide Layout Rules

- **Dark-first** — all slides use dark background (#0D1B2A) with light text.
- **Aspect ratio** — 16:9 (1920x1080 viewport).
- **Typography scale** — slide title: 48px Poppins 700, subtitle: 28px Poppins 400,
  body: 20px Inter 400, caption: 14px Inter 300.
- **Maximum elements per slide** — 1 title + 1 subtitle + 3 content blocks or 1 chart.
- **Color usage** — gold for emphasis and CTAs, blue for data and links, navy for containers.
- **Whitespace** — minimum 80px padding on all edges; content occupies max 80% of slide area.

### Chart Guidelines

| Data Type | Recommended Chart | Library |
|-----------|------------------|---------|
| Market size (TAM/SAM/SOM) | Concentric circles | CSS only |
| Revenue growth | Line chart | Inline SVG |
| Competitive positioning | 2x2 matrix | CSS grid |
| Use of funds | Horizontal bar | CSS only |
| Team structure | Card grid | CSS flexbox |

Prefer CSS-only visuals to keep the HTML self-contained with zero external dependencies.

---

## S3 — HTML Implementation

### Architecture

Single HTML file with embedded CSS and JavaScript. No external dependencies except Google
Fonts (Poppins + Inter loaded via link tag with fallback system fonts).

### Navigation Features

```
Keyboard: ArrowRight/ArrowLeft or Space/Backspace
Touch: swipe left/right on mobile
Click: navigation dots at bottom center
Progress: thin gold bar at top indicating current position
```

### Bilingual Support

- Include a language toggle button (top-right corner): `EN | ES`.
- Each text element uses `data-en` and `data-es` attributes.
- JavaScript toggles `lang` attribute on `html` element and swaps visible text.
- Default language matches user's stated preference or defaults to ES.

### Print Styles

```css
@media print {
  .slide { page-break-after: always; }
  .nav, .lang-toggle, .progress { display: none; }
  :root { --bg: #FFFFFF; --text: #122562; }
}
```

Ensure each slide fits on one printed page in landscape orientation.

---

## S4 — Delivery & Iteration

### Export Options

| Format | Method | Notes |
|--------|--------|-------|
| HTML | Direct file | Open in any browser, present with F11 |
| PDF | Print to PDF | Landscape, no margins, background graphics ON |
| Images | Browser screenshot | Each slide as PNG for social media |

### Iteration Protocol

After delivering the initial deck:
1. Ask user to review each slide and provide feedback.
2. Accept slide-specific edits: "Change slide 5 market size to $4.2B".
3. Support reordering: "Move the traction slide before competition".
4. Support additions: "Add an appendix slide with detailed financials".

### Presentation Coaching Notes

Include a hidden `speaker-notes` div per slide (visible only in HTML source or via
keyboard shortcut `N`):
- Key talking points (3 bullets max).
- Transition phrase to next slide.
- Anticipated questions with suggested answers.

---

## Trade-off Matrix

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Slide count | 10 standard | 15+ detailed | 10 — investor attention is limited |
| Animation | CSS transitions | No animation | Subtle fade-in — professional not flashy |
| Data density | Charts + numbers | Minimal text | Balance — one key metric per slide |
| Dependencies | External libraries | Self-contained CSS | Self-contained — maximum portability |
| Language default | English first | Spanish first | Match user's primary audience |

---

## Assumptions & Limits

- Assumes the user provides accurate business data; the skill does not validate claims. [EXPLICIT]
- Does not generate real charts from live data sources — uses static visual representations. [EXPLICIT]
- HTML file targets modern browsers (Chrome, Firefox, Safari, Edge); no IE11 support. [EXPLICIT]
- Google Fonts require internet connection; fallback to system sans-serif when offline. [INFERRED]
- Does not integrate with presentation tools (PowerPoint, Google Slides, Keynote). [EXPLICIT]

---

## Edge Cases

1. **Pre-revenue startup** — Replace Traction slide with Vision/Roadmap; emphasize team
   credentials and market validation (letters of intent, waitlist numbers).
2. **Non-profit or social enterprise** — Replace Business Model with Impact Model; replace
   Ask with Partnership/Grant request; adjust language from ROI to social impact.
3. **Technical audience (demo day)** — Expand Demo/Product slide to 2-3 slides; add
   architecture diagram; reduce market sizing to one slide.
4. **User provides only a one-line idea** — Enter discovery mode: ask 8-10 structured
   questions covering problem, solution, market, model, team, and ask before generating.

---

## Good vs Bad Example

### Good

```html
<!-- Problem Slide -->
<section class="slide" data-slide="2">
  <h2 data-en="The Problem" data-es="El Problema">The Problem</h2>
  <p class="stat" data-en="73% of SMBs lose $10K+/year to manual invoicing"
     data-es="73% de las PyMEs pierden $10K+/anio en facturacion manual">
    73% of SMBs lose $10K+/year to manual invoicing
  </p>
  <div class="speaker-notes">
    Source: Intuit SMB Survey 2024. Transition: "That's why we built..."
  </div>
</section>
```

Why it works: single metric, bilingual, speaker notes, clean structure.

### Bad

```html
<div>
  <h1>Problems</h1>
  <ul>
    <li>Invoicing is hard</li>
    <li>Takes too long</li>
    <li>People don't like it</li>
    <li>It costs money</li>
    <li>There are errors</li>
    <li>No automation</li>
  </ul>
</div>
```

Why it fails: no data, bullet-point overload, no brand styling, no bilingual support.

---

## Validation Gate

Before delivering the final HTML deck, confirm every item:

- [ ] HTML file is self-contained with no external JS dependencies
- [ ] All 10 standard slides are present (or justified substitutions documented)
- [ ] Brand tokens applied: navy #122562, gold #FFD700, blue #137DC5
- [ ] Typography uses Poppins for headings and Inter for body text
- [ ] Dark-first design with proper contrast ratios (WCAG AA minimum)
- [ ] Keyboard navigation works (ArrowLeft, ArrowRight, Space)
- [ ] Bilingual toggle switches all visible text between ES and EN
- [ ] Print stylesheet produces one slide per landscape page
- [ ] Speaker notes included for each slide (hidden by default)
- [ ] No slide contains more than one core message
- [ ] Slides marked [NEEDS INPUT] when user data is insufficient

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/slide-templates.html` | HTML template for each slide type |
| `references/pitch-frameworks.md` | YC, Sequoia, and Guy Kawasaki deck structures |
| `references/chart-patterns.css` | CSS-only chart implementations |
| `references/speaker-notes-guide.md` | How to write effective speaker notes |
