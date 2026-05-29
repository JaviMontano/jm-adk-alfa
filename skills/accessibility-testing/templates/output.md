# Accessibility Testing Output

## Scope and Environment

| Field | Value |
| --- | --- |
| Target | {target} |
| Routes / components / flows | {scope} |
| Dynamic states opened | {states} |
| WCAG target | {wcag_target} |
| Browser / viewport | {browser_viewport} |
| Assistive technology | {assistive_technology} |
| Tooling and versions | {tooling_versions} |
| Date | {date} |

## Final Status

Status: `{pass_fail_conditional_or_not_verified}`

Rationale: {status_rationale}

## Automated Results

| Command / tool | Target state | Result | Evidence |
| --- | --- | --- | --- |
| {command} | {route_or_component_state} | {pass_fail_conditional_or_not_verified} | {artifact_or_observation} |

## Automated Findings

| Severity | Rule ID | Impact | Selector | WCAG tag | Evidence | Retest |
| --- | --- | --- | --- | --- | --- | --- |
| {severity} | {rule_id} | {impact} | `{selector}` | {wcag_tag} | {artifact} | {retest_status} |

## Keyboard Test Matrix

| Flow | Step | Keys | Expected | Observed | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| {flow} | {step} | {keys} | {expected} | {observed} | {status} | {evidence} |

## Screen Reader Smoke Matrix

| Pairing | Flow | Expected announcement | Observed announcement | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| {os_browser_at} | {flow} | {expected} | {observed} | {status} | {evidence} |

## Contrast and Motion

| Check | Selector / token | State | Expected | Observed | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| {contrast_or_motion_check} | `{selector_or_token}` | {state} | {expected} | {observed} | {status} | {evidence} |

## Findings and Retest Backlog

| ID | Severity | Finding | User impact | Recommended fix | Owner | Retest criterion |
| --- | --- | --- | --- | --- | --- | --- |
| {id} | {severity} | {finding} | {user_impact} | {fix} | {owner} | {criterion} |

## Suppressions and Exclusions

| Rule ID | Selector | Reason | Issue ID | Owner | Expiry | Re-enable criteria |
| --- | --- | --- | --- | --- | --- | --- |
| {rule_id} | `{selector}` | {reason} | {issue_id} | {owner} | {expiry} | {reenable} |

## Risks and Limits

{risks_and_not_verified_areas}

Do not convert a clean automated scan into a blanket WCAG conformance claim unless the report includes the full target, scope, tested technologies, date, and manual evidence.
