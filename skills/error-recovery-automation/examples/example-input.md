# Example Input

Our nightly GitHub Actions job failed while publishing a QA report.

- Failed command: `python3 -B scripts/qa/run-adversarial-tests.py`
- Exit code: `1`
- Last safe checkpoint: commit `abc1234`
- Error excerpt: `requests.exceptions.Timeout: qa fixture service did not respond`
- Current state: no deployment happened, no database migration ran, and no report
  artifact was uploaded
- Desired outcome: decide whether retry is safe, define retry bounds, and provide
  validation evidence before closing the incident
