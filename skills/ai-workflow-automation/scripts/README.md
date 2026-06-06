# AI Workflow Automation Scripts

`check.sh` validates deterministic workflow plan fixtures offline. It accepts
plans with bounded AI steps, approval gates, handoffs, and fallbacks, and rejects
missing approvals, missing AI output contracts, unbounded retries, incomplete
handoffs, and moving time language.
