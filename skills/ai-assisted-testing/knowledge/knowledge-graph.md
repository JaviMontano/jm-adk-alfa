# AI Assisted Testing Knowledge Graph

## Nodes
- test-plan: evidence-backed testing deliverable.
- evidence: code, requirements, defects, examples, coverage.
- candidate-test: target, rationale, oracle, status.
- fuzzing-plan: domain, seeds, iterations, timeout, safety boundary.
- mutation-plan: baseline, operators, kill criteria.
- coverage-plan: current/target coverage and target files.
- validation: offline plan validator.

## Edges
- evidence -> candidate-test -> test-plan
- candidate-test -> coverage-plan
- fuzzing-plan -> candidate-test
- mutation-plan -> coverage-plan
- test-plan -> validation
