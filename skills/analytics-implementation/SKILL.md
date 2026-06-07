---
name: analytics-implementation
description: GA4 setup. Firebase Analytics custom events. Conversions. User properties. BigQuery export. Looker Studio dashboards. [EXPLICIT]
version: 1.0.1
status: production
owner: Javier Montaño
tags: [data, analytics, ga4, firebase, bigquery, dashboard]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Analytics Implementation

Analytics Implementation turns a measurement plan into a verifiable GA4/Firebase implementation package with custom events, conversions, user properties, consent/privacy controls, BigQuery export, and Looker Studio readiness. [EXPLICIT]

## When To Use

- GA4 setup, Firebase Analytics setup, data streams, custom events, event parameters, conversions, audiences, user properties, BigQuery export, or Looker Studio dashboards.
- Implementation handoff for web, iOS, Android, backend, or Firebase projects.
- Analytics QA plans, DebugView validation, BigQuery export validation, consent mode, or privacy-safe analytics rollout.

## When Not To Use

- Firestore schema design, security rules, indexes, or backups without analytics instrumentation.
- Generic dashboard visual design without analytics implementation.
- Event taxonomy only, unless implementation details are requested.
- Warehouse transformation modeling after data is already exported.

## Deterministic Contract

Use `assets/` as the offline contract and `scripts/` as the deterministic oracle. The skill must not depend on network access, wall-clock time, random sampling, or unverifiable platform state. [EXPLICIT]

Required assets:
- `assets/analytics-implementation-contract.json` defines required sections and validation checks.
- `assets/ga4-policy.json` defines GA4/Firebase setup fields.
- `assets/event-policy.json` defines custom event and parameter rules.
- `assets/conversion-policy.json` defines conversion requirements.
- `assets/bigquery-policy.json` defines export and retention requirements.
- `assets/dashboard-policy.json` defines Looker Studio source and metric requirements.
- `assets/evidence-policy.json` defines evidence tags and provenance fields.

Offline validation:
- Use `scripts/validate_analytics_implementation.py` for structured JSON implementation plans.
- Use `bash scripts/check.sh` to validate deterministic fixtures.
- Block final delivery when GA4 setup, event contracts, conversions, user properties, export, dashboards, privacy, or QA evidence is missing.

## Procedure

### Step 1: Discover

- Identify platforms, GA4 properties, Firebase apps, data streams, destinations, consent constraints, and existing implementation gaps.
- Collect evidence for measurement requirements, current analytics stack, privacy constraints, and dashboard needs.

### Step 2: Specify Implementation

- Define GA4/Firebase setup, streams, SDK surfaces, consent mode, debug flow, and owners.
- Define custom events with parameters, platform, trigger, owner, and validation method.
- Define conversions and user properties with privacy review.
- Define BigQuery export settings, dataset ownership, retention, partitioning, and PII handling.
- Define Looker Studio dashboards and data source expectations.

### Step 3: QA And Rollout

- Validate events in DebugView or equivalent local/debug flow.
- Validate destination receipt and BigQuery rows.
- Validate conversion marking and dashboard freshness.
- Document rollback or deprecation steps for incorrect events.

## Quality Criteria

- [ ] GA4 or Firebase setup includes property/app, streams, owner, consent, and debug validation.
- [ ] Every custom event has trigger, owner, platform, parameters, destination, and evidence.
- [ ] Every event parameter has type and privacy classification.
- [ ] Every conversion references a known event and has an owner.
- [ ] Every user property has type, description, and PII classification.
- [ ] BigQuery export includes dataset, location, retention, partitioning, and PII handling.
- [ ] Looker Studio dashboards map to known data sources and metrics.
- [ ] Validation includes GA4 setup, event contract, conversions, user properties, BigQuery export, dashboards, privacy, and evidence.
- [ ] Structured JSON passes `scripts/validate_analytics_implementation.py`.

## Assumptions And Limits

- Assumes the user can provide project, platform, destination, or measurement context. [EXPLICIT]
- Does not replace legal review for consent mode or regulated data handling. [EXPLICIT]
- Does not implement SDK code unless explicitly requested; it defines an implementation and QA handoff. [EXPLICIT]
