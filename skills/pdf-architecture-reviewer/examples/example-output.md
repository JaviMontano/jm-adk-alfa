# Example Output

```json
{
  "schema": 1,
  "skill": "pdf-architecture-reviewer",
  "report_id": "pdf-architecture-reviewer-example",
  "document": {
    "document_id": "architecture-modernization",
    "file_name": "architecture-modernization.pdf",
    "sha256": "2f7c9a65d4c7e55a1ce99bce3f1e3841f2e73d14524b6ddca62dc4d98e0e66c7",
    "extraction_status": "read",
    "extraction_method": "text_layer",
    "page_count": 42,
    "pages_reviewed": [4, 5, 6]
  },
  "page_evidence": [
    {
      "evidence_id": "pe-001",
      "page": 4,
      "excerpt": "Payment events are published to a durable queue before settlement.",
      "extraction_method": "text_layer",
      "claim_ids": ["claim-queue"]
    }
  ],
  "architecture_claims": [
    {
      "claim_id": "claim-queue",
      "claim": "Payment events must use a durable queue before settlement.",
      "status": "supported",
      "page_evidence_ids": ["pe-001"],
      "repo_refs": [
        {
          "path": "services/payments/config/messaging.yml",
          "mapping_status": "supports",
          "observed_state": "queue transport is configured for settlement events"
        }
      ],
      "official_source_required": true,
      "decision_impact": "Implementation needs vendor queue durability documentation before changing runtime settings."
    }
  ],
  "official_source_requirements": [
    {
      "claim_id": "claim-queue",
      "source_kind": "vendor_docs",
      "requirement_reason": "Queue durability semantics must be confirmed by the official vendor documentation.",
      "status": "required",
      "official_source_ids": []
    }
  ],
  "contradictions": [],
  "decisions": [
    {
      "decision_id": "decision-001",
      "action": "block",
      "claim_ids": ["claim-queue"],
      "rationale": "The PDF and repo mapping are traceable, but the required official source is not yet satisfied.",
      "blocking_gaps": ["official source required for claim-queue"]
    }
  ],
  "validation": {
    "pdf_read_before_evidence": true,
    "page_evidence_present": true,
    "claims_trace_to_pages": true,
    "repo_mapping_traceable": true,
    "official_sources_identified": true,
    "contradictions_recorded": true,
    "deterministic_script_passed": true
  },
  "guardian": {
    "decision": "block",
    "reason": "Implementation is blocked until the official vendor source is verified."
  }
}
```
