# Example Output

## Scope and Environment

| Field | Value |
| --- | --- |
| Target | Checkout release accessibility test |
| Routes / components / flows | `/checkout`, shipping form, payment modal, success toast |
| Dynamic states opened | Form errors, modal open/close, toast visible |
| WCAG target | WCAG 2.2 AA testing target |
| Browser / viewport | Chromium desktop and mobile viewport |
| Assistive technology | VoiceOver/Safari and NVDA/Firefox scripts prepared; execution pending |
| Tooling and versions | Playwright + axe package versions from project lockfile |
| Date | 2026-05-28 |

## Final Status

Status: `conditional`

Rationale: automated and keyboard evidence can be collected in the project; screen reader execution remains `not verified` until tested on the declared AT/browser pairs.

## Automated Results

| Command / tool | Target state | Result | Evidence |
| --- | --- | --- | --- |
| `npx playwright test tests/a11y/checkout.spec.ts` | shipping form + error state + modal + toast | `conditional` | Add artifact path after run |

## Automated Findings

| Severity | Rule ID | Impact | Selector | WCAG tag | Evidence | Retest |
| --- | --- | --- | --- | --- | --- | --- |
| High | `label` | Payment method group lacks accessible name | `.payment-methods` | WCAG 4.1.2 | axe report artifact | Re-run modal state scan |

## Keyboard Test Matrix

| Flow | Step | Keys | Expected | Observed | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Payment modal | Close modal | `Escape` | Modal closes and focus returns to "Pay now" | Not run yet | `not verified` | Manual execution needed |
| Shipping form | Error summary | `Tab`, `Enter` | Error summary receives focus and links to invalid field | Not run yet | `not verified` | Manual execution needed |

## Screen Reader Smoke Matrix

| Pairing | Flow | Expected announcement | Observed announcement | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| VoiceOver/Safari | Payment modal opens | Dialog name, role, initial focus, and close control announced | Not run yet | `not verified` | VoiceOver smoke script |
| NVDA/Firefox | Shipping error | Error summary and invalid field relationship announced | Not run yet | `not verified` | NVDA smoke script |

## Contrast and Motion

| Check | Selector / token | State | Expected | Observed | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Contrast | `.error-text` | error | >= 4.5:1 for normal text | 4.7:1 | `pass` | Token contrast calculation |
| Reduced motion | `.success-toast` | visible | No non-essential animation under reduced motion | Not run yet | `not verified` | Playwright reduced-motion context |

## Findings and Retest Backlog

| ID | Severity | Finding | User impact | Recommended fix | Owner | Retest criterion |
| --- | --- | --- | --- | --- | --- | --- |
| A11Y-001 | High | Payment method group lacks accessible name | Screen reader users cannot identify the group purpose | Add native grouping or an accessible label | Frontend | axe modal state passes and SR smoke confirms group name |

## Risks and Limits

- This is not a WCAG conformance certification.
- Screen reader results are not verified until the declared AT/browser pairings are executed.
- Remediation patches were not requested, so this report stops at findings and retest criteria.
