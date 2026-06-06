# AI Architecture Audit Knowledge Graph

## Nodes
- ai-architecture-audit: existing-system audit skill.
- evidence-log: source-backed observations.
- dimension-scorecard: D1-D6 assessment.
- finding: evidence-backed gap or risk.
- severity: CRITICAL/HIGH/MEDIUM/LOW/INFO.
- anti-pattern: detected AI architecture failure mode.
- remediation: pattern, effort, dependencies, Definition of Done.
- roadmap: prioritized remediation sequence.

## Edges
- evidence-log -> finding -> severity
- finding -> dimension-scorecard
- anti-pattern -> finding -> remediation
- technical-debt -> roadmap
- validation-report -> Guardian decision
