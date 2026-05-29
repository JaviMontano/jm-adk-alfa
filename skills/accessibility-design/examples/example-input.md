<!--
generated-by: scripts/scaffold-skill.py
generated-for: accessibility-design
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Design the accessibility behavior for a checkout coupon modal.

Context:

- Trigger: `Apply coupon` button in checkout summary.
- Modal content: title, coupon code input, inline validation error, `Cancel`, `Apply`, and close icon button.
- State changes: valid coupon applies discount and closes modal; invalid coupon shows inline error and summary message.
- Constraints: use native HTML first; use ARIA only when required; design tokens exist but contrast ratios are not yet measured.

Output needed:

Return an accessible interaction spec with semantic decisions, keyboard map,
focus management, screen reader expectations, form/error behavior, contrast
requirements, implementation notes, acceptance criteria, and validation matrix.
