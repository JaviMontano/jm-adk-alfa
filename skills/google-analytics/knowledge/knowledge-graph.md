# Google Analytics — Knowledge Graph

## Core Concepts

- [[ga4-property]] — GA4 account/property/data-stream readiness.
- [[google-tag]] — Direct Google tag / gtag.js setup surface.
- [[google-tag-manager]] — GTM container, tags, triggers, variables, preview, publish.
- [[event-taxonomy]] — Automatic, enhanced measurement, recommended, and custom event classification.
- [[recommended-events]] — Official GA4 event names for standardized reporting.
- [[key-events]] — Business-critical events formerly described as conversions in many workflows.
- [[measurement-protocol]] — Supplemental server-to-server/offline event collection.
- [[consent-mode]] — Consent-aware tag behavior.
- [[debugview]] — GA4 debug verification surface.
- [[tag-assistant]] — GTM and tag debugging surface.

## Edges

- [[event-taxonomy]] validates [[key-events]].
- [[consent-mode]] gates [[google-tag]] and [[google-tag-manager]] collection.
- [[measurement-protocol]] supplements [[google-tag]] and [[google-tag-manager]].
- [[tag-assistant]] verifies [[google-tag-manager]] before publish.
- [[debugview]] verifies [[event-taxonomy]] delivery.

## Tags

#google-analytics #ga4 #gtm #tag-platform #measurement #jm-adk
