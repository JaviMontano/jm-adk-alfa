<!--
generated-by: scripts/scaffold-skill.py
generated-for: accessibility-design
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Design the coupon modal as a native-dialog-like interaction with explicit focus
containment, return focus, visible labels, programmatic error association, and
measured contrast before release. [EXPLICIT]

## Semantic HTML and ARIA Decisions

| Element / Pattern | Native First Decision | ARIA Needed? | Name / Role / State |
|---|---|---|---|
| Trigger | Native `button` | No | Visible text `Apply coupon` is the accessible name |
| Modal container | Dialog pattern | Yes, if not using native `dialog` | `role="dialog"`, `aria-modal="true"`, labelled by modal title |
| Coupon input | Native `input` with visible `label` | `aria-describedby` for help/error text | Error state announced through associated message |
| Close icon | Native `button` | Accessible name required | `aria-label="Close coupon dialog"` if no visible text |

## Keyboard Interaction Map

| Interaction | Expected Behavior |
|---|---|
| Tab / Shift+Tab | Moves through input, Cancel, Apply, Close, and wraps inside the modal while open |
| Enter | Submits coupon when focus is in the input or on Apply |
| Space | Activates focused buttons |
| Escape | Closes modal without applying coupon |
| Close | Returns focus to `Apply coupon` trigger |

## Focus Management

| Moment | Focus Target | Rule |
|---|---|---|
| Open modal | Coupon code input or modal title | Choose input if immediate entry is the dominant task |
| Invalid coupon | First invalid field | Keep focus on input and announce error text |
| Close modal | `Apply coupon` trigger | Always return focus to invoking control |

## Content, Forms, and Feedback

- The input has a visible label, not placeholder-only text. [EXPLICIT]
- Invalid coupon errors are associated with the input and written in recovery-oriented language. [EXPLICIT]
- Successful coupon application uses a polite status message without stealing focus. [EXPLICIT]
- Error/success state is not communicated by color alone. [EXPLICIT]

## Visual and Motion Requirements

| Area | Requirement | Evidence |
|---|---|---|
| Text contrast | Error, helper, and button text meet 4.5:1 | Not verified until token ratios are measured |
| Non-text contrast | Focus ring and input border meet 3:1 | Not verified until token ratios are measured |
| Motion | Modal transition respects reduced motion | Required before implementation acceptance |

## Validation

- Native HTML is preferred before ARIA.
- Keyboard, focus, screen reader, forms/errors, and contrast requirements are testable.
- Contrast evidence is honestly marked not verified instead of overclaimed.
