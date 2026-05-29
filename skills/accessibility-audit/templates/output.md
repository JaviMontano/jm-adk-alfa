<!--
generated-by: scripts/scaffold-skill.py
generated-for: accessibility-audit
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Accessibility Audit Output

## Summary

{audit_verdict_summary}

## Scope and Environment

| Field | Value |
|---|---|
| Target | {target} |
| Routes / components audited | {scope_items} |
| Out of scope | {out_of_scope} |
| Browser / viewport | {browser_viewport} |
| Assistive technology | {assistive_technology} |
| Tooling and versions | {tooling_versions} |
| Report artifacts | {report_artifacts} |

## Final Status

| Status | Reason |
|---|---|
| {pass_conditional_fail_or_not_verified} | {status_reason} |

## Automated Findings

| Target | Tool | Rule | Impact | Selector | WCAG Tags | Evidence |
|---|---|---|---|---|---|---|
| {target} | {tool} | {rule} | {impact} | {selector} | {wcag_tags} | {artifact_or_note} |

## Manual Checklist

| Area | Status | Evidence | Notes |
|---|---|---|---|
| Keyboard navigation | {pass_fail_not_verified} | {evidence} | {notes} |
| Focus management | {pass_fail_not_verified} | {evidence} | {notes} |
| Screen reader names/roles/values | {pass_fail_not_verified} | {evidence} | {notes} |
| Landmarks and headings | {pass_fail_not_verified} | {evidence} | {notes} |
| Forms, labels, and errors | {pass_fail_not_verified} | {evidence} | {notes} |
| Contrast and non-text contrast | {pass_fail_not_verified} | {evidence} | {notes} |
| Dynamic content and live regions | {pass_fail_not_verified} | {evidence} | {notes} |
| Motion and responsive behavior | {pass_fail_not_verified} | {evidence} | {notes} |

## Remediation Tickets

| Severity | Target | WCAG / Principle | User Impact | Reproduction | Expected Behavior | Acceptance Check |
|---|---|---|---|---|---|---|
| {severity} | {target} | {wcag_or_principle} | {impact} | {steps} | {expected} | {acceptance_check} |

## Exceptions and Not-Verified Areas

{exceptions_and_not_verified}

## Risks and Limits

{risks_and_limits}

## Validation Evidence

{validation_evidence}
