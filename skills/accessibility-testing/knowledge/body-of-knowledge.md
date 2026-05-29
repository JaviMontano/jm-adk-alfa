# Accessibility Testing — Body of Knowledge

## Canon

Accessibility testing converts inclusive design intent into reproducible evidence. The skill must separate three things:

1. automated checks that can be rerun;
2. manual observations that need human or assistive-technology judgment;
3. claims that remain `not verified`.

The default testing target is WCAG 2.2 AA unless the user gives a different target. This is a test target, not an automatic conformance claim.

## Evidence Model

| Evidence type | Required fields | Notes |
| --- | --- | --- |
| Scope | target, routes/components, states, browser, viewport, auth state, date | Without scope, results are not portable. |
| Automation | command, tool/version, route/component, state, rule ID, impact, selector, artifact path | Use axe-core, `@axe-core/playwright`, `jest-axe`, or equivalent. |
| Keyboard | step, keys, expected focus/action, observed result, pass/fail, evidence | Include Tab, Shift+Tab, Enter, Space, Escape, arrows where relevant. |
| Screen reader | OS, browser, AT, flow, expected announcement, observed announcement, status | Label as smoke, regression, or full manual test. |
| Contrast | token/selector, foreground/background, state, ratio, threshold, status | Include normal, large, non-text, placeholder, disabled, focus, hover, and error states when relevant. |
| Motion | preference, scenario, expected behavior, observed behavior, status | Test `prefers-reduced-motion` for non-essential movement. |
| Suppression | issue ID, owner, expiry, selector, rule ID, reason, re-enable criteria | Broad exclusions hide risk and need explicit governance. |

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Scope coverage | 100% of declared routes/components/states | Matrix has status for each in-scope item |
| Evidence coverage | 100% | Each claim maps to command, artifact, observation, or `not verified` |
| Automation reproducibility | 100% for runnable automated checks | Commands and tool versions are listed |
| Manual coverage clarity | 100% | Keyboard, screen reader, contrast, and motion are pass/fail/not-verified |
| Claim safety | 100% | No blanket conformance claim without explicit scope and evidence |

## Status Semantics

- `pass`: tested with evidence and no issue found for the declared expectation.
- `fail`: tested with evidence and at least one issue found.
- `conditional`: partially tested or blocked by known limitation with a documented mitigation.
- `not verified`: no evidence was collected; this is not a pass.

## Severity Model

| Severity | User impact | Example |
| --- | --- | --- |
| Blocker | Prevents task completion for keyboard or AT users | Modal traps focus with no Escape path |
| High | Major friction or data-entry failure | Required field error is not announced |
| Medium | Repeated difficulty or inconsistent semantics | Icon button has unclear accessible name |
| Low | Localized polish issue | Decorative image lacks empty alt |
| Observation | Contextual improvement | Heading structure could be easier to scan |

## Test Design Notes

- Automated tests should open relevant dynamic states before scanning.
- `jest-axe` is useful for component semantics, but browser-rendered contrast and interaction behavior need a browser or manual evidence.
- Keyboard testing needs both forward and reverse focus movement.
- Screen reader smoke tests should cover landmarks, headings, names/roles/values, errors, live regions, dialogs, and reading order.
- Reduced motion and zoom/reflow are regression risks in modern frontends.
- Remediation patches require explicit user intent; otherwise produce findings and retest criteria.

## References
- WCAG target/version selected by the user or declared default.
- axe-core and Playwright/Jest accessibility tooling available in the target project.
- Assistive-technology notes captured from the actual test environment.
