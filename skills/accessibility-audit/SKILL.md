---
name: accessibility-audit
description: Audit a digital UI (web app, route list, React/HTML component, or static markup) against WCAG 2.1 AA. Combines automated axe-core scanning with manual verification of keyboard, screen reader, contrast, forms, focus, dynamic content, and motion, then emits an evidence-backed report with a pass/conditional/fail/not-verified verdict and owner-ready remediation tickets. USE when the request is about web/app accessibility, WCAG, a11y, axe, keyboard-only or screen-reader behavior, color contrast, or ARIA. DO NOT use for physical-space accessibility, financial/credit access, API rate-limit "accessibility", or pure code remediation without an audit (it reports findings by default and only patches code on explicit request).
version: 1.0.0
status: production
owner: Javier Montaño
tags: [testing, accessibility, wcag, axe-core, a11y, screen-reader, keyboard-nav]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 082 — Accessibility Audit {Testing}

## Purpose
Audit digital interfaces against WCAG 2.1 AA using automated axe-core scanning plus structured manual checks for keyboard, screen reader behavior, color contrast, forms, focus management, dynamic content, and semantic structure. [EXPLICIT]
The default output is an evidence-backed accessibility audit report, not a code remediation patch. Code edits require an explicit remediation request. [EXPLICIT]

## Physics — 3 Immutable Laws

1. **Law of Universal Access**: If a sighted mouse user can do it, a keyboard-only or screen reader user must also be able to do it. No exceptions. [EXPLICIT]
2. **Law of Automated First, Manual Finality**: Automated scans find important issues but do not prove WCAG conformance. Run automation first, then manually verify the remaining criteria before making compliance claims. [EXPLICIT]
3. **Law of Evidence Before Compliance**: Do not claim "WCAG compliant" unless automated results, manual checks, scope, exceptions, and remediation status are documented. [EXPLICIT]

## Protocol

### Phase 0 — Scope and Evidence Setup
1. Identify audit target: URL, local app command, route list, component list, design artifact, or supplied HTML. [EXPLICIT]
2. Record environment: browser, viewport set, assistive technology used, auth/session state, and test date. [EXPLICIT]
3. If there is no runnable target, source artifact, or route/component list, return a gap report and do not claim compliance. [EXPLICIT]

### Phase 1 — Automated Scanning
1. Select the available runner: `axe-core`, `@axe-core/playwright`, `axe-playwright`, `cypress-axe`, `jest-axe`, or equivalent project-local tooling. [EXPLICIT]
2. Run scans against each route/component in scope and save machine-readable evidence when the environment permits. [EXPLICIT]
3. Report scan command, target, rule id, impact, affected selector, WCAG tags, and artifact path for every violation. [EXPLICIT]
4. Treat automated "no violations" as "no automated violations found", not as full WCAG compliance. [EXPLICIT]

### Phase 2 — Manual Checklist
1. **Keyboard navigation**: Verify tab order, visible focus, skip links, focus trap, return focus, escape behavior, and keyboard activation for custom controls. [EXPLICIT]
2. **Screen reader**: Verify page title, headings, landmarks, names/roles/values, form labels, error announcements, status updates, and modal announcements with VoiceOver, NVDA, or the available runner. [EXPLICIT]
3. **Contrast and visual states**: Verify 4.5:1 for normal text, 3:1 for large text, non-text contrast for UI controls/icons, focus indicator visibility, and color-not-alone signaling. [EXPLICIT]
4. **Responsive and motion**: Verify reflow at narrow widths, zoom behavior, orientation assumptions, `prefers-reduced-motion`, and pause/stop/hide controls for moving content. [EXPLICIT]

### Phase 3 — Remediation
1. Prioritize by user impact, WCAG level, blocker status, and recurrence across components; do not rely only on axe severity. [EXPLICIT]
2. Each remediation ticket must include target, selector/component, reproducer, WCAG criterion, user impact, expected behavior, evidence artifact, and acceptance check. [EXPLICIT]
3. If remediation is requested, make the smallest safe patch and rerun the relevant automated/manual checks. [EXPLICIT]
4. If remediation is not requested, produce owner-ready tickets and status: `pass`, `conditional`, `fail`, or `not verified`. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| React/HTML component | axe-core violation report (JSON/HTML) + manual checklist for that component |
| Route list | Per-route automated scan results + scope coverage table |
| Running app URL or app command | Full automated + manual audit with environment record |
| Manual audit checklist | Completed checklist with pass/fail/not-verified per criterion |
| Violation report | Remediation tickets with WCAG reference and acceptance check |
| No runnable target or artifact | Gap report listing required inputs, status `not verified` |

## Routing Boundary

Activate ONLY for digital WCAG/a11y audits. Hard non-matches (ask for clarification or decline, do NOT audit):
- Physical accessibility (building entrances, ramps, parking). [EXPLICIT]
- Financial/credit "access" (SMB credit access, banking inclusion). [EXPLICIT]
- API/network "accessibility" (uptime, rate limits, reachability). [EXPLICIT]
- A bare "fix accessibility" with no target and no evidence → return a gap report, do not invent findings. [EXPLICIT]

## Quality Gates — 5 Checks

1. **Zero unresolved WCAG 2.1 AA failures** in scope, or each exception has owner, rationale, expiry, and risk acceptance. [EXPLICIT]
2. **Automated evidence present**: command/tool, target, rule id, impact, selector, WCAG tags, and report artifact are recorded when runnable. [EXPLICIT]
3. **Manual evidence present**: keyboard, screen reader, contrast, forms/errors, focus, dynamic content, motion, and responsive checks are pass/fail/not-verified with notes. [EXPLICIT]
4. **No unsupported compliance claim**: final status is `pass`, `conditional`, `fail`, or `not verified`; "compliant" requires all in-scope checks passing or documented exceptions. [EXPLICIT]
5. **Owner-ready remediation**: every finding has severity, WCAG criterion, user impact, reproducer, expected behavior, and acceptance check. [EXPLICIT]

## Edge Cases

- **Dynamic content**: Use `aria-live="polite"` for async updates (toasts, loaders).
- **Modals**: Trap focus inside modal. Return focus to trigger on close.
- **Custom components**: `<div>` buttons need `role="button"`, `tabindex="0"`, `onKeyDown` for Enter/Space.
- **SVG icons**: Add `aria-hidden="true"` for decorative. `role="img"` + `aria-label` for meaningful.
- **ARIA overuse**: Prefer native HTML before adding ARIA. Remove redundant or misleading roles.
- **Clean axe report with manual failure**: Overall status remains `fail` or `conditional`; automation cannot override manual blockers.

## Anti-Patterns

- **"axe is clean, so we are WCAG AA compliant."** Automated scans cover roughly 30-40% of WCAG criteria. A clean scan with skipped manual checks is `conditional` or `not verified`, never `pass`. [EXPLICIT]
- **ARIA-as-default.** Adding `role`/`aria-*` to native elements (`<button>`, `<h2>`, `<nav>`) is a regression, not a fix. Prefer native HTML; reach for ARIA only to repair semantics native elements cannot provide. [EXPLICIT]
- **Severity = axe impact.** axe `critical/serious/moderate/minor` is a starting signal, not the priority. Re-rank by user-task blocking, WCAG level, and recurrence across components. [EXPLICIT]
- **Findings without a reproducer.** "Contrast is low somewhere" is not a ticket. Every finding names target, selector/component, steps, expected behavior, and acceptance check. [EXPLICIT]
- **Auditing the design mock instead of the rendered DOM.** Contrast, focus order, and announcements must be verified on the running build or supplied markup, not inferred from a Figma frame. [EXPLICIT]
- **Silent scope shrink.** Routes/components that could not be run are recorded as `not verified`, never dropped to make the report look green. [EXPLICIT]

## Self-Correction Triggers

- axe violation count increases between releases → block deploy, remediate.
- Screen reader test skipped → flag in PR review checklist.
- New component lacks a11y test → component review blocks approval.
- Contrast check fails on new theme → update design tokens before merge.

## Usage

Example invocations:

- "/accessibility-audit" — Run the full accessibility audit workflow
- "accessibility audit on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- If no runnable target or artifact is available, produce a gap report with required inputs instead of an audit verdict. [EXPLICIT]
