# Example Input

Run accessibility testing on the checkout flow before release.

Context:

- App route: `/checkout`
- States to cover: cart summary, shipping form, validation errors, payment modal, success toast
- Browser: Chromium desktop and mobile viewport
- Target: WCAG 2.2 AA
- Existing tools: Playwright is installed; no screen reader notes exist yet
- Need: a QA report and retest backlog, not remediation patches

Include automated axe checks after each interaction, keyboard-only test steps, contrast checks for form labels and error text, reduced-motion coverage for the toast, and screen reader smoke scripts for VoiceOver/Safari and NVDA/Firefox.
