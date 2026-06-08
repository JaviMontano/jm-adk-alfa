---
name: pdf-architecture-reviewer
version: 1.0.0
description: "Extract architecture from a PDF/attachment and map claims to the repo: evidence per page, contradictions, decisions, and which official source each claim requires. Never treats a PDF as evidence before reading it."
owner: "JM Labs (Javier Montaño)"
triggers:
  - pdf architecture
  - attachment review
  - claim mapping
  - document architecture
  - pdf evidence
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Pdf Architecture Reviewer

## Purpose

Use this skill when a user asks for architecture findings from a PDF, attachment, pasted page extraction, or document-derived architecture review. The skill exists to keep PDF claims separate from repo facts and official-source decisions.

## Activation Rules

Activate only when the task depends on architecture content from a PDF or attachment. Do not activate for general repo architecture review with no document, source verification with no attachment, or generic summarization.

If the PDF or attachment has not been read into page-indexed text, stop and request extraction or mark the report blocked. A file name, user paraphrase, or screenshot thumbnail is not evidence.

## Inputs Required

- Document identifier, file name, checksum, extraction method, page count, and pages reviewed.
- Page-indexed excerpts for each claim under review.
- Repository paths, docs, configs, or code snippets used for comparison.
- Official-source topics required before implementing or changing architecture.
- Acceptance criteria for whether the result should authorize, block, or defer action.

## Procedure

### 1. Read and Register the Document

Record `extraction_status: "read"` only after page-indexed text exists. Capture the SHA-256 or fixture hash, page count, pages reviewed, and extraction method. If the document cannot be read, produce a blocked report.

### 2. Extract Page Evidence

Create one evidence record per architecture assertion. Each record must include page number, excerpt, extraction method, and the claim IDs it supports.

### 3. Normalize Architecture Claims

Turn excerpts into atomic claims. Each claim must include status, page evidence references, repository references, whether an official source is required, and its decision impact.

### 4. Map Claims to the Repository

Compare every claim with code, docs, configs, or absence in the repo. Mark mappings as `supports`, `contradicts`, `missing`, or `not_checked`. Do not infer repo alignment from the PDF alone.

### 5. Identify Official Source Requirements

For implementation-impacting claims, name the official source type needed before action, such as vendor docs, framework docs, product docs, standards, or internal architecture decision records. A PDF can motivate a question; it cannot be the final authority for framework or platform behavior.

### 6. Resolve Decisions

Authorize work only when page evidence exists, repo mapping is traceable, contradictions are resolved, and required official sources are satisfied. Otherwise, block or defer with explicit gaps.

### 7. Validate Offline

When producing a structured report, validate it against `scripts/validate_pdf_architecture_reviewer.py` or the equivalent contract rules. The `assets/` directory is the source of truth for contract fields, evidence policy, repo mapping policy, official source requirements, and decision safety. Preserve validation evidence in the handoff.

## Output Contract

Follow `templates/output.md` and keep these sections distinct:

- Document read status.
- Page evidence.
- Architecture claims.
- Repository mapping.
- Official source requirements.
- Contradictions and decisions.
- Validation and Guardian decision.

## Quality Criteria

- Every claim traces to at least one page evidence ID.
- Every implementation-impacting claim has repo mapping.
- Required official sources are named before any change is authorized.
- Contradictions block authorization unless resolved.
- Guardian cannot pass a report that treats an unread PDF as evidence.

## Edge Cases

- Missing attachment: return blocked with required inputs.
- Unread PDF: return blocked; do not summarize from filename or user paraphrase.
- OCR degradation: mark low-confidence excerpts and avoid authorization unless corroborated.
- PDF/repo conflict: record contradiction and block until resolved.
- No official source available: mark decision as blocked or deferred.

## Related Skills

- `official-source-verifier`
- `repo-structure-navigation`
- `architecture-review`
- `quality-guardian`
