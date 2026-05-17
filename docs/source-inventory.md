# Source Inventory

## 목적

이 문서는 RAG 지식베이스 후보 source의 출처, 접근 방식, 제공 형식, data mode, 처리 상태를 추적하기 위한 초기 운영 문서다. 목표는 지원 가능한 source와 아직 지원하지 않는 source를 명확히 구분하고, unsupported/deferred source가 조용히 ingested 된 것처럼 처리되는 일을 방지하는 것이다.

## Source Status

| Status | 의미 | 처리 규칙 |
|---|---|---|
| `supported` | 현재 loader/parser가 처리할 수 있는 source | ingestion 대상이 될 수 있다. |
| `unsupported` | 현재 형식/접근 방식이 지원되지 않는 source | silent success 금지. ingestion 결과에서 명시적으로 제외/오류 처리한다. |
| `deferred` | 후속 story 또는 도메인 확장에서 검토할 source | 실제 지식베이스에 들어간 것처럼 표시하지 않는다. |
| `ingested` | 실제 ingestion이 완료된 source | ingestion run id, 수집일, document/chunk 수를 기록한다. |
| `failed` | ingestion 시도 중 실패한 source | 실패 사유와 재시도 조건을 기록한다. |

## Expected Fields

| Field | Description | Example |
|---|---|---|
| `source_id` | source 식별자 | `sample-local-policy` |
| `name` | 사람이 읽는 이름 | `Sample Local Policy Notes` |
| `status` | `supported`, `unsupported`, `deferred`, `ingested`, `failed` | `supported` |
| `data_mode` | `sample`, `official`, `user_provided`, `unknown` | `sample` |
| `source_type` | 파일/API/웹/PDF 등 | `markdown` |
| `access_method` | local path, API, URL, manual upload 등 | `local_file` |
| `source_url` | 원본 URL, 없으면 blank/unknown | `unknown` |
| `source_path` | local file/path, 없으면 blank | `sample_data/example.md` |
| `requires_auth` | 인증/API key 필요 여부 | `false` |
| `priority` | 처리 우선순위 | `high`, `medium`, `low` |
| `last_checked_at` | source 상태 확인일 | `2026-05-17` |
| `notes` | 제약, 실패 사유, 후속 작업 | `MVP sample only` |

## Initial Inventory

| source_id | name | status | data_mode | source_type | access_method | source_url | source_path | requires_auth | priority | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| `sample-local-markdown` | Local sample markdown/txt files | `supported` | `sample` | `markdown/txt` | `local_file` | `unknown` | `sample_data/` | `false` | `high` | 후속 ingestion story에서 smoke data로 사용한다. |
| `user-uploaded-business-docs` | User-provided appraisal/business documents | `deferred` | `user_provided` | `pdf/docx/hwp/unknown` | `manual_upload` | `unknown` | `unknown` | `false` | `medium` | retention/deletion/tracing 정책 전까지 실제 처리하지 않는다. |
| `official-law-notices` | Official 법령/고시 source candidates | `deferred` | `official` | `html/xml/json/pdf` | `api_or_web` | `TBD` | `unknown` | `unknown` | `medium` | Epic 6에서 source 조사 후 확정한다. |
| `hwp-documents` | HWP documents | `unsupported` | `unknown` | `hwp` | `local_file` | `unknown` | `unknown` | `false` | `low` | MVP loader 범위 밖. unsupported로 명시해야 하며 silent ingestion 금지. |

## 운영 규칙

1. `unsupported` 또는 `deferred` source는 성공적으로 ingested 된 것처럼 표시하지 않는다.
2. ingestion 결과는 source별 status, 처리 document 수, chunk 수, 실패 사유를 기록해야 한다.
3. official source가 실제로 ingested 되기 전까지 시스템은 official knowledge base가 있는 것처럼 응답하지 않는다.
4. user_provided data는 retention/deletion/external tracing 정책 전까지 sample data와 섞지 않는다.
