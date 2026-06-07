# AI Software Architecture - Body of Knowledge

## Canon

This skill combines software architecture practice with AI-specific production concerns: feature computation, model training, model registry, inference topology, monitoring, governance, and model drift. The canonical reference model is the 6-layer AI stack in `references/ai-architecture-stack.md`.

## Deterministic Quality Metrics

| Metric | Target | How To Measure |
|--------|--------|----------------|
| Layer coverage | 6 layers or justified exclusions | Each report has hardware, data, model, inference, application, monitoring_control entries |
| Evidence coverage | 100% for decisions | Each pattern, ADR, and debt item links to evidence or an assumption |
| Quality scenario completeness | 100% | Each scenario includes attribute, stimulus, response, measure, and evidence |
| ADR completeness | 100% | Each ADR includes status, context, decision, consequences, alternatives, and evidence |
| Debt actionability | 100% | Each debt item includes severity, owner, mitigation, sequence, and evidence |
| Offline validation | pass | JSON handoff passes `scripts/validate_ai_architecture_report.py` |

## Architecture Concepts

- The model is a component, not the full system.
- Drift is first-class architecture debt.
- Feature definitions are contracts between training and serving.
- Explainability, fairness, robustness, and auditability are quality attributes, not optional add-ons.
- Patterns must trace to a quality attribute or risk.

## References

- `references/ai-architecture-stack.md`
- `references/ai-quality-attributes.md`
- `references/ai-patterns-catalog.md`
