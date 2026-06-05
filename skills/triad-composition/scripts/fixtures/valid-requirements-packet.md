# Triad Composition Packet

[EXPLICIT] Classify a payroll onboarding story request and compose the Pristino triad.

# Input Classification

- [EXPLICIT] Domain: Requirements
- [EXPLICIT] Confidence band: >=0.85
- [EXPLICIT] Action: auto_select_skill_compose_triad_execute

# Selected Triad

| Role | Agent | Reason |
|---|---|---|
| Lead | requirements-analyst | [EXPLICIT] Owns requirements, user stories, and acceptance criteria |
| Support | domain-modeler | [EXPLICIT] Reviews domain terms and entity boundaries |
| Guardian | quality-guardian | [EXPLICIT] Validates evidence, Constitution compliance, and quality gates |

# Execution Mode

- [EXPLICIT] Mode: triad
- [EXPLICIT] Execute sequentially: Lead -> Support -> Guardian

# Validation Gates

- [EXPLICIT] G0 pre-flight: input has Goal, Context, Constraints, Definition of done.
- [EXPLICIT] G1 post-spec: domain and triad mapped to matrix.
- [EXPLICIT] G2 post-plan: sequential handoff confirmed.
- [EXPLICIT] G3 deploy-ready: guardian validation required before delivery.

# Risks and Assumptions

- [OPEN] Confirm payroll compliance constraints before final requirements.
