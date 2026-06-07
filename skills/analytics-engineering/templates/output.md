# {{project_name}} Analytics Engineering Plan

## Summary

{{summary}}

## Evidence

| Evidence ID | Tag | Source | Summary |
|---|---|---|---|
| {{evidence_id}} | {{tag}} | {{source}} | {{summary}} |

## Source-to-Target Mapping

| Source | Staging Model | Downstream Models | Freshness | Evidence |
|---|---|---|---|---|
| {{source}} | {{staging_model}} | {{downstream_models}} | {{freshness_sla}} | {{evidence_ids}} |

## Model Inventory

| Model | Layer | Grain | Materialization | Owner | Upstream |
|---|---|---|---|---|---|
| {{model_name}} | {{layer}} | {{grain}} | {{materialization}} | {{owner}} | {{upstream}} |

## Tests And Data Contracts

| Model | Blocking Tests | Contract Enforced | Breaking Change Policy |
|---|---|---|---|
| {{model_name}} | {{tests}} | {{contract_status}} | {{breaking_change_policy}} |

## Lineage

```mermaid
flowchart LR
  {{source_node}} --> {{staging_node}} --> {{mart_node}}
```

## Documentation Plan

| Model | Required Documentation | Owner |
|---|---|---|
| {{model_name}} | {{documentation_scope}} | {{owner}} |

## Validation

- Layer policy: {{layer_policy_status}}
- Materialization policy: {{materialization_policy_status}}
- Test policy: {{test_policy_status}}
- Contract policy: {{contract_policy_status}}
- Lineage complete: {{lineage_status}}
- Documentation policy: {{documentation_status}}

## Risks And Assumptions

{{risks_and_assumptions}}
