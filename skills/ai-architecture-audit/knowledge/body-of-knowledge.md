# AI Architecture Audit Body of Knowledge

The audit evaluates an existing AI system. It does not design a new system and does not implement remediation.

## Six Dimensions

| id | dimension | expected evidence |
|----|-----------|-------------------|
| D1 | Structural Integrity | diagrams, dependency graph, module boundaries |
| D2 | AI Quality Attributes | thresholds, metrics, tests, monitoring |
| D3 | Pattern & Anti-Pattern Detection | code/config review, pipeline inspection |
| D4 | Security & Compliance | controls matrix, access policy, logs, PII handling |
| D5 | Technical Debt Inventory | debt item, impact, interest, principal |
| D6 | Remediation Roadmap | priority score, dependencies, Definition of Done |

## Evidence Rule

Each finding needs at least one concrete source: `[CÓDIGO]`, `[CONFIG]`, `[MÉTRICA]`, `[DOC]`, `[ENTREVISTA]`, or `[HERRAMIENTA]`. `[INFERENCIA]` can explain reasoning but cannot be the only evidence for a finding.

## Severity Rule

Severity is fixed: CRITICAL, HIGH, MEDIUM, LOW, INFO. Unknown or custom severity labels must be rejected.

## Report Rule

When evidence is missing, the report records a limitation or evidence gap instead of inventing a result.
