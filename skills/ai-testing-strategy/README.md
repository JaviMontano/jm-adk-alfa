# AI Testing Strategy

Deterministic JM Labs skill for designing test strategies for AI-enabled systems. It covers the 6 test types x 6 layers matrix, model and prediction tests, data quality tests, fairness and compliance tests, integration harnesses, CI/CD gates, and continuous monitoring.

## Trigger

Use this skill when the request asks to define an AI testing strategy, validate model predictions, design data quality tests, plan fairness testing, test AI pipelines, build AI integration tests, automate model quality gates, or evaluate coverage gaps in AI system testing.

## Deterministic Inputs

- System or project name.
- AI use case, model type, and risk level.
- Layers present: UI, API, pipeline ops, model processing, data management, infrastructure.
- Required metrics for accuracy, performance, fairness, explainability, drift, compliance, and security.
- CI/CD context, test tools, monitoring tools, and test data constraints.

## Output Contract

The strategy must include system context, evidence, matrix coverage, model tests, data quality tests, fairness and compliance tests, integration strategy, automation gates, monitoring plan, residual risks, and validation checks. JSON handoffs are validated offline with `scripts/validate_ai_testing_strategy.py`.

## Local Validation

```bash
bash skills/ai-testing-strategy/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill ai-testing-strategy
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-testing-strategy
```
