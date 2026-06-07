# Analytics Engineering Knowledge Graph

## Core Nodes

- `analytics-engineering`: transformation design capability.
- `source-inventory`: source systems, tables, owners, and freshness.
- `model-layer`: staging, intermediate, mart, and metrics models.
- `materialization`: view, ephemeral, table, incremental, snapshot, or semantic layer.
- `data-test`: schema, relationship, accepted-value, freshness, custom, or reconciliation test.
- `data-contract`: enforced schema and breaking-change policy.
- `lineage`: source-to-model and model-to-exposure dependency path.
- `documentation`: model and column descriptions for discovery.

## Required Edges

- `source-inventory` feeds `model-layer`.
- `model-layer` is constrained by `materialization`.
- `model-layer` is validated by `data-test`.
- `model-layer` is governed by `data-contract`.
- `lineage` connects every production mart to upstream sources.
- `documentation` explains each production mart and its columns.

## Guardrail

If a mart lacks grain, owner, tests, lineage, or contract status, the Guardian blocks final delivery.
