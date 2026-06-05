# User Representative Scripts

`validate_user_representative_review.py` checks Markdown review packets for the deterministic contract defined in `scripts/fixtures/review-contract.json`.

The script validates:

- Required review sections.
- Five scorecard dimensions with numeric `/10` scores.
- At least five `MA-N` micro-adjustments.
- Allowed evidence tags and blocked legacy tags.
- Correct `PASS`, `CONDITIONAL`, or `FAIL` verdict derived from scores.

Run:

```bash
bash skills/user-representative/scripts/check.sh
```
