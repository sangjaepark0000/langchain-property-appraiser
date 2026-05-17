# Recent Period Filter Design

## Purpose

Recent-period filtering lets a query such as “최근 1년 안에 개정된 고시” become a structured filter candidate. The filter is applied after vector retrieval in the current MVP so existing pgvector/local retrieval paths remain simple.

## Supported Natural Language

Supported patterns:

- `최근 1년`
- `최근 6개월`
- `최근 30일`

Unsupported/uncertain pattern:

- `최근 변경사항` without amount/unit returns `needs_clarification`.

## Date Field Policy

Default preferred date fields:

1. `revision_date` — 개정일, preferred when the user asks about changed/revised material.
2. `effective_date` — 시행일, fallback when revision date is missing.

The result must report which date field was used. Missing dates are never fabricated.

## Missing Metadata Behavior

If a retrieved chunk/document has no valid `revision_date` or `effective_date`, the filter excludes it from the filtered result and reports a limitation: date metadata was missing for some chunks.

This is not an API/server error. It means filter quality is limited by source metadata.

## Manual Supplementation

Manual supplementation can help when official sources expose dates visually but the parser cannot extract them yet:

1. Export source id, source URL, source title, and missing date fields.
2. Human reviewer copies only visible official dates.
3. Store review evidence and reviewer timestamp in metadata.
4. Do not infer dates from context or neighboring documents.

## Agent Limitation

Current agent limitation:

- The agent cannot verify live official source recency without source/API access.
- The parser cannot safely infer ambiguous date labels.
- PDF/HWP/OCR attachments may need manual review or dedicated extraction quality checks.

## Prerequisite Work

Prerequisite work for stronger automation:

- Source-specific date-label fixtures.
- Live API credential and recorded response policy.
- Dedupe/version policy for repeated official collection.
- Query/API contract for exposing filter status and limitations to frontend.
