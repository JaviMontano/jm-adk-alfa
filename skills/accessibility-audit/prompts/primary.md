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

1. Read `SKILL.md` `## Purpose`, `## Protocol`, `## Routing Boundary`, `## Quality Gates`, and `## Anti-Patterns`. Read `knowledge/body-of-knowledge.md` for the Status Model and Severity model.
2. **Confirm scope is digital WCAG.** If the request is physical-space, financial-access, or API "accessibility", stop and ask for clarification (see Routing Boundary) — do not audit.
3. **Lock the evidence base.** Record target (`{{task}}`), route/component scope, auth/session state, browser, viewport set, assistive technology, and date. If there is no runnable target or supplied artifact, emit a gap report with the missing inputs and stop at status `not verified`.
4. **Run automation.** Detect the project runner (`@axe-core/playwright` → `axe-playwright` → `cypress-axe` → `jest-axe` → `@storybook/addon-a11y` → standalone `axe-core`). Scan each in-scope route/component, save artifacts, and record tool, target, rule id, impact, selector, and WCAG tags per violation. Treat "0 violations" as "no automated violations found", not conformance.
5. **Run the manual checklist** — keyboard, focus management, screen reader (page title / headings / landmarks / name-role-value / error and status announcements), contrast (4.5:1 text, 3:1 large/non-text), forms and errors, dynamic content / live regions, motion (`prefers-reduced-motion`, pause-stop-hide), and reflow/zoom (400% reflow, 200% text). Each area gets `pass` / `fail` / `not verified` with an observation.
6. **Re-rank severity** by user-task blocking, WCAG level, and recurrence — not by raw axe impact. Map every finding to a WCAG 2.1 AA criterion or documented principle and write an owner-ready ticket (target, selector, reproduction, user impact, expected behavior, evidence, acceptance check).
7. **Produce the report** from `templates/output.md`.
8. **Validate the verdict.** Final status is exactly one of `pass` / `conditional` / `fail` / `not verified`. No "compliant" / "accessible" claim may appear while any area is `not verified` or evidence is missing; a manual blocker outranks a clean axe scan.
