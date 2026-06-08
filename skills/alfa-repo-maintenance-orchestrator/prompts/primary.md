# Primary Prompt

Use `alfa-repo-maintenance-orchestrator` to plan or execute JM-ADK Alfa maintenance.

## Prompt

Create an orchestration report with the eight required phases in order. Prove the baseline, require repo-sync audit evidence, require a local-state-preservation manifest before any mutation, require an isolated non-main branch for writes, require cleanup manifests for transient/archive actions, run validation gates, and close with `proceed`, `pause`, or `blocked`.
