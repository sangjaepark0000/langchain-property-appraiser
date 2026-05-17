# Canonical Document Schema

## 목적

Canonical document schema는 loader/parser가 서로 다른 입력 형식을 공통 구조로 변환하기 위한 기준이다. 이후 chunking, embedding, retrieval, citation, answer generation에서 source metadata와 lineage를 보존하는 것이 핵심이다.

## Data Modes

| data_mode | 의미 | 응답/처리 규칙 |
|---|---|---|
| `sample` | 테스트/학습용 sample data | official 또는 user-provided 실제 자료처럼 표현하지 않는다. |
| `official` | 공식/공개 source에서 수집한 자료 | source_url, 수집일, 가능한 경우 시행일/개정일 등 provenance를 보존한다. |
| `user_provided` | 사용자가 제공한 업무 문서 | 민감 원문 tracing/logging 정책을 따른다. sample/official과 섞지 않는다. |
| `unknown` | 출처 또는 mode가 아직 확정되지 않음 | 가능한 빨리 명확한 mode로 보정한다. |

## Canonical Document Fields

| Field | Required | Description |
|---|---:|---|
| `document_id` | yes | 내부 document 식별자 |
| `source_id` | yes | source inventory의 `source_id` |
| `source_path` | conditional | local file path 또는 object path |
| `source_url` | conditional | official/web source URL |
| `source_name` | yes | 표시용 source 이름 |
| `source_type` | yes | markdown, txt, html, pdf 등 |
| `data_mode` | yes | `sample`, `official`, `user_provided`, `unknown` |
| `title` | no | 문서 제목 |
| `text` | yes | normalized text content |
| `metadata` | yes | source-specific metadata dictionary |
| `ingested_at` | later | ingestion timestamp |
| `status` | yes | loaded, skipped, unsupported, failed 등 |

## Canonical Chunk Fields

| Field | Required | Description |
|---|---:|---|
| `chunk_id` | yes | 내부 chunk 식별자 |
| `document_id` | yes | parent document id |
| `chunk_index` | yes | 문서 내 chunk 순서 |
| `text` | yes | chunk text |
| `metadata` | yes | document metadata에서 상속/보강된 metadata |
| `source_path` | conditional | citation에 사용할 local path |
| `source_url` | conditional | citation에 사용할 URL |
| `source_name` | yes | citation 표시명 |
| `data_mode` | yes | parent document의 data mode |
| `lineage` | yes | original source → document → chunk 추적 정보 |

## Metadata Guidelines

공통 metadata 예시:

```json
{
  "source_id": "sample-local-markdown",
  "source_name": "Local sample markdown/txt files",
  "source_path": "sample_data/example.md",
  "source_url": null,
  "source_type": "markdown",
  "data_mode": "sample",
  "created_at": null,
  "collected_at": null,
  "revision_date": null,
  "effective_date": null
}
```

## Lineage and Citation Rules

1. Every chunk must preserve enough lineage to trace back to the original document/source.
2. Citation must be generated only from actual retrieved chunk metadata.
3. Missing official metadata must use `unknown`/null; do not fabricate URL, law name, revision date, effective date, or appraisal/legal conclusions.
4. Unsupported file formats must produce explicit unsupported/skipped status, not silent success.
5. `data_mode` must travel from source inventory → document → chunk → retrieval result → answer/API response.

## Out of Scope for This Draft

- Final SQLAlchemy table definitions
- Loader/parser implementation
- Embedding/vector schema details
- Official legal/regulatory source ingestion
