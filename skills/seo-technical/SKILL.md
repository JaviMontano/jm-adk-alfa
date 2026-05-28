---
name: seo-technical
description: JSON-LD structured data, sitemap.xml, robots.txt, Open Graph tags, canonical URLs, and Firebase Hosting SEO headers
version: 1.0.0
status: production
owner: Javier Montaño
tags: [performance, seo, json-ld, sitemap, robots, open-graph, canonical, structured-data]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 097 — Technical SEO {Performance}

## Purpose
Ensure search engines can discover, crawl, and index all public pages correctly. Implement structured data for rich snippets, sitemaps for crawl efficiency, and Open Graph tags for social sharing. [EXPLICIT]

## Physics — 3 Immutable Laws

1. **Law of Crawlability**: If a search engine cannot reach and render a page, it does not exist. SPA rendering, robots.txt, and canonical URLs must work together. [EXPLICIT]
2. **Law of Structured Communication**: Machines understand structured data. JSON-LD tells Google what content means — not just what it says. [EXPLICIT]
3. **Law of Single Source**: Every page has exactly one canonical URL. Duplicate content is consolidated. Redirect chains are eliminated. [EXPLICIT]

## Protocol

### Phase 1 — Crawl Foundation
1. Generate `sitemap.xml` from route definitions. Include `lastmod`, `changefreq`, `priority`. [EXPLICIT]
2. Create `robots.txt`: allow all public paths, disallow `/admin/`, `/api/`. [EXPLICIT]
3. Configure Firebase Hosting headers: `X-Robots-Tag: index, follow` for public pages. [EXPLICIT]
4. For SPAs: implement prerendering (`react-snap`) or SSR for SEO-critical pages. [EXPLICIT]

### Phase 2 — Structured Data
1. Add JSON-LD `<script type="application/ld+json">` to page `<head>`. [EXPLICIT]
2. Implement schema types: `Organization`, `WebSite`, `BreadcrumbList`, `Article`, `Product` as applicable. [EXPLICIT]
3. Validate with Google Rich Results Test for every schema type. [EXPLICIT]
4. Dynamic pages: generate JSON-LD from Firestore data at render time. [EXPLICIT]

### Phase 3 — Meta Tags & Social
1. `<title>` unique per page, < 60 characters, keyword-front-loaded. [EXPLICIT]
2. `<meta name="description">` unique per page, < 160 characters, action-oriented. [EXPLICIT]
3. `<link rel="canonical">` on every page — self-referencing or pointing to primary URL. [EXPLICIT]
4. Open Graph: `og:title`, `og:description`, `og:image` (1200x630px), `og:url`. [EXPLICIT]
5. Twitter Card: `twitter:card=summary_large_image`, `twitter:title`, `twitter:image`. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| Route definitions | `sitemap.xml` with all public URLs |
| Content/page data | JSON-LD structured data per page |
| Page metadata | `<title>`, `<meta>`, OG tags per page |
| Firebase Hosting config | SEO-optimized headers |

## Quality Gates — 5 Checks

1. **sitemap.xml accessible** at `/sitemap.xml` — lists all public URLs. [EXPLICIT]
2. **robots.txt valid** — Google Search Console shows no crawl errors. [EXPLICIT]
3. **JSON-LD validates** — zero errors in Google Rich Results Test. [EXPLICIT]
4. **Canonical URLs on all pages** — no duplicate content issues. [EXPLICIT]
5. **OG image renders correctly** — test with Facebook Sharing Debugger. [EXPLICIT]

## Edge Cases

- **SPA rendering**: Google renders JS but prerendering is more reliable. Use `react-snap` or dynamic rendering.
- **Paginated content**: Use `rel="next"` / `rel="prev"` or load-more pattern with canonical to first page.
- **Multilingual**: `hreflang` tags for each language variant. Separate sitemaps per language.
- **Dynamic OG images**: Generate per-page OG images via Cloud Function if content varies.

## Self-Correction Triggers

- Pages missing from Google index → check sitemap, robots.txt, canonical tags.
- Rich results disappearing → revalidate JSON-LD, check for schema errors.
- Social shares show wrong image → verify OG tags, clear Facebook/Twitter cache.
- Crawl budget wasted → audit robots.txt, block non-essential paths from crawling.

## Usage

Example invocations:

- "/seo-technical" — Run the full seo technical workflow
- "seo technical on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
