<!--
generated-by: scripts/scaffold-skill.py
generated-for: accessibility-audit
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Run a WCAG 2.1 AA accessibility audit for a checkout flow.

Context:

- Target: local app at `http://localhost:4173`.
- Routes in scope: `/cart`, `/checkout`, `/checkout/confirmation`.
- Tooling available: Playwright and axe-core.
- Manual checks requested: keyboard-only navigation, VoiceOver smoke test, color contrast, form labels/errors, modal behavior, and toast announcements.
- Known concern: axe reports zero violations on `/checkout`, but QA noticed focus does not return to the "Apply coupon" button after the coupon modal closes.

Output needed:

Return an audit report with final status, automated findings, manual checklist,
WCAG/principle mapping, remediation tickets, and not-verified areas.
