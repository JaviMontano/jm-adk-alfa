---
name: accessibility-audit-primary
type: execution
version: 2.0.0
description: "Execute the Accessibility Audit workflow."
triad:
  lead: "accessibility-audit-lead"
  support: "accessibility-audit-support"
  guardian: "accessibility-audit-guardian"
---

# Accessibility Audit — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |

## Execution Steps
1. Read `SKILL.md` `## Purpose`, `## Protocol`, `## I/O`, and `## Quality Gates`.
2. Confirm the request is for digital WCAG/accessibility audit scope.
3. Establish target, route/component scope, environment, available tools, and evidence gaps.
4. Run or request automated scan evidence; record tool, target, rule, impact, selector, WCAG tags, and artifact path.
5. Perform or request manual evidence for keyboard, focus, screen reader, contrast, forms/errors, dynamic content, motion, and responsive behavior.
6. Produce the audit report using `templates/output.md`.
7. Validate that final status is `pass`, `conditional`, `fail`, or `not verified`, and that no compliance claim appears without evidence.
