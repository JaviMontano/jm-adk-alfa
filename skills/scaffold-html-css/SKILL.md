---
name: scaffold-html-css
description: Production HTML5/CSS3/JS project scaffold. Semantic structure, responsive grid, design tokens, Hostinger-ready deployment. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [frontend, scaffold, html, css, hostinger]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# scaffold-html-css {Frontend} (v1.0)
> **"Ship pixels that perform, accessible by default."**
## Purpose
Production HTML5/CSS3/JS project scaffold. Semantic structure, responsive grid, design tokens, Hostinger-ready deployment. [EXPLICIT]
**When to use:** Frontend development within the Firebase/Google/Hostinger stack.
## Core Principles
1. **Law of Semantics:** HTML first, CSS second, JS third. Semantic markup is non-negotiable. [EXPLICIT]
2. **Law of Performance:** Lighthouse > 90. Lazy load images. Code-split routes. Critical CSS inline. [EXPLICIT]
3. **Law of Accessibility:** WCAG 2.1 AA minimum. Keyboard navigable. Screen reader tested. ARIA where needed. [EXPLICIT]
## Core Process
### Phase 1: Structure
1. Define page/component structure with semantic HTML5. [EXPLICIT]
2. Apply design tokens from `.agent/.shared/design-tokens.md`. [EXPLICIT]
3. Configure responsive breakpoints (mobile-first). [EXPLICIT]
### Phase 2: Build
1. Implement with framework (React/Angular) or vanilla HTML/CSS/JS. [EXPLICIT]
2. Integrate Firebase services (Auth, Firestore listeners, Storage). [EXPLICIT]
3. Add loading/error states for async operations. [EXPLICIT]
### Phase 3: Validate
1. Run Lighthouse audit (> 90 on all categories). [EXPLICIT]
2. Run accessibility audit (axe-core). [EXPLICIT]
3. Test on mobile, tablet, desktop breakpoints. [EXPLICIT]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Requirements/spec | Text/File | Yes | What to build |
| Output | Type | Description |
|--------|------|-------------|
| Source files | HTML/CSS/JS/TSX | Production-ready code |
## Validation Gate
- [ ] Semantic HTML5 structure
- [ ] Responsive on all breakpoints
- [ ] Lighthouse > 90
- [ ] WCAG 2.1 AA compliant
- [ ] Firebase integration working
## 5. Self-Correction Triggers
> [!WARNING]
> IF using div soup without semantic elements THEN refactor to semantic HTML5.
> IF Lighthouse < 90 THEN optimize before shipping.

## Usage

Example invocations:

- "/scaffold-html-css" — Run the full scaffold html css workflow
- "scaffold html css on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
