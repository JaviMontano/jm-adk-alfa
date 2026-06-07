# AI Design Patterns

AI Design Patterns selects reusable AI architecture patterns and tactics from
explicit requirements, detected anti-patterns, constraints, and pattern
dependencies. It produces a machine-checkable selection report.

## Triggers
- ai-design-patterns
- select AI design patterns
- apply ML patterns
- design drift detection
- implement feature store
- plan shadow deployment
- design champion-challenger
- select availability tactics for AI

## Output
Markdown by default, plus optional JSON packet using
`assets/pattern-selection-contract.json`.

Required sections:
- system requirements and detected context
- anti-pattern detection
- pattern recommendations with evidence and trade-offs
- tactic mapping
- dependency checks
- implementation roadmap
- validation and risks

## Determinism Rules
- Patterns must come from `assets/pattern-catalog-policy.json`.
- Every recommended pattern requires rationale, trade-offs, tactics, and evidence.
- Anti-pattern findings require detection signal and remediation pattern.
- Dependencies such as Champion-Challenger needing Feature Store or Model Registry must be explicit.
- Roadmap phases require exit criteria.

## Local Validation
```bash
bash skills/ai-design-patterns/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill ai-design-patterns
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-design-patterns
```
