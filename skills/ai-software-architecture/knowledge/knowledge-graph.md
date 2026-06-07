# AI Software Architecture - Knowledge Graph

## Core Nodes

- `ai-software-architecture`: skill capability.
- `system-context`: project, use case, risk level, architecture scope.
- `evidence`: explicit, inferred, or open provenance.
- `six-layer-stack`: hardware, data, model, inference, application, monitoring_control.
- `component-contract`: input, output, responsibility, dependencies, owner.
- `pattern-decision`: selected or rejected AI architecture pattern.
- `quality-scenario`: attribute, stimulus, response, measure.
- `adr`: architecture decision record.
- `debt-item`: architecture or model-drift debt with mitigation.
- `validation`: deterministic completion checks.

## Relationships

- `ai-software-architecture` requires `system-context`.
- `system-context` is supported by `evidence`.
- `six-layer-stack` contains `component-contract`.
- `pattern-decision` enables `quality-scenario`.
- `adr` records `pattern-decision`.
- `debt-item` is mitigated by `evolution-plan`.
- `validation` checks all prior nodes.
