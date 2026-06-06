# AI Architecture Audit

Audit an existing AI-enabled system across six deterministic dimensions: structural integrity, AI quality attributes, pattern adherence, anti-pattern detection, security/compliance, and technical debt. The skill produces evidence-backed findings and a remediation roadmap without implementing fixes.

Use this skill when the user asks for AI architecture review, ML system quality assessment, AI technical debt inventory, AI security posture review, GenAI architecture audit, drift monitoring audit, or compliance readiness for an AI system.

## Deterministic Contract

- Every finding must cite concrete evidence: code, configuration, metrics, documentation, interview notes, or tool output.
- Unknown evidence is reported as a gap; it must not be invented.
- Severity must use the fixed taxonomy in `assets/severity-policy.json`.
- All six audit dimensions must be covered, or an omission must include a rationale.
- Remediation must include pattern, effort, dependencies, and Definition of Done.
- Machine-readable audit packets must validate with `scripts/check.sh`.

## Output

The expected report contains:

- System identity, audit scope, mode, depth, and format.
- Six-dimension scorecard.
- Evidence-backed findings with severity and remediation.
- Quality attribute threshold gaps.
- Pattern and anti-pattern matrix.
- Security and compliance control matrix.
- Technical debt inventory.
- Prioritized remediation roadmap.
- Validation evidence and residual risks.
