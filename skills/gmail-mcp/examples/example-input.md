# Example Input

Use `gmail-mcp` to plan a safe inbox workflow:

- Search Gmail for recent messages about P-007 using `subject:"P-007" newer_than:14d -in:trash`.
- Read only the selected thread after the search results are narrowed.
- Draft a reply and do not send until I approve.
- Apply the label `Project/P-007` to two selected messages after I confirm the IDs.
- If the draft is approved, send it only after showing recipients, subject, body summary, and scope review.
- Do not store email bodies, attachments, credentials, or OAuth tokens.
