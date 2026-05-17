# Domain Metadata Schema

## Purpose

`domain_metadata` extends the canonical document `metadata` dictionary for official 법령·고시 and appraisal-domain sources. This story defines the contract only. It does not require a new DB column yet; loaders should place this object under `documents.metadata.domain_metadata` and copy relevant values into chunk metadata for citation/retrieval.

## Compatibility Rules

- Existing sample/local documents remain valid without `domain_metadata`.
- For `data_mode=official`, loaders should populate `domain_metadata` whenever the source provides the value.
- Missing values must be represented as `null` when truly absent or `"unknown"` when the loader cannot determine the value from the source.
- Do not fabricate 없는 공식 metadata such as 법령명, 조항, 개정일, 시행일, source URL, or source authority.

## Object Shape

```json
{
  "domain_metadata": {
    "source_title": "감정평가 실무기준",
    "law_name": "감정평가 및 감정평가사에 관한 법률",
    "notice_name": "국토교통부 고시 제2024-000호",
    "article_number": "제3조",
    "article_title": "정의",
    "revision_date": "2024-01-01",
    "effective_date": "2024-02-01",
    "created_date": null,
    "collected_at": "2026-05-17T00:00:00Z",
    "appraisal_base_date": null,
    "source_url": "https://example.official/source",
    "source_authority": "국토교통부",
    "source_authority_type": "government_ministry",
    "jurisdiction": "KR",
    "version_label": "unknown",
    "manual_supplementation_status": "not_reviewed"
  }
}
```

## Field Definitions

| Field | Required for official ingestion | Missing value | Meaning |
|---|---:|---|---|
| `source_title` | yes | `"unknown"` | 자료명/표시명. 법령, 고시, 공고, 지침 등의 원문 제목. |
| `law_name` | conditional | `null` | 법령 또는 행정규칙 이름. 고시/공고만 있으면 `null` 가능. |
| `notice_name` | conditional | `null` | 고시명, 공고명, 예규명, 훈령명 등 법령 외 공식 문서명. |
| `article_number` | conditional | `null` | 조항 번호. 조문 단위 source/chunk에서만 필요. |
| `article_title` | optional | `null` | 조항 제목. source가 제공하지 않으면 생성하지 않는다. |
| `revision_date` | conditional | `null` | 개정일. 원문 또는 API metadata가 제공한 개정 기준 날짜. |
| `effective_date` | conditional | `null` | 시행일. 특정 version이 효력을 갖는 날짜. |
| `created_date` | optional | `null` | 작성일/공고 작성일. 개정일 또는 수집일과 다르다. |
| `collected_at` | yes | ISO timestamp | 시스템이 source를 수집한 수집일/수집시각. source 원문 날짜가 아니다. |
| `appraisal_base_date` | optional | `null` | 평가기준일. 감정평가 업무 문맥에서 판단 기준이 되는 날짜. |
| `source_url` | conditional | `"unknown"` | 원문 또는 API canonical URL. 없으면 추정 URL을 만들지 않는다. |
| `source_authority` | yes | `"unknown"` | source를 발행/운영한 기관명. 예: 국토교통부, 국가법령정보센터. |
| `source_authority_type` | optional | `"unknown"` | 기관 유형. 예: government_ministry, public_agency, court, municipality. |
| `jurisdiction` | optional | `"KR"` | 관할권/국가 코드. 국내 MVP 기본값은 `KR`. |
| `version_label` | optional | `"unknown"` | source가 제공하는 버전, 고시번호, 시행 버전 라벨. |
| `manual_supplementation_status` | optional | `"not_reviewed"` | 사람이 metadata를 검토/보완했는지 표시. |

## Date Semantics

| Date field | Korean meaning | Do not confuse with | Rule |
|---|---|---|---|
| `created_date` | 작성일 | 수집일, 시행일 | 문서 또는 고시가 작성/공고된 날짜. source가 제공할 때만 사용. |
| `collected_at` | 수집일 | 작성일, 개정일 | 시스템이 데이터를 가져온 날짜/시간. loader가 항상 기록한다. |
| `revision_date` | 개정일 | 시행일 | 법령/규정 내용이 개정된 날짜. source metadata 기반만 허용. |
| `effective_date` | 시행일 | 개정일 | 해당 version이 효력을 갖기 시작하는 날짜. |
| `appraisal_base_date` | 평가기준일 | 수집일, 작성일 | 감정평가 판단 기준일. 원문/사용자 업무문서가 제공할 때만 사용. |

## Manual Supplementation

Manual supplementation can improve official metadata when public sources are incomplete or hard to parse.

Recommended manual workflow:

1. Export candidate documents with `source_id`, `source_url`, current `domain_metadata`, and missing fields.
2. Human reviewer fills only verifiable values from the official source.
3. Store reviewer, review timestamp, and evidence note in metadata, e.g. `manual_supplementation_status="reviewed"`.
4. Keep original raw/extracted metadata alongside reviewed values when possible.
5. Never use manual supplementation to infer legal conclusions or appraisal appropriateness.

Manual fields that are reasonable to supplement:

- `source_title`
- `source_authority`
- `notice_name` / `law_name`
- `article_number` when visible in source text
- `source_url` copied from the official page

Manual fields that require caution:

- `revision_date` and `effective_date`; reviewer must verify labels in the source.
- `appraisal_base_date`; only use if the task/source explicitly states it.

## Agent Limitation

Current agent limitation:

- Cannot guarantee live official source availability without source access/API credentials.
- Cannot reliably parse HWP/PDF/OCR-heavy attachments without dedicated parsers and quality checks.
- Cannot certify legal validity; it can only preserve source metadata and display uncertainty.
- Cannot infer missing official metadata from nearby text unless a loader rule explicitly extracts it and tests cover it.

## Prerequisite Work That Makes Automation Safer

Prerequisite work before reliable official ingestion:

1. Pick a first source with stable access and machine-readable XML/JSON/HTML.
2. Store API credentials/app ids in environment settings, not code.
3. Add source-specific parser tests with real or recorded fixtures.
4. Define dedupe/update policy for repeated official source collection.
5. Add validation that official answers only cite chunks with `data_mode=official` and real `source_url`/`source_authority`.
6. Add manual review queue/export if a source has incomplete but human-verifiable metadata.

## Loader Mapping Guidance

- Document-level metadata should include the full `domain_metadata` object.
- Chunk metadata should inherit relevant fields needed for citation: `source_title`, `law_name`, `notice_name`, `article_number`, `effective_date`, `source_url`, and `source_authority`.
- If fields differ within a document, split chunks or sections so each chunk has accurate metadata.
- Do not promote `domain_metadata` fields to DB columns until query/filter requirements stabilize.
