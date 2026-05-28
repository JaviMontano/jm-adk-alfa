---
name: monitoring-alerting
description: Firebase Crashlytics, Performance Monitoring, Cloud Logging, Cloud Monitoring alerts, and uptime checks
version: 1.0.0
status: production
owner: Javier Montaño
tags: [devops, monitoring, alerting, crashlytics, performance, cloud-logging, uptime]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 092 — Monitoring & Alerting {DevOps}

## Purpose
Establish comprehensive observability across the application stack. Detect crashes, performance degradation, and downtime proactively through Firebase and Google Cloud monitoring tools. [EXPLICIT]

## Physics — 3 Immutable Laws

1. **Law of Observability**: If it's not monitored, it's not in production. Every service (hosting, functions, firestore, auth) has active monitoring. [EXPLICIT]
2. **Law of Alert Fatigue Prevention**: Alerts fire only on actionable conditions. No informational alerts — only conditions requiring human intervention. [EXPLICIT]
3. **Law of Mean Time to Detect**: MTTD < 5 minutes for critical issues. Uptime checks run every 60 seconds. Crash reports arrive in real-time. [EXPLICIT]

## Protocol

### Phase 1 — Crash & Error Monitoring
1. Enable Firebase Crashlytics for web: `import { getPerformance } from 'firebase/performance'`. [EXPLICIT]
2. Configure global error boundary in React to report uncaught errors. [EXPLICIT]
3. Cloud Functions: structured logging with `functions.logger` — errors auto-surface in Cloud Logging. [EXPLICIT]
4. Set up Cloud Logging sink for error-level logs → alert channel. [EXPLICIT]

### Phase 2 — Performance Monitoring
1. Initialize Firebase Performance Monitoring SDK in app entry point. [EXPLICIT]
2. Add custom traces for critical operations: `perf.trace('checkout-flow')`. [EXPLICIT]
3. Monitor Cloud Functions execution time via Cloud Monitoring metrics. [EXPLICIT]
4. Set performance budgets: page load < 3s, function execution < 10s. [EXPLICIT]

### Phase 3 — Alerts & Uptime
1. Cloud Monitoring uptime check: HTTPS GET on production URL every 60s. [EXPLICIT]
2. Alert policies: error rate > 1% → email + Slack. Uptime check fails 2x → page. [EXPLICIT]
3. Firestore usage alert: reads > 50K/day or writes > 10K/day → email. [EXPLICIT]
4. Billing alert: projected spend > budget threshold → email + pause non-critical functions. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| Application errors/crashes | Crashlytics dashboard + alert |
| Page loads and custom traces | Performance Monitoring dashboard |
| Cloud Functions logs | Cloud Logging queries + alerts |
| Production URL | Uptime check status (up/down) |

## Quality Gates — 5 Checks

1. **Crashlytics enabled** — crash-free rate visible in Firebase Console. [EXPLICIT]
2. **Uptime check active** — 60-second interval on production URL. [EXPLICIT]
3. **Alert channels configured** — email + Slack/PagerDuty for critical alerts. [EXPLICIT]
4. **Billing alerts set** — threshold at 80% of monthly budget. [EXPLICIT]
5. **Error rate dashboard exists** — real-time error rate visible to team. [EXPLICIT]

## Edge Cases

- **Crash in error boundary**: Implement fallback logging (beacon API) for catastrophic failures.
- **Cold start noise**: Exclude first invocation from function performance baselines.
- **Alert storms**: Set alert cooldown period (5 min) to prevent notification flooding.
- **Third-party outages**: Monitor external API dependencies separately from app health.

## Self-Correction Triggers

- Crash-free rate drops below 99.5% → immediate investigation and hotfix.
- Uptime check fails → verify hosting, DNS, SSL certificate status.
- Performance regression detected → run Lighthouse audit (skill 096).
- Billing spike → audit Firestore queries (skill 100), check for infinite loops in functions.

## Usage

Example invocations:

- "/monitoring-alerting" — Run the full monitoring alerting workflow
- "monitoring alerting on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
