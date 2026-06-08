# Assets for genai-architecture

[CODE] These assets define the deterministic contracts used by `scripts/compile-genai-architecture.py`.

## Files

- `genai-architecture-schema.json` defines required input fields and allowed values.
- `rag-pattern-model.json` defines canonical RAG stages, variants, retrieval methods, and chunking strategies.
- `model-routing-matrix.json` defines model tiers, routing criteria, and fallback rules.
- `vector-db-selection-matrix.json` defines vector database candidates and deterministic selection rules.
- `connector-security-model.json` defines connector types, security controls, and fallback behaviors.
- `qa-metrics-model.json` defines GenAI quality metrics, guardrails, and improvement cadence.
- `genai-architecture-report-template.md` defines the Markdown report skeleton.
