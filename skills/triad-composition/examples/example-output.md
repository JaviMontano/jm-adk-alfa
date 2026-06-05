# Triad Composition Packet

[EXPLICIT] The request is a requirements task for payroll onboarding with confidence `0.91`, so it meets the `>=0.85` auto-select band.

# Input Classification

- [EXPLICIT] Domain: Requirements.
- [EXPLICIT] Confidence band: `>=0.85`.
- [EXPLICIT] Action: auto-select and execute sequential triad.
- [EXPLICIT] Matrix source: `assets/composition-matrix.json`.

# Selected Triad

| Role | Agent | Evidence |
|---|---|---|
| Lead | `requirements-analyst` | [EXPLICIT] Requirements domain owns user stories and acceptance criteria. |
| Support | `domain-modeler` | [EXPLICIT] Support reviews domain terms, entities, and boundaries. |
| Guardian | `quality-guardian` | [EXPLICIT] Guardian validates evidence, Constitution compliance, and quality gates. |

# Execution Mode

- [EXPLICIT] Mode: triad.
- [EXPLICIT] Sequence: Lead -> Support -> Guardian.
- [EXPLICIT] Do not skip Guardian.

# Validation Gates

- [EXPLICIT] G0 pre-flight: Goal, Context, Constraints, Definition of done, and confidence are present.
- [EXPLICIT] G1 post-spec: domain maps to a single matrix row.
- [EXPLICIT] G2 post-plan: roles and sequence are explicit.
- [EXPLICIT] G3 delivery: Guardian validation required before final output.

# Risks and Assumptions

- [OPEN] Confirm payroll compliance jurisdictions before story finalization.
- [INFERRED] If compliance expands across legal, analytics, and security, escalate to committee.
