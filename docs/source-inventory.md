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
| `official-law-open-api` | 국가법령정보 공동활용 OPEN API | `deferred` | `official` | `XML/HTML` | `open_api` | `https://open.law.go.kr/LSO/openApi/guideList.do` | `API key/app id likely required` | `high` | 법령/행정규칙 후보. `data_mode` = `official`. 다음 작업: XML parser, law metadata mapper, API credential handling. next_loader_work=`xml_api_loader`. |
| `official-molit-appraisal-standards` | 국토교통부 감정평가 실무기준 고시 | `deferred` | `official` | `HTML/PDF/HWP possible` | `web_page` | `https://www.molit.go.kr/USR/I0204/m_45/dtl.jsp?idx=17932` | `unknown` | `medium` | 감정평가 실무기준 공식 고시 후보. 현재 HTML/PDF/HWP parser 부재로 ingest 금지. next_loader_work=`html_notice_parser`, `pdf_or_hwp_attachment_strategy`. |
| `official-molit-open-api-guide` | 국토교통부 Open API 가이드라인 | `deferred` | `official` | `API/JSON/XML varies` | `open_api_catalog` | `https://www.molit.go.kr/USR/WPGE0201/m_23746/DTL.jsp` | `API key likely required` | `medium` | 국토교통부 API 사용 방식 확인용 source. 실제 도메인 데이터 source와 분리. next_loader_work=`api_catalog_research`. |
| `official-public-land-price-api` | 공공데이터포털 국토교통부 개별공시지가정보 | `deferred` | `official` | `JSON/XML` | `open_api` | `https://www.data.go.kr/data/15124014/openapi.do?recommendDataYn=Y` | `API key likely required` | `medium` | 공시지가/토지 가격 데이터 후보. 법령 텍스트 RAG와 별도 구조화 데이터 처리 필요. next_loader_work=`json_xml_api_loader`, `structured_price_schema`. |
| `official-law-notices` | Official 법령/고시 source candidates umbrella | `deferred` | `official` | `html/xml/json/pdf` | `api_or_web` | `TBD` | `unknown` | `unknown` | `low` | 구체 source가 위 항목으로 분리됨. 신규 공식 source 발견 시 별도 row 추가. |
| `hwp-documents` | HWP documents | `unsupported` | `unknown` | `HWP` | `local_file` | `unknown` | `unknown` | `false` | `low` | MVP loader 범위 밖. unsupported로 명시해야 하며 silent ingestion 금지. DOCX/PDF/OCR도 별도 parser 도입 전까지 deferred 또는 unsupported로 처리한다. |

## 공식/공개 source 조사 메모

- 국가법령정보 공동활용 OPEN API는 법령/행정규칙 계열의 우선 후보이며, 검색 결과 기준 OPEN API 활용 가이드가 제공된다. XML/HTML 응답과 인증 식별자 처리를 전제로 별도 loader가 필요하다.
- 국토교통부 고시 페이지는 감정평가 실무기준 같은 도메인 핵심 자료의 공식 위치 후보지만, HTML 본문과 PDF/HWP 첨부가 섞일 수 있어 MVP markdown/txt loader로 처리하지 않는다.
- 공공데이터포털 개별공시지가정보는 JSON/XML API로 구조화 부동산 가격 데이터를 제공하는 후보지만, 텍스트 법령 RAG와 다른 schema 및 API key 관리가 필요하다.
- PDF, DOCX, HWP, OCR 필요 source는 별도 parser/추출 품질 평가 전까지 `deferred` 또는 `unsupported`로 둔다.
- official source는 조사 완료 상태여도 ingestion 완료로 표시하지 않는다. `data_mode` = `official` source는 실제 API/scraping 구현과 검증이 끝난 뒤에만 `ingested`로 변경한다.

## 다음 loader/parser 작업 후보

| priority | next_loader_work | needed for | notes |
|---|---|---|---|
| high | `xml_api_loader` | 국가법령정보 OPEN API | API key/app id 설정, XML metadata mapping, rate/error handling 필요 |
| medium | `html_notice_parser` | 국토교통부 고시 페이지 | 본문/첨부 구분, 고시번호/시행일 metadata 추출 필요 |
| medium | `json_xml_api_loader` | 공공데이터포털 공시지가 API | 구조화 schema와 텍스트 RAG chunking 분리 필요 |
| low | `pdf_docx_hwp_ocr_pipeline` | 첨부 문서 | parser 품질, 저작권/이용조건, OCR 비용 검토 필요 |

## 운영 규칙

1. `unsupported` 또는 `deferred` source는 성공적으로 ingested 된 것처럼 표시하지 않는다.
2. ingestion 결과는 source별 status, 처리 document 수, chunk 수, 실패 사유를 기록해야 한다.
3. official source가 실제로 ingested 되기 전까지 시스템은 official knowledge base가 있는 것처럼 응답하지 않는다.
4. user_provided data는 retention/deletion/external tracing 정책 전까지 sample data와 섞지 않는다.
5. sample/local data와 official data는 `data_mode`로 분리하며, official source는 실제 수집 전까지 검색/답변 근거로 사용하지 않는다.
