# Admin Dashboards Output

## Scope and Assumptions

| Field | Value |
| --- | --- |
| Objective | {objective} |
| Users / roles | {roles} |
| Entities | {entities} |
| Data sources | {data_sources} |
| Existing APIs / schemas | {api_schema_evidence} |
| Not verified | {not_verified_items} |

## Entity and Data Contract

| Entity | Source | Query / endpoint | Params | Response | Error shape | Owner | Freshness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {entity} | {source} | `{query_or_endpoint}` | {params} | {response_shape} | {error_shape} | {owner} | {freshness} |

## Authorization Matrix

| Role | Route | Resource | Action | UI behavior | Backend enforcement | Negative test |
| --- | --- | --- | --- | --- | --- | --- |
| {role} | `{route}` | {resource} | {action} | {visible_disabled_hidden} | {policy_or_not_verified} | {test} |

## Navigation and Layout

- Primary navigation: {primary_nav}
- Secondary navigation / breadcrumbs: {secondary_nav}
- Responsive behavior: {responsive_behavior}
- Density and scanability rules: {density_rules}

## Table Behavior Contract

| Table | Columns | Sort | Filters | Search | Pagination | Selection / bulk | URL state |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {table} | {columns} | {sort} | {filters} | {search} | {pagination} | {bulk_actions} | {url_state} |

## CRUD and Bulk Workflows

| Workflow | Validation | Loading / disabled states | Success | Error / conflict | Audit | Recovery |
| --- | --- | --- | --- | --- | --- | --- |
| {workflow} | {form_rules} | {loading} | {success} | {error_conflict} | {audit} | {recovery} |

## Metrics and Charts

| KPI / chart | Formula | Source | Unit | Time range / timezone | Refresh | Empty/error state |
| --- | --- | --- | --- | --- | --- | --- |
| {metric} | {formula_or_not_verified} | {source} | {unit} | {range_timezone} | {refresh} | {state} |

## Realtime and Refresh Strategy

| Feature | Channel | Event shape | Fallback | Stale state | Evidence |
| --- | --- | --- | --- | --- | --- |
| {feature} | {channel_or_not_verified} | {event_shape} | {fallback} | {stale_state} | {artifact_or_not_verified} |

## States and Recovery

| Area | Empty | Loading | Partial error | Permission denied | Timeout/offline | Retry |
| --- | --- | --- | --- | --- | --- | --- |
| {area} | {empty} | {loading} | {partial_error} | {permission_denied} | {timeout_offline} | {retry} |

## Security, Audit, and Export

| Risk | Guardrail | Evidence | Test |
| --- | --- | --- | --- |
| {risk} | {guardrail} | {evidence_or_not_verified} | {test} |

## Accessibility, Responsive, and Performance

| Gate | Requirement | Evidence / test |
| --- | --- | --- |
| Keyboard | {keyboard_requirement} | {keyboard_test} |
| Screen reader semantics | {semantic_requirement} | {semantic_test} |
| Responsive density | {responsive_requirement} | {responsive_test} |
| Performance | {dataset_size_and_measurement_context} | {performance_test} |

## Test Plan

| Test | Purpose | Expected result |
| --- | --- | --- |
| {test_name} | {purpose} | {expected} |

## Risks and Not Verified

{risks_and_not_verified}
