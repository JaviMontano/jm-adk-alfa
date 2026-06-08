# GenAI Architecture — Body of Knowledge

## Canon

[CODE] GenAI architecture is the system design discipline for LLM-powered products that retrieve knowledge, route work across model tiers, execute controlled tools, and validate grounded answers.

[CODE] The skill treats RAG as a full pipeline: query processing, retrieval, context assembly, generation, and validation. [CODE] `assets/rag-pattern-model.json` is the executable source for required RAG stages and variants.

## Deterministic Contracts

- [CODE] `assets/genai-architecture-schema.json` defines required input fields and allowed values.
- [CODE] `assets/rag-pattern-model.json` defines RAG variants, stages, retrieval methods, and chunking strategies.
- [CODE] `assets/model-routing-matrix.json` defines LLM tiers, routing criteria, and fallback controls.
- [CODE] `assets/vector-db-selection-matrix.json` defines vector database candidates and recommendation rules.
- [CODE] `assets/connector-security-model.json` defines connector security controls and degraded behavior.
- [CODE] `assets/qa-metrics-model.json` defines retrieval, generation, citation, latency, and cost metrics.

## Quality Metrics

| Metric | Target | How to Measure |
|---|---|---|
| Retrieval recall | >= 0.85 | Labeled question set and expected evidence |
| Faithfulness | >= 0.90 | Grounding judge plus human sample |
| Citation accuracy | >= 0.95 | Source support audit |
| P95 latency | SLA-specific | Production telemetry |
| Cost per answer | Budget-specific | Inference and retrieval cost logs |

## Architecture Rules

1. [CODE] Retrieval quality is a first-order architecture decision, not prompt decoration.
2. [CODE] Model routing must define tier, trigger, fallback, and budget control.
3. [CODE] Vector database selection must reflect deployment preference, sensitivity, metadata filtering, scale, and operations model.
4. [CODE] Connectors must preserve authorization boundaries and expose degraded fallback behavior.
5. [CODE] Guardrails must run before final output when sources, tools, or sensitive data are involved.

## References

- [CODE] `references/rag-patterns.md`
- [CODE] `references/llm-orchestration.md`
- [CODE] `references/vector-db-comparison.md`
