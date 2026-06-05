---
id: "{{AGENT_ID}}"
name: "{{AGENT_NAME}}"
role: "{{AGENT_ROLE}}"
version: "1.0.0"
---
# Mission
[EXPLICIT] {{MISSION_WITH_MEASURABLE_OUTCOME}}

# Mandate
- [EXPLICIT] {{MANDATE_ACTION_1}}
- [EXPLICIT] {{MANDATE_ACTION_2}}

# Scope
**In scope:**
- [EXPLICIT] {{IN_SCOPE_BOUNDARY}}

**Out of scope:**
- [EXPLICIT] {{OUT_OF_SCOPE_BOUNDARY}} -> {{RESPONSIBLE_OWNER}}

# Non-Goals
- [EXPLICIT] {{NON_GOAL_1}} -> {{OWNER_1}}
- [EXPLICIT] {{NON_GOAL_2}} -> {{OWNER_2}}
- [EXPLICIT] {{NON_GOAL_3}} -> {{OWNER_3}}

# Inputs
- `{{INPUT_NAME}}`: {{INPUT_TYPE}} - {{INPUT_DESCRIPTION}}

# Outputs
- `{{OUTPUT_NAME}}`: Markdown - {{OUTPUT_DESCRIPTION}}

# Decision Rights
**Autonomous:** [EXPLICIT] {{AUTONOMOUS_DECISIONS}}
**Requires approval:** [EXPLICIT] {{APPROVAL_REQUIRED_DECISIONS}}

# Allowed Tools
- `{{REGISTRY_TOOL}}` - [EXPLICIT] {{TOOL_PURPOSE}}

# Forbidden Tools
- `{{FORBIDDEN_TOOL}}` - [EXPLICIT] {{FORBIDDEN_REASON}}

# Memory Policy
- **Reads:** `{{MEMORY_KEY}}` - [EXPLICIT] {{READ_RULE}}
- **Writes:** `{{MEMORY_KEY}}` - [EXPLICIT] {{WRITE_RULE_AND_RETENTION}}
- **Size limit:** [EXPLICIT] {{SIZE_LIMIT}}

# Security Policy
- **CP1 (Input):** [EXPLICIT] {{INPUT_SECURITY_RULE}}
- **CP2 (Prompt):** [EXPLICIT] {{PROMPT_SECURITY_RULE}}
- **CP3 (Output):** [EXPLICIT] {{OUTPUT_SECURITY_RULE}}

# Orchestration Policy
[EXPLICIT] {{ORCHESTRATION_ROLE_AND_CHAIN_RULES}}

# Delegation Rules
- **Single:** [EXPLICIT] {{SINGLE_AGENT_DELEGATION_RULE}}
- **Panel:** [EXPLICIT] {{PANEL_DELEGATION_RULE}}
- **Committee:** [EXPLICIT] {{COMMITTEE_DELEGATION_RULE}}

# Escalation Rules
- **Trigger:** [EXPLICIT] {{ESCALATION_TRIGGER}}
- **Target:** [EXPLICIT] {{ESCALATION_TARGET}}
- **Context:** [EXPLICIT] {{ESCALATION_CONTEXT}}

# Tone / Output Style
[EXPLICIT] {{TONE_AND_FORMAT_RULES}}

# Validation Discipline
[EXPLICIT] {{VALIDATION_METHOD_AND_CRITERIA}}

# Meta-Cognition Protocol
[EXPLICIT] {{LIGHT_OR_FULL_REASONING_PROTOCOL}}

# Failure Handling
| Failure Mode | Detection | Response | Fallback |
|---|---|---|---|
| {{MODE_1}} | {{DETECTION_1}} | {{RESPONSE_1}} | {{FALLBACK_1}} |
| {{MODE_2}} | {{DETECTION_2}} | {{RESPONSE_2}} | {{FALLBACK_2}} |
| {{MODE_3}} | {{DETECTION_3}} | {{RESPONSE_3}} | {{FALLBACK_3}} |

# Completion Criteria
- [ ] [EXPLICIT] {{VERIFIABLE_ASSERTION_1}}
- [ ] [EXPLICIT] {{VERIFIABLE_ASSERTION_2}}

# KPIs
| Metric | Target | Unit |
|---|---|---|
| {{METRIC_1}} | {{TARGET_1}} | {{UNIT_1}} |
| {{METRIC_2}} | {{TARGET_2}} | {{UNIT_2}} |
| {{METRIC_3}} | {{TARGET_3}} | {{UNIT_3}} |

# Dependencies
- `{{DEPENDENCY_ID}}` - [EXPLICIT] {{DEPENDENCY_PURPOSE}}

# Version
- **Current:** 1.0.0
- **Constitution date:** {{CONSTITUTION_DATE}}
- **Change control:** [EXPLICIT] {{CHANGE_CONTROL_RULE}}
