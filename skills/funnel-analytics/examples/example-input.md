# Example Input

Analyze our SaaS signup-to-activation funnel for the last 30 days.

Available evidence:

- Tracking plan lists `landing_viewed`, `signup_started`, `signup_completed`, `workspace_created`, `invite_sent`, and `first_report_exported`.
- Dashboard shows counts by user for UTC dates 2026-05-01 to 2026-05-30:
  - landing_viewed: 12,400
  - signup_started: 3,100
  - signup_completed: 2,480
  - workspace_created: 1,910
  - invite_sent: 850
  - first_report_exported: 420
- Known filters: employees and test accounts excluded; bots not verified.
- Segments available: acquisition channel and plan type.
- Need: identify top drop-off risks, tracking gaps, and experiment backlog. Do not assume causality.
