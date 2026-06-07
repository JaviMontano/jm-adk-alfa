# Example Output

```json
{
  "schema": "jm-labs.ai-code-review.report.v1",
  "target": "src/auth/session.ts",
  "scope": {
    "includes": ["src/auth/session.ts", "src/auth/session.test.ts"],
    "excludes": ["package-lock.json", "dist/**"],
    "basis": "User supplied review scope"
  },
  "review_mode": "standard",
  "evidence": [
    {
      "id": "E-001",
      "tag": "[CÓDIGO]",
      "kind": "source",
      "source": "src/auth/session.ts:42",
      "summary": "The rememberMe branch uses the same expiration as the default branch."
    }
  ],
  "findings": [
    {
      "id": "F-001",
      "priority": "P1",
      "category": "correctness",
      "status": "confirmed",
      "file": "src/auth/session.ts",
      "line_start": 42,
      "evidence_id": "E-001",
      "observation": "The rememberMe branch sets the default 30-minute expiration instead of the configured long-session expiration.",
      "impact": "Users who select persistent sessions are logged out earlier than the product contract describes.",
      "recommendation": "Use the long-session TTL for rememberMe and add a regression test for both branches.",
      "confidence": 0.91,
      "false_positive_notes": "The branch and product flag are both in the reviewed scope."
    }
  ],
  "summary": {
    "finding_count": 1,
    "highest_priority": "P1",
    "overall_risk": "high",
    "clean_review_rationale": ""
  },
  "validation": {
    "status": "warn",
    "checks": ["assets", "deterministic_scripts", "quality_criteria", "file_line_evidence", "false_positive_filter", "no_fake_test_results"],
    "commands_run": [],
    "claimed_test_status": "not-run"
  },
  "risks": ["Tests were not executed, so runtime behavior remains unverified."]
}
```
