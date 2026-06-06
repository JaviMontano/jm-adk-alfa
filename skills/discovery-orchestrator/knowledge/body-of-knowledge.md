# Discovery Orchestrator — Body of Knowledge

## Canon

Discovery orchestration is the governance layer for phases 0-6. It coordinates downstream skills, records gate state, and blocks unsupported transitions. It does not author the analysis artifacts that those downstream skills own.

## Canonical Controls

| Control | Deterministic Rule |
|---------|--------------------|
| Phase order | Use `assets/phase-contract.json`; never start phase 4 before G1 and feasibility readiness. |
| Skill sequence | Use only skills listed in `assets/skill-sequence-contract.json`. |
| Gate state | Represent each gate as `pass`, `block`, or `pending`; never infer approval. |
| Evidence | Tag every claim with `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`, or `[ASSUMPTION]`. |
| Assumptions | Add a warning banner when assumptions exceed 30 percent. |
| Boundary | Reject domain findings, implementation plans, and currency or price fields. |

## Quality Metrics

| Metric | Target |
|--------|--------|
| Evidence coverage | 100 percent of claims |
| G1 scenario coverage | At least 3 scored scenarios |
| Gate decision determinism | Explicit criteria and approval state |
| Skill sequence validity | 100 percent canonical skills |
| Price leakage | 0 currency, rate, or price fields |
| Offline validation | `scripts/check.sh` passes |
