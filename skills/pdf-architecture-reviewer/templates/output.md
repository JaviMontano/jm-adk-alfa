# Pdf Architecture Review

## Document Status

- document_id: `{document_id}`
- file_name: `{file_name}`
- sha256: `{sha256}`
- extraction_status: `{extraction_status}`
- pages_reviewed: `{pages_reviewed}`

## Page Evidence

| Evidence ID | Page | Excerpt | Claim IDs |
|---|---:|---|---|
| `{evidence_id}` | `{page}` | `{excerpt}` | `{claim_ids}` |

## Architecture Claims

| Claim ID | Claim | Status | Page Evidence | Repo Mapping | Official Source Required |
|---|---|---|---|---|---|
| `{claim_id}` | `{claim}` | `{status}` | `{page_evidence_ids}` | `{repo_refs}` | `{official_source_required}` |

## Repository Mapping

Record the path, observed state, and whether each repo artifact supports, contradicts, is missing, or was not checked for the claim.

## Official Source Requirements

List the official source kind required before each implementation decision and whether it is required, satisfied, or blocked.

## Contradictions

Record each PDF/repo conflict with severity, involved claim, repo path, and resolution status.

## Decisions

State `authorize`, `block`, or `defer`, with claim IDs and blocking gaps.

## Validation

Report each validation flag from the deterministic contract and include the Guardian decision.
