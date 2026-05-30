---
name: accessibility-testing
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Plan, execute, and report web accessibility tests as reproducible evidence:
  stateful axe-core scans (@axe-core/playwright, jest-axe), keyboard-only
  matrices, screen reader smoke scripts (VoiceOver/Safari, NVDA/Firefox),
  color and non-text contrast checks, reduced-motion and zoom/reflow regression,
  governed suppressions, and an explicit WCAG target with pass/fail/conditional/
  not-verified status. Use when someone needs a11y test plans, regression suites,
  QA reports, or retest evidence on a web UI. NOT for compliance governance/policy
  audits (use accessibility-audit), NOT for designing accessible patterns (use
  accessibility-design), and never emits a WCAG-conformance claim without target,
  scope, tested technologies, date, and evidence. [EXPLICIT]
  Trigger: "accessibility test", "a11y test", "WCAG test", "screen reader test",
  "axe-core run", "keyboard accessibility test", "contrast check"
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

## Inputs Required (resolve before Step 3)

| Input | If missing | Default if user defers |
|-------|-----------|------------------------|
| WCAG target version + level | Ask once | WCAG 2.2 AA (test target, not a claim) |
| Routes / components / flows in scope | Ask once | Refuse a blanket pass; scope only what is named |
| Dynamic states to open | Inventory from code/DOM | Mark unopened states `not verified` |
| Browser + viewport set | Ask once | Chromium desktop; note mobile as `not verified` |
| AT pairings | Ask once | VoiceOver/Safari + NVDA/Firefox scripts, execution `not verified` |
| Remediation authorized? | Ask once | No — produce findings + retest only |
| Available tooling | Detect from lockfile/config | Document scripts as runnable-pending |

Treat the answers as a signed contract. Echo them back in the Scope table verbatim; every later status inherits from this scope.

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
- Produce or run automated tests with route/component/state coverage; scan **after** each interaction, not just first page load. Stateful pattern: `await page.getByRole('button', { name: 'Pay now' }).click(); const r = await new AxeBuilder({ page }).include('[role=dialog]').analyze(); expect(r.violations).toEqual([])`. For component semantics use `expect(await axe(container)).toHaveNoViolations()` (jest-axe), and flag that jest-axe does NOT cover browser-rendered contrast or live keyboard behavior.
- Produce keyboard scripts covering Tab, Shift+Tab, Enter, Space, Escape, arrow keys where relevant, skip links, focus visibility, focus trap, and focus restoration. Each row is one step with explicit keys and an expected focus target by accessible name.
- Produce screen reader smoke scripts with OS/browser/AT pairing, expected announcement, observed announcement, and pass/fail status. Cover landmarks, headings, name/role/value, form errors, live regions, dialog semantics, and reading order.
- Record contrast evidence for normal text, large text, non-text UI, placeholder, disabled, focus, hover, and error states, or mark gaps as `not verified`. State the threshold used (4.5:1 normal text, 3:1 large text and non-text UI) next to each ratio.
- Test `prefers-reduced-motion: reduce` for non-essential motion (Playwright: `browser.newContext({ reducedMotion: 'reduce' })`) and 200% zoom / 320 CSS px reflow where in scope.
- Create remediation tickets or backlog items only when remediation is requested; otherwise report issues with evidence and recommended owner.

**Status decision rule** (apply per row, then roll up): evidence collected + no issue → `pass`; evidence collected + ≥1 issue → `fail`; partial/blocked with documented mitigation → `conditional`; no evidence collected → `not verified`. The overall status is the worst not-`pass` state present; a report containing any `not verified` in-scope item is at best `conditional`, never `pass`.

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
