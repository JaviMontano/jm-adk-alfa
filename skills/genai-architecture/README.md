# GenAI Architecture

[CODE] Use this skill to design production-grade generative AI systems with RAG, model routing, agent workflows, vector store selection, knowledge connectors, and quality guardrails.

## Triggers

- `genai-architecture`
- `design RAG architecture`
- `architect LLM system`
- `select vector database`
- `design AI agents`
- `plan GenAI quality`

## Deterministic Bundle

- [CODE] `assets/` stores schemas, decision matrices, architecture models, and the report template.
- [CODE] `scripts/compile-genai-architecture.py` converts structured JSON into a deterministic Markdown report.
- [CODE] `scripts/check.sh` runs the fixture, verifies expected fragments, and confirms invalid input fails.

## Quick Use

```bash
python3 skills/genai-architecture/scripts/compile-genai-architecture.py \
  --input skills/genai-architecture/scripts/fixtures/genai-architecture-input.json
```

## Output Format

[CODE] Markdown report with executive summary, evidence, knowledge profile, RAG pipeline, LLM orchestration, vector database decision, connectors, quality gates, validation, and limits.
