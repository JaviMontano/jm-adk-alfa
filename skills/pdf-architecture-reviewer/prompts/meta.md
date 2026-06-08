# Pdf Architecture Reviewer Meta Prompt

Activate `pdf-architecture-reviewer` only when a PDF or attachment is the source of architecture claims.

## Activation Check

- Does the user ask to review architecture from a PDF, attachment, pasted extraction, or document?
- Is the document read into page-indexed text or can the result be blocked until extraction is provided?
- Does the task require mapping document claims to repo evidence?
- Does the task need official source requirements before implementation?

## Non-Activation Cases

- Plain repo architecture review with no document.
- Official docs verification with no PDF claim source.
- Generic summarization where page evidence is irrelevant.
- A request to approve changes from an unread attachment.

## Agent Routing

- Lead owns report assembly.
- Specialist owns claim normalization and repo mapping.
- Support checks missing pages, paths, and official source gaps.
- Guardian blocks unread, untraceable, contradictory, or unsourced decisions.
