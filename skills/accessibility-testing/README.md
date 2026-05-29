# Accessibility Testing

Evidence-first workflow for planning, running, and reporting accessibility tests on web apps, components, and critical user flows.

## Triggers

- "run accessibility tests"
- "test this with axe"
- "a11y regression"
- "keyboard accessibility test"
- "screen reader smoke test"
- "WCAG test evidence"

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when the user needs executable accessibility QA: automated checks, manual test scripts, scoped findings, retest evidence, or a regression-ready report. It is not the right skill for visual redesign (`accessibility-design`) or broad policy/compliance review (`accessibility-audit`).

Minimum useful input:

- target app, route, component, flow, fixture, or repository path;
- desired WCAG target, or permission to default to WCAG 2.2 AA as a testing target;
- available tooling and environment constraints;
- whether the user wants only a report or also remediation patches.

## Output Format

Markdown report with:

- scope and environment;
- final status: `pass`, `fail`, `conditional`, or `not verified`;
- automated results and exact commands;
- keyboard test matrix;
- screen reader smoke matrix;
- contrast and reduced-motion evidence;
- findings, owners, suppressions, and retest status;
- limits, not-verified areas, and next validation step.

Do not write "WCAG compliant" unless the target, scope, technologies, date, and evidence support that claim.
