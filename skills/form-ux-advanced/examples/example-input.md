<!--
generated-by: scripts/scaffold-skill.py
generated-for: form-ux-advanced
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Audit the UX of a two-step enterprise intake form:

- Step 1 asks for work email.
- Step 2 asks for company size and an optional security brief.
- The form should show progress, allow back navigation, preserve the draft, show a top error summary, and retry failed submissions.
- Work email validates on blur; the upload validates with debounced feedback.
- Company size should default from CRM context when available.

Run the deterministic journey audit if the requirements can be represented as JSON.
