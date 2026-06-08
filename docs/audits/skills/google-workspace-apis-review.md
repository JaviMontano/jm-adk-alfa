# google-workspace-apis review

## Decision

[CODE] `google-workspace-apis` is `dod-complete` for the deterministic skill
contract.

## Evidence

- [CODE] The skill includes complete core files, `assets/`, deterministic
  `scripts/`, fixtures, examples, evals, templates, knowledge, and agent files.
- [CODE] `scripts/compile-google-workspace-apis.py` validates multi-service
  Workspace plans offline and never calls Google APIs, OAuth, network resources,
  or MCP tools.
- [CODE] Negative fixtures reject missing consent, broad scopes, skipped
  read-before-write, and MCP tool/service mismatches.
- [DOC] Official sources used: Google Workspace overview/auth/MCP guide, Gmail,
  Calendar, Drive, Docs, Sheets, Slides REST references, and MCP tools spec.

## Checks

```text
python3 -B scripts/validate-skill-dod.py --skill google-workspace-apis
skill=google-workspace-apis dod=pass errors=0

python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-workspace-apis
skills_with_scripts=1 warnings=0 errors=0

bash skills/google-workspace-apis/scripts/check.sh
OK: google-workspace-apis scripts are deterministic and offline

python3 -B -m py_compile skills/google-workspace-apis/scripts/*.py
PASS
```

## Residual Limits

[INFERENCE] Offline validation does not prove Google Cloud API enablement,
OAuth consent, Workspace organization policy, quota, billing, live permissions,
or resource existence.
