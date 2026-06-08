# Example Input

Design a Google Workspace automation for a weekly client status workflow.

Requirements:

- Read rows from a tracking spreadsheet.
- Create a status document from approved summary content.
- Upload the generated report to a Drive folder.
- Send a Gmail draft to the account owner for review, not a live email.
- Add a Calendar follow-up event only after explicit confirmation.
- Prefer MCP for interactive execution, but keep REST method mapping visible.
- Use least-privilege scopes and keep all credentials out of the repository.
- Produce an offline validation plan before any live call.
