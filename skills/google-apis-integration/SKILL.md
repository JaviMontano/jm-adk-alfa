---
name: google-apis-integration
author: JM Labs (Javier Montano)
version: 1.0.0
description: "Multi-service Google API integration planning for Google Sheets API v4, Docs API v1, Calendar API v3, Maps JavaScript API, and YouTube Data API v3 with deterministic offline auth, scope, quota, retry, consent, secrets, operation, and test-matrix checklists. [DOC]"
triggers:
  - google apis
  - google api integration
  - sheets docs calendar maps youtube
  - oauth scopes
  - multi google api
status: production
owner: Javier Montaño
tags: [backend, google-apis, oauth2, sheets, docs, calendar, maps, youtube]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Google APIs Integration

## TL;DR

Use this skill to compile a safe, offline integration plan across Sheets, Docs,
Calendar, Maps JavaScript, and YouTube Data APIs. The deterministic compiler is
`scripts/compile-google-apis-integration.py`; it reads only local `assets/` and
JSON fixtures, renders Markdown or JSON, and never calls Google, OAuth, HTTP,
network, or MCP tools. [CODE]

## Deterministic Assets

- `assets/google-apis-integration-schema.json` defines the stable input contract. [CODE]
- `assets/service-catalog.json` maps services to official REST or client-side operations. [DOC]
- `assets/auth-scope-policy.json` encodes least-privilege OAuth scopes and API-key profiles. [DOC]
- `assets/error-retry-policy.json` defines retry, quota, backoff, and idempotency gates. [DOC]
- `assets/consent-secrets-policy.json` defines human consent and secret-handling policy. [CODE]
- `assets/test-matrix-policy.json` defines required test layers for multi-API plans. [CODE]
- `assets/source-map.md` records the primary official references used by this skill. [DOC]
- `assets/google-apis-integration-template.md` renders the offline report. [CODE]

## Procedure

### Step 1: Classify Services And Operations

- Select one or more service entries: `sheets`, `docs`, `calendar`, `maps_js`, or `youtube`. [CODE]
- Map every requested action to an operation in `assets/service-catalog.json`. [DOC]
- Separate read-only, browser-render, and mutating operations before selecting credentials. [CODE]

### Step 2: Select Auth And Scopes

- Use OAuth 2.0 profiles for Workspace and YouTube user-data operations. [DOC]
- Use a restricted API key profile for Maps JavaScript browser loading and public YouTube reads when user data is not required. [DOC]
- Choose the narrowest profile in `assets/auth-scope-policy.json`; broad write scopes require an explicit escalation reason. [CODE]
- Keep client secrets, refresh tokens, and OAuth token exchange server-side. [CODE]

### Step 3: Build The Offline Operation Plan

- Include resource identifiers, selected auth profile, requested scopes, retry policy, quota strategy, and idempotency key for each service operation. [CODE]
- For mutating operations, include read-before-write evidence unless the operation is explicitly modeled as browser-render or public read. [CODE]
- For Maps JavaScript, include key restriction and allowed API checks instead of OAuth scopes. [DOC]

### Step 4: Gate Consent, Retries, And Idempotency

- Mutating operations require `human_consent.status=confirmed` and confirmation text beginning with the configured consent phrase. [CODE]
- Mutating operations require a stable `idempotency_key` so retries can be correlated and duplicate effects can be reviewed. [CODE]
- Retry plans must distinguish user-fix errors, auth refresh/re-auth, quota/rate-limit backoff, and transient 5xx retry. [DOC]

### Step 5: Validate And Export

- Run `bash skills/google-apis-integration/scripts/check.sh` after modifying this skill. [CODE]
- Use Markdown output for human review and JSON output for stable downstream automation. [CODE]
- Live API execution remains outside this skill; this skill compiles a plan/checklist only. [CODE]

## Quality Criteria

- [ ] Operations map to official Sheets, Docs, Calendar, Maps JavaScript, or YouTube API surfaces. [DOC]
- [ ] Auth profile and requested scopes are least privilege for each operation. [DOC]
- [ ] Maps JavaScript uses restricted API-key policy rather than OAuth scopes. [DOC]
- [ ] Mutations have human consent, read-before-write evidence, retry policy, and idempotency key. [CODE]
- [ ] Secrets policy blocks client-side OAuth secrets, static tokens, and committed credentials. [CODE]
- [ ] Quota/error handling covers 400, 401, 403, 429, 5xx, refresh/re-auth, and backoff behavior. [DOC]
- [ ] Test matrix includes unit, contract, integration-sandbox, e2e-preview, security, quota-error, and consent-gate layers. [CODE]
- [ ] `assets/`, `scripts/`, examples, evals, prompts, templates, and knowledge stay deterministic and offline. [CODE]

## Anti-Patterns

- Requesting full Google account scopes for read-only discovery. [DOC]
- Shipping OAuth client secrets, refresh tokens, or service account keys in browser code or fixtures. [CODE]
- Treating Maps JavaScript browser loading as an OAuth flow. [DOC]
- Retrying mutating operations without an idempotency key or read-back plan. [CODE]
- Sending Calendar invitations, editing Docs/Sheets, or uploading YouTube data without explicit consent. [CODE]
- Calling live Google APIs from local skill scripts or fixtures. [CODE]

## Usage

- `/google-apis-integration` to plan a multi-Google-API integration. [CODE]
- `python3 skills/google-apis-integration/scripts/compile-google-apis-integration.py --input skills/google-apis-integration/scripts/fixtures/google-apis-integration-input.json`. [CODE]
- `python3 skills/google-apis-integration/scripts/compile-google-apis-integration.py --format json --input skills/google-apis-integration/scripts/fixtures/google-apis-integration-input.json`. [CODE]
- `bash skills/google-apis-integration/scripts/check.sh`. [CODE]

## Assumptions & Limits

- The compiler validates local JSON and assets only; it does not verify live OAuth clients, enabled APIs, quotas, ACLs, domain policy, or billing state. [CODE]
- Generated scopes and operations must be reviewed against the target Google Cloud project before deployment. [DOC]
- API references can evolve; rerun a source review against official Google docs before changing policies or publishing externally. [DOC]
