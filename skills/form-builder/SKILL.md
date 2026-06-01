---
name: form-builder
description: Complex form construction. Multi-step, conditional fields, validation (Zod + React Hook Form / Angular Reactive Forms), Firebase submission. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [frontend, forms, validation, multi-step]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# form-builder {Frontend} (v1.0)
> **"Ship pixels that perform, accessible by default."**
## Purpose
Complex form construction. Multi-step, conditional fields, validation (Zod + React Hook Form / Angular Reactive Forms), Firebase submission. [EXPLICIT]
**When to use:** Frontend development within the Firebase/Google/Hostinger stack.
## Core Principles
1. **Law of Semantics:** HTML first, CSS second, JS third. Semantic markup is non-negotiable. [EXPLICIT]
2. **Law of Performance:** Lighthouse > 90. Lazy load images. Code-split routes. Critical CSS inline. [EXPLICIT]
3. **Law of Accessibility:** WCAG 2.1 AA minimum. Keyboard navigable. Screen reader tested. ARIA where needed. [EXPLICIT]
## Core Process
### Phase 1: Structure
1. Define page/component structure with semantic HTML5. [EXPLICIT]
2. Apply reusable assets from `assets/`: `form-control.css`, `form-step-template.html`, and `validation-policy.json`. [EXPLICIT]
3. Configure responsive breakpoints (mobile-first). [EXPLICIT]
### Phase 2: Build
1. Implement with framework (React/Angular) or vanilla HTML/CSS/JS. [EXPLICIT]
2. Integrate Firebase services (Auth, Firestore listeners, Storage). [EXPLICIT]
3. Add loading/error states for async operations. [EXPLICIT]
4. When input is structured, render a deterministic semantic prototype with `scripts/render-form-schema.py --schema <schema.json>`. [EXPLICIT]
### Phase 3: Validate
1. Run Lighthouse audit (> 90 on all categories). [EXPLICIT]
2. Run accessibility audit (axe-core). [EXPLICIT]
3. Test on mobile, tablet, desktop breakpoints. [EXPLICIT]
4. Run `scripts/check.sh` or `scripts/render-form-schema.py` fixtures when changing bundled form assets. [EXPLICIT]
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
- [ ] `assets/manifest.json` declares every reusable form asset
- [ ] Scripted schema rendering includes labels, fieldsets, hints, and submit button
- [ ] Conditional fields reference a driver field that appears earlier in the schema
## 5. Self-Correction Triggers
> [!WARNING]
> IF using div soup without semantic elements THEN refactor to semantic HTML5.
> IF Lighthouse < 90 THEN optimize before shipping.

## Usage

Example invocations:

- "/form-builder" — Run the full form builder workflow
- "form builder on this project" — Apply to current context

## Deterministic Script Contract

- Runtime script: `scripts/render-form-schema.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks --skill form-builder`
- Default behavior: render to stdout; write files only with `--output`.
- Safety boundary: invalid schemas fail nonzero instead of producing inaccessible or ambiguous forms.

## Assets Contract

- Output assets live in `assets/`.
- `assets/manifest.json` lists every reusable asset and where it is used.
- `assets/form-control.css` provides minimal accessible styling.
- `assets/form-step-template.html` provides the canonical semantic step wrapper.
- `assets/validation-policy.json` defines allowed field types and accessibility policy.


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
