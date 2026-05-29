<!--
generated-by: scripts/scaffold-skill.py
generated-for: accessibility-audit
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Accessibility Audit

WCAG 2.1 AA digital accessibility audit with automated axe-core evidence,
manual keyboard and screen reader checks, contrast review, remediation tickets,
and explicit pass/conditional/fail/not-verified status.

## Triggers

- accessibility-audit
- WCAG audit
- axe-core
- keyboard accessibility
- screen reader
- contrast audit

## Allowed Tools

- Read
- Write
- Edit
- Grep
- Glob
- Bash

## Quick Use

Use this skill when the user needs to audit a web app, route, component, HTML
artifact, or design implementation for WCAG 2.1 AA accessibility. The skill
produces an audit report by default. Code remediation requires an explicit user
request.

## Output Format

Markdown audit report with scope, environment, automated axe findings, manual
keyboard/screen reader/contrast matrix, WCAG references, remediation tickets,
final status, validation evidence, and unresolved risks.
