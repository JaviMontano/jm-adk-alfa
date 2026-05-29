<!--
generated-by: scripts/scaffold-skill.py
generated-for: accessibility-design
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Accessibility Design Output

## Summary

{accessible_design_summary}

## Scope

| Field | Value |
|---|---|
| Feature / component | {feature_or_component} |
| User journey | {user_journey} |
| In-scope states | {states} |
| Out of scope | {out_of_scope} |
| Related audit/testing handoff | {audit_or_testing_handoff} |

## WCAG / POUR Mapping

| Area | Requirement | Acceptance Criteria |
|---|---|---|
| Perceivable | {perceivable_requirement} | {perceivable_acceptance} |
| Operable | {operable_requirement} | {operable_acceptance} |
| Understandable | {understandable_requirement} | {understandable_acceptance} |
| Robust | {robust_requirement} | {robust_acceptance} |

## Semantic HTML and ARIA Decisions

| Element / Pattern | Native First Decision | ARIA Needed? | Name / Role / State |
|---|---|---|---|
| {component_part} | {native_decision} | {aria_decision} | {name_role_state} |

## Keyboard Interaction Map

| Interaction | Expected Behavior |
|---|---|
| Tab / Shift+Tab | {tab_behavior} |
| Enter / Space | {activation_behavior} |
| Escape | {escape_behavior} |
| Arrow keys | {arrow_behavior} |
| Route or state change | {route_state_focus_behavior} |

## Focus Management

| Moment | Focus Target | Rule |
|---|---|---|
| Initial render | {initial_focus} | {initial_focus_rule} |
| Open overlay / disclosure | {open_focus} | {open_focus_rule} |
| Close overlay / disclosure | {return_focus} | {return_focus_rule} |
| Validation error | {error_focus} | {error_focus_rule} |

## Content, Forms, and Feedback

| Area | Requirement |
|---|---|
| Labels and descriptions | {labels_descriptions} |
| Errors and recovery | {errors_recovery} |
| Status / live updates | {status_updates} |
| Alt text and decorative media | {alt_text} |
| Plain language and sensory cues | {content_cues} |

## Visual and Motion Requirements

| Area | Requirement | Evidence |
|---|---|---|
| Text contrast | {text_contrast} | {text_contrast_evidence} |
| Non-text contrast | {non_text_contrast} | {non_text_contrast_evidence} |
| Focus indicator | {focus_indicator} | {focus_evidence} |
| Reduced motion | {reduced_motion} | {motion_evidence} |
| Zoom / reflow / forced colors | {responsive_accessibility} | {responsive_evidence} |

## Implementation Notes

{implementation_notes}

## Validation Matrix

| Check | Expected Result | Status |
|---|---|---|
| Automated a11y scan | {automated_expected} | {automated_status} |
| Keyboard smoke test | {keyboard_expected} | {keyboard_status} |
| Screen reader smoke test | {screen_reader_expected} | {screen_reader_status} |
| Contrast/token check | {contrast_expected} | {contrast_status} |

## Risks and Not-Verified Areas

{risks_not_verified}
