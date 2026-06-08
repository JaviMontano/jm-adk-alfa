# Example Input

[CODE] The deterministic script consumes structured JSON like `scripts/fixtures/genai-architecture-input.json`.

```json
{
  "system_name": "MetodologIA Knowledge Copilot",
  "audience": "Founders, presales architects, and implementation engineers",
  "business_goal": "Answer methodology and client-delivery questions with cited internal knowledge and controlled tool use.",
  "scope": "technical",
  "deployment_preference": "hybrid",
  "data_sensitivity": "confidential",
  "knowledge_base": {
    "size": "large",
    "update_frequency": "daily",
    "languages": ["es", "en"],
    "source_count": 1280
  },
  "knowledge_sources": [
    {
      "name": "Jarvis OS canon",
      "type": "documents",
      "update_frequency": "daily",
      "access_model": "filesystem ACL plus manifest",
      "sensitivity": "confidential",
      "owner": "methodology-ops"
    }
  ],
  "rag_pipeline": [
    {
      "id": "retrieval",
      "decision": "Use hybrid vector plus keyword retrieval with ACL filters.",
      "mechanism": "Qdrant hybrid search with metadata filters and reciprocal rank fusion.",
      "owner": "knowledge-platform",
      "metric": "retrieval_recall_at_k"
    }
  ],
  "evidence": {
    "source_inventory": "1280 governed documents"
  }
}
```

[CODE] The complete fixture also includes all five RAG stages, use cases, model tiers, connectors, and quality targets.
