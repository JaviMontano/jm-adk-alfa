# Pdf Architecture Reviewer

`pdf-architecture-reviewer` turns a read PDF or attachment excerpt into a deterministic architecture review. It maps every architecture claim to page evidence, compares the claim with repository evidence, records contradictions, and identifies which official source must confirm the claim before a change is authorized.

The skill must not treat an attachment name, user summary, screenshot, or unread PDF as evidence. Evidence starts only after page text has been extracted, paginated, and recorded in the report contract.

## Deterministic Contract

The canonical offline report shape lives in `assets/pdf-architecture-reviewer-contract.json`. A valid report includes:

- `document` metadata with `extraction_status: "read"`, `sha256`, `page_count`, and `pages_reviewed`.
- `page_evidence` entries with page numbers, excerpts, extraction method, and linked claim IDs.
- `architecture_claims` that trace to page evidence and repository mapping.
- `repo_mapping` entries that compare PDF claims to code, docs, config, or missing repo evidence.
- `official_source_requirements` for claims that need official documentation before implementation.
- `contradictions`, `decisions`, `validation`, and `guardian` sections.

## Local Validation

Run the deterministic check:

```bash
bash skills/pdf-architecture-reviewer/scripts/check.sh
```

The check validates known-good report fixtures and rejects mutated reports that skip PDF reading, omit page evidence, authorize unsupported changes, or pass Guardian despite unresolved contradictions.

## Output Standard

The output should separate PDF evidence from repo evidence and decision evidence. If a claim lacks page evidence, repo mapping, or required official source coverage, mark it as blocked or unverified instead of turning it into implementation guidance.
