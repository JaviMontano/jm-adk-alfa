# Pdf Architecture Reviewer Primary Prompt

## Objective

Produce a deterministic architecture review from a PDF or attachment extraction. Separate document claims, repository facts, official-source requirements, contradictions, decisions, and Guardian status.

## Required Inputs

- Page-indexed document extraction with checksum and pages reviewed.
- Repository paths or search targets to compare against each claim.
- Decision goal: authorize, block, defer, or produce risk inventory.
- Constraints for official sources required before implementation.

## Process

1. Verify the document is read before treating any content as evidence.
2. Extract atomic architecture claims from page excerpts.
3. Map each claim to repo evidence or absence.
4. Name official source requirements for implementation-impacting claims.
5. Record contradictions and unresolved gaps.
6. Produce a structured report compatible with `assets/pdf-architecture-reviewer-contract.json`.
7. Validate that Guardian cannot pass unresolved or unread-document cases.

## Output

Return Markdown or JSON using `templates/output.md`. If JSON is requested, keep it compatible with `scripts/validate_pdf_architecture_reviewer.py`.
