# Accessibility Audit — Body of Knowledge

## Canon

Accessibility audit quality depends on separating automated evidence from
manual verification. Automated tools are necessary but insufficient. A valid
audit records scope, environment, in-scope routes/components, automated results,
manual checks, WCAG references, user impact, and remediation acceptance checks.

## WCAG 2.1 AA Audit Map

| Area | Examples to Check | Evidence |
|---|---|---|
| Keyboard | Tab order, focus visibility, skip link, escape behavior, custom control activation, modal focus trap and return focus. | Manual pass/fail/not-verified notes per route/component. |
| Screen reader | Page title, headings, landmarks, names/roles/values, form labels, error announcements, status updates, modal announcement. | Assistive technology, browser, expected announcement, observed result. |
| Contrast | Normal text 4.5:1, large text 3:1, non-text UI/icon contrast 3:1, focus indicator visibility. | Measured ratio or tool evidence. |
| Forms and errors | Visible labels, instructions, required state, error identification, error suggestion, programmatic association. | Selector/component and expected behavior. |
| Semantics | Landmarks, heading order, lists, buttons/links, tables, alt text, decorative image hiding. | DOM/HTML evidence. |
| Dynamic content | Toasts, loaders, async results, validation updates, live regions. | Interaction steps and announcement behavior. |
| Motion and responsive | Reduced motion, pause/stop/hide, reflow, zoom, orientation assumptions. | Viewport/OS setting and result. |

## Status Model

| Status | Meaning |
|---|---|
| `pass` | All in-scope automated and manual checks pass, or exceptions are documented and accepted. |
| `conditional` | No blocking issue remains, but moderate/low-risk exceptions or not-verified areas need owner follow-up. |
| `fail` | One or more WCAG 2.1 AA blockers, serious user-impact issues, or missing critical evidence remain. |
| `not verified` | The target could not be run or the required artifact/evidence was not provided. |

## Finding Severity

| Severity | Use When |
|---|---|
| P1 blocker | Prevents keyboard/screen reader completion, blocks core task, exposes unusable form, or causes severe contrast/readability failure. |
| P2 major | Violates WCAG AA or creates substantial friction but a workaround exists. |
| P3 minor | Low-impact accessibility improvement, documentation gap, or polish item. |

## Remediation Ticket Contract

Every finding should include target, route/component, selector if available,
WCAG criterion or accessibility principle, user impact, reproduction steps,
expected behavior, evidence artifact, proposed fix, and acceptance check.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Scope coverage | 100% | Every in-scope route/component has automated or not-verified status |
| Manual coverage | 100% | Keyboard, screen reader, contrast, forms/errors, focus, dynamic content, motion, and responsive checks recorded |
| WCAG mapping | 100% | Findings include WCAG criterion or documented accessibility principle |
| Evidence coverage | 100% | Claims tagged with evidence, assumption, or not-verified status |
| Remediation readiness | 100% | Findings include owner-ready reproduction and acceptance checks |

## References
- WCAG 2.1 AA is the default target because the skill purpose names it.
- Use project-local axe, Playwright, Cypress, Jest, Storybook, or browser tools when present.
- Prefer native HTML semantics before ARIA. Use ARIA to repair missing semantics only when native controls cannot be used.
