---
name: accessibility-design
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Designs the accessible interaction contract for a web UI component or flow
  BEFORE or DURING build: native-HTML-first semantics, targeted ARIA only when
  native is insufficient, keyboard interaction maps, focus management (initial,
  trap, return, route-change), screen reader name/role/value/state expectations,
  contrast and focus-indicator token requirements, accessible forms with error
  recovery, live regions, reduced motion, and WCAG 2.1 AA acceptance criteria.
  [EXPLICIT]
  Use WHEN the deliverable is a design/implementation spec a developer or tester
  can build and verify against (e.g. "make this modal/tabs/combobox/form
  accessible", "spec keyboard and focus behavior", "what ARIA does this widget
  need"). Do NOT use to scan an existing app for violations or to write/run test
  automation: route those to `accessibility-audit` and `accessibility-testing`.
  Out of scope: physical/built-environment accessibility, non-web platforms
  unless explicitly web-rendered, and general visual design unrelated to a11y.
  Trigger: "accessibility", "WCAG", "ARIA", "a11y", "screen reader", "keyboard navigation", "focus management", "inclusive design", "accessible component/form/modal"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Accessibility Design

> "The power of the Web is in its universality. Access by everyone regardless of disability is an essential aspect." — Tim Berners-Lee

## TL;DR

Designs or implements accessible web UI behavior before or during feature
delivery. [EXPLICIT]
Use this skill to produce component-level accessibility requirements, semantic
HTML/ARIA decisions, keyboard maps, focus rules, contrast/token requirements,
form/error behavior, and acceptance criteria. [EXPLICIT]
Use `accessibility-audit` or `accessibility-testing` when the primary task is
to discover/report violations rather than design the solution. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the feature, component, user journey, interaction states, target
  users, device constraints, and existing design system tokens/components. [EXPLICIT]
- Capture required controls, content, validation states, dynamic updates,
  responsive behavior, motion behavior, and success/failure paths. [EXPLICIT]
- If the request is only to find violations, route to `accessibility-audit` or
  `accessibility-testing`; this skill owns accessible design and implementation
  specifications. [EXPLICIT]

### Step 2: Analyze
- Apply the native-first ladder in order; stop at the first rung that satisfies
  the requirement: (1) native HTML element, (2) native element + minimal
  attributes (`type`, `for`, `required`, `disabled`), (3) native element + one
  ARIA state/relationship (`aria-expanded`, `aria-describedby`, `aria-current`),
  (4) full ARIA widget pattern from APG only when no native element exists
  (combobox, tablist, tree). [EXPLICIT]
- Choose native HTML semantics first: buttons, links, headings, labels, fieldsets,
  lists, tables, landmarks, and form controls before custom ARIA widgets. [EXPLICIT]
- For every custom component, define name, role, value/state, keyboard model,
  focus entry/exit, pointer alternative, screen reader announcement, and disabled
  behavior. [EXPLICIT]
- Map requirements to WCAG 2.1 AA / POUR areas and note acceptance criteria for
  each relevant state. [EXPLICIT]
- Identify design-token requirements for text contrast, non-text contrast, focus
  indicators, error states, disabled states, hover/focus/active states, and color
  not being the only signal. [EXPLICIT]

### Step 3: Execute
- Produce or update accessible implementation guidance, component specs, or code
  changes when explicitly requested. [EXPLICIT]
- Include keyboard interaction tables for dialogs, tabs, accordions, menus,
  combobox/listbox patterns, disclosures, toasts/live regions, forms, and skip
  links when those patterns are in scope. [EXPLICIT]
- Define focus management: initial focus, visible focus indicator, trap/containment
  when needed, return focus, route-change focus, and no focus stealing. [EXPLICIT]
- Define content requirements: accessible names, labels, descriptions, alt text,
  error copy, status messages, plain language, and sensory-independent cues.
  [EXPLICIT]

### Step 4: Validate
- Verify the output includes component behavior, semantic/ARIA decision log,
  keyboard map, focus plan, screen reader expectations, contrast/token evidence
  or not-verified status, and acceptance criteria. [EXPLICIT]
- Validate that ARIA is not used redundantly on native controls and that
  `aria-hidden` does not hide focusable or meaningful content. [EXPLICIT]
- Provide a test matrix for automated checks, keyboard, screen reader smoke,
  contrast/non-text contrast, reduced motion, 200% zoom/reflow, and forced colors
  when relevant. [EXPLICIT]

## Quality Criteria

- [ ] All interactive elements are keyboard accessible
- [ ] Native HTML is used before ARIA, and every ARIA use has a clear purpose
- [ ] Accessible name, role, value/state, and description are specified for custom controls
- [ ] Color contrast meets WCAG AA ratios for text and non-text UI states
- [ ] Forms have visible labels, programmatic labels, error messages, descriptions, and recovery flow
- [ ] Focus order, focus visibility, focus return, and route-change focus are specified
- [ ] Reduced motion, zoom/reflow, and sensory-independent cues are addressed
- [ ] Acceptance criteria and validation matrix are included

## Anti-Patterns

- ARIA overuse: adding roles to elements that are already semantic (role="button" on a button)
- Visible focus removal (`outline: none`) without replacement
- Color as the only means of conveying information
- `aria-label` that hides or contradicts visible text
- Focusable content inside `aria-hidden="true"`
- Custom widgets without a keyboard interaction model
- `div`/`span` with click handlers instead of a `button` (loses role, keyboard, focus)
- Placeholder used as the only label
- `tabindex` greater than 0 to reorder focus
- Live region added after content changes (must exist in the DOM before the update)
- Claiming "WCAG AA compliant" without contrast measurement or AT verification evidence

## Related Skills

- `html-semantic` — semantic HTML is the foundation of accessibility
- `form-engineering` — accessible form patterns and validation
- `responsive-design` — responsive and accessible design overlap significantly
- `accessibility-audit` — use when the primary output is an audit report
- `accessibility-testing` — use when the primary output is test automation or manual test execution

## Usage

Example invocations:

- "/accessibility-design" — Run the full accessibility design workflow
- "accessibility design on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- If contrast ratios, runtime behavior, or assistive technology output cannot be
  verified, mark them as not verified and provide the needed evidence. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Request to find/report violations | Route to `accessibility-audit` (report) or `accessibility-testing` (automation) |
| Physical/built-environment accessibility | Out of scope; this skill owns digital web UI behavior only |
| Contrast ratios or AT output not measurable | Mark `not verified`, state the evidence needed; never overclaim compliance |
| Native element exists for the need | Stop at the native rung; do not author a full ARIA widget pattern |
| Drag-and-drop or pointer-only gesture | Require a keyboard/single-pointer alternative (WCAG 2.5.7 / 2.1.1) |
