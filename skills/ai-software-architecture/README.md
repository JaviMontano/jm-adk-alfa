# AI Software Architecture

Deterministic JM Labs skill for designing and reviewing the internal architecture of AI-enabled software systems. It covers module boundaries, the 6-layer AI stack, component contracts, AI architecture patterns, measurable quality attribute scenarios, ADRs, and debt evolution.

## Trigger

Use this skill when the request asks for AI software structure, AI module boundaries, AI architecture decisions, AI quality attributes, AI design patterns, model-serving architecture, feature-store boundaries, drift-resilient design, or technical debt in AI-enabled systems.

## Deterministic Inputs

- System or project name.
- AI use case and risk context.
- Existing codebase notes or declared greenfield constraints.
- Latency, availability, accuracy, fairness, explainability, robustness, drift, compliance, and deployability targets when known.
- Known modules, data sources, model-serving approach, monitoring constraints, and team ownership.

## Output Contract

The report must include system context, evidence, 6-layer module view, component contracts, selected patterns, detected anti-patterns, measurable quality attribute scenarios, ADRs, debt inventory, evolution plan, and validation checks. JSON handoffs are validated offline with `scripts/validate_ai_architecture_report.py`.

## Local Validation

Run:

```bash
bash skills/ai-software-architecture/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill ai-software-architecture
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-software-architecture
```
