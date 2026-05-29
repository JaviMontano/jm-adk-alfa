---
name: accessibility-testing
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Plan, execute, and report web accessibility tests with axe-core,
  Playwright/Jest evidence, keyboard scripts, screen reader smoke checks,
  color contrast validation, and explicit WCAG target scope. [EXPLICIT]
  Trigger: "accessibility test", "a11y test", "WCAG test", "screen reader",
  "axe-core", "keyboard accessibility"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Accessibility Testing

> "The power of the web is in its universality. Access by everyone regardless of disability is an essential aspect." — Tim Berners-Lee

## TL;DR

Guides accessibility testing as an evidence-producing workflow: define scope, run automated checks where possible, execute manual keyboard and assistive-technology smoke tests, record contrast and motion results, and produce a pass/fail/not-verified report. Use for test plans, regression suites, QA reports, and retest evidence. Do not claim WCAG compliance without explicit target, scope, date, tested technologies, and evidence. [EXPLICIT]

## Procedure

### Step 1: Discover
- Capture the accessibility target: WCAG version/level, routes, components, flows, browsers, viewports, auth state, and assistive technology pairings.
- Inventory dynamic states that must be opened before testing: menus, dialogs, tooltips, form errors, toasts, accordions, route changes, and live regions.
- Identify available tooling: axe-core, `@axe-core/playwright`, `jest-axe`, browser-rendered contrast checks, visual/focus evidence, CI, and manual test notes.
- Record known issues, exclusions, and suppressions with owner, issue ID, selector, rule ID, expiry, and re-enable criteria.

### Step 2: Analyze
- Map each test to an observable expectation, artifact, and status: `pass`, `fail`, `conditional`, or `not verified`.
- Separate automated evidence from manual evidence; a clean axe run is not a full accessibility or WCAG conformance claim.
- Prioritize risks by user impact: blocker, high, medium, low, or observation.
- Choose manual scripts for focus order, focus trapping/restoration, keyboard activation, screen reader announcements, contrast, zoom/reflow, reduced motion, and dynamic content.

### Step 3: Execute
- Produce or run automated tests with route/component/state coverage; scan after interactions, not just first page load.
- Produce keyboard scripts covering Tab, Shift+Tab, Enter, Space, Escape, arrow keys where relevant, skip links, focus visibility, focus trap, and focus restoration.
- Produce screen reader smoke scripts with OS/browser/AT pairing, expected announcement, observed announcement, and pass/fail status.
- Record contrast evidence for normal text, large text, non-text UI, placeholder, disabled, focus, hover, and error states, or mark gaps as `not verified`.
- Create remediation tickets or backlog items only when remediation is requested; otherwise report issues with evidence and recommended owner.

### Step 4: Validate
- Every claim has a command, artifact, observation, or explicit `not verified` marker.
- Automated findings include command/tool version, route or component, state, rule ID, impact, selector, WCAG tags when available, and artifact path.
- Manual findings include script step, expected result, observed result, evidence, severity, and retest status.
- Final status avoids blanket "compliant" language unless the full conformance scope is documented and evidenced.

## Quality Criteria

- [ ] Scope and environment are explicit: target, routes/components/states, browser, viewport, assistive technology, date, and tool versions.
- [ ] Automated evidence is scoped and reproducible; single body scans and unopened dynamic states are rejected as insufficient proof.
- [ ] Keyboard evidence covers forward/reverse tab order, activation keys, escape paths, focus visibility, traps, restoration, and route-change focus.
- [ ] Screen reader evidence is labeled as smoke, regression, or full manual test and includes expected vs observed announcements.
- [ ] Contrast and reduced-motion results are recorded, or each gap is marked `not verified` with next action.
- [ ] Suppressions have issue ID, owner, expiry, selector, rule ID, reason, and re-enable criteria.
- [ ] No WCAG conformance claim is made without scope, target level, tested technologies, date, and evidence.
- [ ] Evidence tags applied to all claims.

## Anti-Patterns

- Treating automated tools as complete proof of accessibility or WCAG conformance
- Adding ARIA attributes to elements that already have native semantics
- Using `outline: none` without providing alternative focus indicators
- Scanning only the initial DOM while ignoring opened menus, dialogs, form errors, and live updates
- Broadly excluding selectors from axe without owner, expiry, and re-enable criteria
- Mixing testing with remediation without explicit user approval

## Related Skills

- `accessibility-audit` — use for broader governance, policy, and compliance audit scope
- `accessibility-design` — use for designing accessible interaction patterns and UI changes
- `modal-dialog-patterns` — focus management is critical for modal accessibility
- `navigation-patterns` — navigation is the most common a11y failure area

## Usage

Example invocations:

- "/accessibility-testing" — Run the full accessibility testing workflow
- "accessibility testing on this project" — Apply to current context


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
