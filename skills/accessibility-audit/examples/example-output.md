<!--
generated-by: scripts/scaffold-skill.py
generated-for: accessibility-audit
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Final status: `fail`. [EXPLICIT]
The automated scan found no violations on `/checkout`, but manual keyboard verification found a focus-management blocker in the coupon modal. [EXPLICIT]
The flow cannot be called WCAG 2.1 AA compliant until the focus return behavior is fixed and retested. [EXPLICIT]

## Scope and Environment

| Field | Value |
|---|---|
| Target | `http://localhost:4173` |
| Routes | `/cart`, `/checkout`, `/checkout/confirmation` |
| Browser / viewport | Chromium desktop, 1440x900 |
| Assistive technology | VoiceOver smoke test |
| Tooling | Playwright + axe-core |

## Automated Findings

| Target | Tool | Rule | Impact | Selector | WCAG Tags | Evidence |
|---|---|---|---|---|---|---|
| `/checkout` | axe-core | none | none | none | none | automated report recorded |

## Manual Checklist

| Area | Status | Evidence | Notes |
|---|---|---|---|
| Keyboard navigation | fail | Tab sequence enters coupon modal but focus does not return to trigger on close. | Blocks predictable keyboard workflow. |
| Focus management | fail | Close modal with Escape; focus moves to document body. | Return focus to `Apply coupon`. |
| Screen reader names/roles/values | pass | VoiceOver announces coupon dialog title and close button. | Smoke test only. |
| Contrast | pass | Body text and buttons meet required ratios in sampled states. | Full token audit not performed. |
| Forms and errors | not verified | No invalid form submission tested. | Needs follow-up. |

## Remediation Tickets

| Severity | Target | WCAG / Principle | User Impact | Reproduction | Expected Behavior | Acceptance Check |
|---|---|---|---|---|---|---|
| P1 blocker | `/checkout` coupon modal | Focus management / keyboard operability | Keyboard users lose context after closing modal. | Open coupon modal, press Escape. | Focus returns to `Apply coupon`. | Playwright focus assertion plus manual keyboard retest passes. |

## Validation

- Skill activated intentionally for digital WCAG accessibility audit.
- Output separates automated evidence from manual verification.
- Final status does not overclaim compliance.
