# Alert Priority

Alert levels are **work priority labels only**. They must never be presented as legal compliance, legality, liability, or appraisal appropriateness determinations.

## Levels

| Level | Meaning | Safe copy |
|---|---|---|
| high | Review this first because retrieved evidence, source metadata, or date filters suggest stronger operational relevance. | `작업 우선순위: high` |
| medium | Review after high priority items; evidence is relevant but less complete. | `작업 우선순위: medium` |
| low | Evidence is weak, metadata is missing, or additional review is needed before action. | `작업 우선순위: low` |

## Confidence and Review

If source authority, citations, or date metadata are missing, the result should show low confidence or 추가 확인 필요. The system must not convert weak evidence into a confident conclusion.

## Explanation Policy

When a user asks “왜 high야?”, explain:

- 검색 근거 relevance
- citation count and source authority
- date filter condition and date field used
- limitation that this is not final legal/professional judgment

## Manual Supplementation

Manual supplementation can add verified source authority or date fields. It cannot add legal conclusions or liability judgments.

## Agent Limitation

The agent can rank work priority from available metadata but cannot certify legality, compliance, or professional appraisal correctness.

## Prerequisite Work

- Stable official source metadata
- Citation coverage
- Date filter metadata quality
- Human review workflow for high priority operational follow-up
