# Triad Composition Packet

[EXPLICIT] Classify a mixed React and Firebase login request without silently choosing one domain.

# Input Classification

- [EXPLICIT] Domains: Frontend, Backend/Firebase, Testing
- [EXPLICIT] Confidence band: 0.60-0.84
- [EXPLICIT] Action: needs_disambiguation
- [EXPLICIT] Present top 3 options.

# Selected Triad

| Rank | Domain | Lead | Support | Guardian |
|---|---|---|---|---|
| 1 | Frontend | frontend-craftsman | accessibility-designer | quality-engineer |
| 2 | Backend/Firebase | firebase-specialist | security-architect | quality-engineer |
| 3 | Testing | quality-engineer | e2e-test-writer | code-reviewer |

# Execution Mode

- [OPEN] Do not execute until the user chooses the intended domain or confirms a committee.

# Validation Gates

- [EXPLICIT] G0 pre-flight: ambiguity detected.
- [EXPLICIT] G1 post-spec: top 3 matrix options shown.
- [EXPLICIT] G2 post-plan: execution paused.
- [EXPLICIT] G3 deploy-ready: blocked pending user choice.

# Risks and Assumptions

- [OPEN] Choosing Frontend first may under-review Firebase Auth rules.
