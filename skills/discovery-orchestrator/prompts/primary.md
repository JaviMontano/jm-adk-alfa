---
name: discovery-orchestrator-primary
type: execution
version: 2.0.0
triad:
  lead: "discovery-orchestrator-lead"
  support: "discovery-orchestrator-support"
  guardian: "discovery-orchestrator-guardian"
---
# Discovery Orchestrator — Execute

1. Determine operating mode: `sequence`, `gate-check`, `dashboard`, or `handoff-readiness`.
2. Load `assets/report-contract.json`, `assets/phase-contract.json`, `assets/skill-sequence-contract.json`, and `assets/gate-policy.json` when packet validation is required.
3. Build an evidence-tagged phase plan and canonical skill sequence.
4. Evaluate G1, feasibility checkpoint, G2, and G3 as `pass`, `block`, or `pending`.
5. Enforce the non-analysis boundary: no domain findings, no implementation steps, and no prices.
6. Emit validation evidence and the next skill or blocker.
