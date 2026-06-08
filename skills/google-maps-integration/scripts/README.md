# Google Maps Integration Scripts

[CODE] `compile-google-maps-plan.py` compiles a deterministic offline Markdown plan from a local JSON input.
[CODE] `check.sh` runs the positive fixture and negative fixtures without network access.

## Contract

- [CODE] Inputs live under `scripts/fixtures/*.json`.
- [CODE] Outputs are generated into temporary files by checks.
- [CONFIG] The scripts do not call Google APIs, Cloud Console, OAuth, package registries, or any external URL.
- [CONFIG] The scripts reject monetary amounts because this skill outputs billing/quota risk checks without prices.

## Example

```bash
python3 skills/google-maps-integration/scripts/compile-google-maps-plan.py \
  --input skills/google-maps-integration/scripts/fixtures/google-maps-plan-input.json \
  --output /tmp/google-maps-platform-plan.md
```
