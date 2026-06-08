# Example Output

## Summary

- [CODE] System: MetodologIA Knowledge Copilot.
- [CODE] Recommended pattern: Agentic RAG because at least one use case requires multi-step tool use.
- [CODE] Recommended vector store: Qdrant because the deployment is hybrid and the knowledge base is confidential.

## Architecture Slices

| Slice | Deterministic decision |
|---|---|
| RAG pipeline | Query processing, retrieval, context assembly, generation, validation |
| Retrieval | Hybrid vector plus keyword retrieval with ACL filters |
| Model routing | Tiered router with confidence escalation and cached fallback |
| Connectors | Documents plus CRM with row-level security and degraded fallback |
| QA | Retrieval recall, faithfulness, citation accuracy, latency, cost |

## Validation

- [CODE] Required RAG stages are present.
- [CODE] Knowledge sources include owner, access model, sensitivity, and update frequency.
- [CODE] Model tiers include trigger and fallback behavior.
- [CODE] Connectors include security control and degraded fallback.
- [CODE] Quality targets include metric, target, measurement, and owner.

## Risks

- [INFERENCE] Architecture recommendations require benchmark validation before production rollout.
- [ASSUMPTION] Input evidence and constraints are accepted as the source of truth for this deterministic report.
