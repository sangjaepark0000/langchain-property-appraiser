---
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories", "step-04-final-validation"]
inputDocuments:
  - "_bmad-output/planning-artifacts/prd.md"
  - "_bmad-output/planning-artifacts/architecture.md"
---

# langchain-property-appraiser - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for langchain-property-appraiser, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: 개발자/운영자는 RAG 지식베이스 후보 소스의 출처, 접근 방식, 제공 형식, 필수 메타데이터, 우선순위, 처리 상태를 관리할 수 있다.

FR2: 시스템은 지식베이스 자료, 사용자 업무 문서, 테스트/샘플 자료를 구분하고 현재 데이터 모드를 표시할 수 있다.

FR3: 시스템은 지원 가능한 소스와 미지원/보류 소스를 구분하며, 미지원 소스를 조용히 누락하지 않고 상태로 기록할 수 있다.

FR4: 개발자는 지원 문서 형식을 로딩하고 공통 document schema로 변환할 수 있다.

FR5: 시스템은 문서를 검색 가능한 단위로 분할하고 메타데이터와 원본 source lineage를 유지한 채 지식베이스에 적재할 수 있다.

FR6: 사용자는 자연어 질문으로 지식베이스를 검색하고 근거 기반 답변을 받을 수 있다.

FR7: 시스템은 답변에 참조 문서 조각, 출처, 메타데이터, 데이터 모드 정보를 포함할 수 있다.

FR8: 사용자는 멀티턴 대화를 통해 후속 질문, 문맥 기반 요청, 필터 조정, 검토 이력 기록, 참고용 초안 요청을 자연어로 수행할 수 있다.

FR9: 시스템은 CRAG 흐름을 통해 검색 결과의 충분성을 평가하고, 필요한 경우 질의 보정·재검색·근거 부족 응답을 수행할 수 있다.

FR10: 시스템은 대화 메시지, 참조 문서 조각, 질의 보정 이력, 근거 부족 원인을 추적할 수 있다.

FR11: 사용자는 웹 화면에서 버튼 중심 워크플로우가 아닌 자연어 멀티턴 RAG 챗봇을 사용할 수 있다.

FR12: 시스템은 웹 화면에서 메시지, 출처/근거, 데이터 모드, 로딩, 오류, 근거 부족 상태를 표시할 수 있다.

FR13: 시스템은 법률 위반 여부, 감정평가 적정성, 법적 책임 가능성을 단정하지 않고 참고용 검토 보조로 응답할 수 있다.

FR14: 시스템은 제공되지 않은 실제 업무 문서나 공식 법령 데이터를 임의 생성해 실제 자료처럼 가장하지 않는다.

FR15: 시스템은 법령/고시 도메인 확장을 위해 법령명, 조항, 개정일, 시행일, 수집일, 출처 URL, 최근 X기간 필터, 알림 레벨을 지원할 수 있다.

FR16: 개발자는 웹 UI 없이 RAG Core smoke test를 실행할 수 있다.

FR17: 개발자는 RAG/CRAG/LangGraph 실행 흐름과 주요 중간 결과를 로컬 로그 또는 선택적 tracing 도구로 확인할 수 있다.

### NonFunctional Requirements

NFR1: 소규모 문서 세트 기준 ingestion과 RAG 질의는 개발 중 반복 실행 가능한 수준으로 완료되어야 한다.

NFR2: 장시간 실행되는 ingestion, retrieval, answer generation 작업은 사용자 또는 개발자가 멈춤과 진행 중을 구분할 수 있는 상태를 제공해야 한다.

NFR3: API key, LangSmith key, LLM provider key 등 비밀값은 코드나 문서 본문에 하드코딩하지 않아야 한다.

NFR4: 민감한 사용자 업무 문서 원문은 기본적으로 외부 tracing 로그에 남기지 않아야 한다.

NFR5: 사용자 업무 문서 원문을 외부 LLM 또는 tracing 도구에 전송하는 경우, 전송 여부와 범위가 설정으로 통제 가능해야 한다.

NFR6: 지원하지 않는 문서 형식이나 데이터 소스는 조용히 누락하지 않고 unsupported/deferred 또는 명확한 오류 상태로 기록되어야 한다.

NFR7: 검색 근거가 부족한 경우 시스템은 단정 답변 대신 근거 부족 상태로 응답해야 한다.

NFR8: 공식 데이터가 없는 경우 시스템은 공식 법령 검토 결과처럼 응답하지 않아야 한다.

NFR9: LangSmith 또는 외부 tracing 설정이 없어도 RAG Core와 웹 챗봇은 정상 동작해야 한다.

NFR10: 개발자는 ingestion, retrieval, grading, rewrite, answer generation의 주요 실행 단계와 실패 원인을 확인할 수 있어야 한다.

NFR11: LangSmith가 설정된 경우 LangGraph node transition과 RAG/CRAG 중간 결과를 추적할 수 있어야 하며, 비활성화된 경우에도 로컬 로그로 주요 실행 상태를 확인할 수 있어야 한다.

NFR12: loader/parser는 새로운 문서 형식을 추가해도 기존 RAG 흐름을 크게 변경하지 않도록 공통 schema 기반으로 확장 가능해야 한다.

NFR13: 지식베이스 자료와 사용자 업무 문서는 데이터 모델과 보관 정책에서 분리되어야 한다.

NFR14: RAG Core, Web Chat, Domain Layer는 단계적으로 교체 또는 확장 가능하도록 결합도를 낮게 유지해야 한다.

NFR15: 웹 채팅 UI는 키보드 입력, 읽기 쉬운 메시지 구조, 명확한 로딩/오류/근거 부족 상태 표시를 제공해야 한다.

### Additional Requirements

- Starter Template: Backend-first FastAPI 구조를 우선 사용하고, RAG Core 검증 이후 SvelteKit frontend를 추가한다. 첫 구현 story는 이 초기화 접근을 반영해야 한다.
- Backend 초기화는 `backend/` 디렉터리, Python virtual environment, FastAPI, Uvicorn, LangChain, LangGraph 설치를 기준으로 한다.
- Frontend 초기화는 후속 phase에서 `npx sv create frontend`를 사용한다.
- 프로젝트 구조는 `backend/app/api`, `core`, `db`, `models`, `schemas`, `ingestion`, `rag`, `graph`, `services`, `backend/alembic`, `backend/scripts`, `backend/tests`, `docs`, `sample_data`, 후속 `frontend` 경계를 따른다.
- V1 데이터 저장소는 PostgreSQL + pgvector를 사용하고, local development DB는 Docker Compose로 실행한다.
- SQLAlchemy + Alembic으로 schema modeling과 migration을 관리한다.
- `documents`, `chunks`, `conversations`, `messages`, `retrieval_traces`, `source_inventory` 개념 모델을 분리해 구현한다.
- LangChain vector store 통합은 사용할 수 있으나 core schema의 소유권은 애플리케이션 SQLAlchemy model에 둔다.
- 설정 관리는 `.env`, environment variables, `pydantic-settings`를 사용하며 secret은 하드코딩하지 않는다.
- V1은 인증, 사용자 계정, authorization, multi-user isolation을 포함하지 않는다.
- REST API 초기 surface는 `POST /ingest`, `POST /chat`, `GET /conversations/{id}`와 선택적 local-only retrieval trace debug endpoint다.
- Chat API 응답은 `conversation_id`, `message_id`, `answer`, `citations`, `data_mode`, `insufficient_evidence`, 가능한 경우 `retrieval_trace_id`를 일관되게 포함한다.
- API 오류는 `{ "error": { "code", "message", "details" } }` 형태를 사용한다.
- FastAPI route handler는 얇게 유지하고 business logic은 `services/`, `rag/`, `graph/`로 분리한다.
- SQLAlchemy models와 Pydantic schemas는 별도 파일/계층으로 유지한다.
- `graph/`는 LangGraph orchestration만 담당하고 retrieval, embedding, answer logic은 `rag/` 재사용 함수에 둔다.
- `data_mode`는 `sample`, `official`, `user_provided`, `unknown` 등 명시적 값으로 표시한다.
- Insufficient evidence는 server error가 아니라 정상 응답 상태로 처리한다.
- Unsupported document format은 silent skip이 아니라 명시적 오류 또는 unsupported/deferred 상태로 처리한다.
- Source metadata는 ingestion, retrieval, answer generation, API response 전체 경로에서 보존한다.
- Retrieval trace는 original query, rewritten query, retrieved chunk ids, grading/relevance result, insufficient evidence reason을 디버깅 가능하도록 캡처한다.
- LangSmith는 선택 사항이며, 설정이 없으면 local logs만으로 정상 동작해야 한다.
- 민감한 사용자 업무 문서 원문은 기본적으로 trace에 남기지 않는다.
- 첫 구현 우선순위는 backend skeleton, `.env.example`, PostgreSQL + pgvector Docker Compose, `pydantic-settings`, SQLAlchemy/Alembic setup, 초기 model/migration placeholder다.
- Backend Python version은 구현 전 명시해야 하며, Python 3.12 또는 3.13이 package compatibility 측면에서 더 안전할 수 있다.
- 실제 embedding provider key가 없어도 첫 story가 막히지 않도록 mock/skip 동작을 허용해야 한다.
- `sample_data/`를 먼저 사용하고, 공식 법령/고시 데이터 수집은 후속 도메인 확장으로 둔다.

### UX Design Requirements

UX Design 문서가 발견되지 않았으므로 별도 UX-DR 요구사항은 추출하지 않았다. PRD/Architecture에서 추출된 웹 채팅 관련 UX 요구사항은 FR11, FR12, NFR15 및 Additional Requirements의 frontend/API 응답 규칙에 반영되어 있다.

### FR Coverage Map

FR1: Epic 1, Epic 2, Epic 6 - source inventory와 지식베이스 후보 소스 관리
FR2: Epic 1, Epic 2, Epic 3, Epic 6 - 데이터 모드 구분과 표시
FR3: Epic 1, Epic 2, Epic 6 - 지원/미지원 소스 상태 기록
FR4: Epic 2 - 지원 문서 형식 로딩과 공통 schema 변환
FR5: Epic 2 - chunking, metadata, source lineage, vector store 적재
FR6: Epic 3 - 자연어 질문 기반 RAG 답변
FR7: Epic 3, Epic 5 - 답변에 참조 chunk, 출처, 메타데이터, 데이터 모드 포함
FR8: Epic 4, Epic 5 - 멀티턴 대화와 후속 질문
FR9: Epic 4 - CRAG 검색 평가, query rewrite, re-retrieval, insufficient evidence
FR10: Epic 1, Epic 4 - 메시지, 참조 chunk, query rewrite, 근거 부족 원인 trace
FR11: Epic 5 - 웹 자연어 멀티턴 챗봇
FR12: Epic 5 - 웹 UI 상태 표시
FR13: Epic 3, Epic 4, Epic 5, Epic 6 - 법률/감정평가 판단 단정 금지
FR14: Epic 3, Epic 4, Epic 5, Epic 6 - 제공되지 않은 공식/업무 데이터 임의 생성 금지
FR15: Epic 6 - 법령/고시 도메인 확장 메타데이터와 필터/알림 레벨
FR16: Epic 1, Epic 2, Epic 3 - 웹 UI 없는 RAG Core smoke test
FR17: Epic 1, Epic 2, Epic 3, Epic 4 - 로그/tracing 기반 실행 흐름 확인

## Epic List

### Epic 1: Local RAG Development Workspace
PSJ는 local-first 환경에서 FastAPI backend, PostgreSQL/pgvector, 설정, migration, 기본 프로젝트 구조를 갖춘 실행 가능한 RAG 개발 작업공간을 만들 수 있다.

**FRs covered:** FR1, FR2, FR3, FR10, FR16, FR17

### Epic 2: Document Ingestion and Searchable Knowledge Base
PSJ는 markdown/txt 문서를 공통 schema로 로딩하고, chunking, metadata, source lineage, embedding/vector 저장을 통해 검색 가능한 지식베이스를 만들 수 있다.

**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR16, FR17

### Epic 3: Evidence-Based RAG Answering and Smoke Tests
사용자는 자연어 질문으로 지식베이스를 검색하고, 출처·근거·메타데이터·데이터 모드가 포함된 답변을 CLI 또는 API로 받을 수 있다.

**FRs covered:** FR2, FR6, FR7, FR13, FR14, FR16, FR17

### Epic 4: Multi-Turn CRAG Conversation Runtime
사용자는 멀티턴 대화에서 이전 문맥을 유지하며 후속 질문을 할 수 있고, 시스템은 검색 결과를 평가해 query rewrite, re-retrieval, insufficient evidence 응답, retrieval trace를 제공할 수 있다.

**FRs covered:** FR8, FR9, FR10, FR13, FR14, FR17

### Epic 5: Svelte Web Chat Experience
사용자는 웹 화면에서 자연어 멀티턴 RAG 챗봇을 사용할 수 있고, 메시지, 출처/근거, 데이터 모드, 로딩, 오류, 근거 부족 상태를 확인할 수 있다.

**FRs covered:** FR7, FR8, FR11, FR12, FR13, FR14

### Epic 6: Domain Extension Readiness (Post-MVP)
운영자/개발자는 법령·고시 도메인 확장을 위해 공식/공개 소스 후보를 source inventory로 관리하고, 법령명, 조항, 개정일, 시행일, 수집일, 출처 URL, 최근 X기간 필터, 알림 레벨 같은 도메인 메타데이터를 수용할 준비를 할 수 있다.

**FRs covered:** FR1, FR2, FR3, FR13, FR14, FR15

## Epic 1: Local RAG Development Workspace

PSJ는 local-first 환경에서 FastAPI backend, PostgreSQL/pgvector, 설정, migration, 기본 프로젝트 구조를 갖춘 실행 가능한 RAG 개발 작업공간을 만들 수 있다.

### Story 1.1: 백엔드 프로젝트 기본 골격 만들기

As a 개발자,
I want FastAPI 기반 백엔드 프로젝트 구조를 만들고 싶다,
So that 이후 RAG 기능을 안정적인 구조 위에서 구현할 수 있다.

**Acceptance Criteria:**

**Given** 깨끗한 프로젝트 저장소가 있다
**When** 백엔드 작업공간을 초기화한다
**Then** `backend/pyproject.toml`, `backend/app/main.py`, 승인된 backend 폴더 구조가 존재한다
**And** FastAPI, LangChain, LangGraph와 호환되는 Python 버전이 문서화되어 있다.

**Given** 백엔드 의존성이 설치되어 있다
**When** FastAPI 앱을 로컬에서 실행한다
**Then** 기본 health endpoint가 성공적으로 응답한다
**And** LLM, embedding, LangSmith, database credentials 없이도 앱이 시작된다.

**Given** 새 개발자가 저장소를 연다
**When** setup 문서를 읽는다
**Then** backend 환경 생성, 의존성 설치, local API 실행 방법을 확인할 수 있다.

### Story 1.2: 환경변수와 secret 관리 만들기

As a 개발자,
I want 애플리케이션 설정을 환경변수와 `.env` 파일에서 로드하고 싶다,
So that secret과 provider 설정을 코드에 하드코딩하지 않고 관리할 수 있다.

**Acceptance Criteria:**

**Given** 백엔드 애플리케이션이 시작된다
**When** 설정이 로드된다
**Then** `pydantic-settings` 또는 동등한 typed settings module을 통해 설정을 읽는다
**And** optional provider key가 없어도 local startup이 실패하지 않는다.

**Given** 저장소에 설정 예시가 있다
**When** `.env.example`을 확인한다
**Then** database URL, LLM provider 설정, embedding provider 설정, LangSmith 설정, safe default가 문서화되어 있다
**And** 실제 secret 값은 커밋되어 있지 않다.

**Given** LangSmith 설정이 없다
**When** 애플리케이션이 시작된다
**Then** tracing은 안전하게 비활성화된다
**And** local logging은 계속 사용할 수 있다.

### Story 1.3: PostgreSQL + pgvector 로컬 DB 준비하기

As a 개발자,
I want Docker Compose로 PostgreSQL과 pgvector 로컬 데이터베이스를 실행하고 싶다,
So that RAG metadata와 vector-ready storage를 일관된 local 환경에서 개발할 수 있다.

**Acceptance Criteria:**

**Given** 로컬에 Docker가 사용 가능하다
**When** 문서화된 compose 명령을 실행한다
**Then** PostgreSQL이 pgvector 지원과 함께 시작된다
**And** 연결 정보는 `.env.example`에 문서화된 값과 일치한다.

**Given** database container가 실행 중이다
**When** backend가 database connectivity를 확인한다
**Then** 설정된 database URL로 연결할 수 있다
**And** 연결 실패 시 명확한 local error message를 제공한다.

**Given** 개발자가 local state를 reset해야 한다
**When** 문서화된 절차를 따른다
**Then** local database를 중지, 제거, 재생성하는 방법을 명확히 알 수 있다.

### Story 1.4: SQLAlchemy와 Alembic migration 기반 만들기

As a 개발자,
I want SQLAlchemy와 Alembic을 local database에 맞게 설정하고 싶다,
So that future RAG entities를 controlled migration으로 추가할 수 있다.

**Acceptance Criteria:**

**Given** 백엔드 database configuration이 있다
**When** Alembic을 초기화한다
**Then** migration configuration이 `backend/alembic` 아래에 존재한다
**And** migration은 애플리케이션과 동일한 database settings를 사용한다.

**Given** local database가 실행 중이다
**When** initial migration command를 실행한다
**Then** migration이 성공적으로 완료된다
**And** database에 현재 migration version이 기록된다.

**Given** 아직 domain table이 필요하지 않다
**When** baseline migration을 만든다
**Then** 불필요한 future table을 미리 만들지 않는다
**And** 이후 story에서 필요한 entity를 추가할 준비만 갖춘다.

### Story 1.5: Source inventory와 canonical schema 문서 초안 만들기

As a 개발자/운영자,
I want source inventory와 canonical document schema의 초기 문서 초안을 만들고 싶다,
So that supported, unsupported, sample, official, user-provided data를 처음부터 구분해 추적할 수 있다.

**Acceptance Criteria:**

**Given** repository documentation folder가 있다
**When** 문서 초안을 추가한다
**Then** `docs/source-inventory.md`와 `docs/canonical-document-schema.md`가 존재한다
**And** 각 문서는 목적과 예상 필드를 설명한다.

**Given** 아직 지원하지 않는 source가 있다
**When** source inventory에 기록한다
**Then** 해당 source를 unsupported 또는 deferred로 표시할 수 있다
**And** unsupported source가 조용히 ingested된 것처럼 처리되지 않는다.

**Given** data mode가 이후 RAG 답변에 중요하다
**When** canonical schema 문서 초안을 검토한다
**Then** `sample`, `official`, `user_provided`, `unknown` 같은 data mode 개념이 포함되어 있다.

### Story 1.6: 로컬 로그와 개발자 smoke command 만들기

As a 개발자,
I want local logging과 최소 smoke command를 갖추고 싶다,
So that 웹 UI나 외부 AI provider credentials 없이도 workspace 상태를 검증할 수 있다.

**Acceptance Criteria:**

**Given** 백엔드 앱이 로컬에 설치되어 있다
**When** health check 또는 smoke command를 실행한다
**Then** backend가 시작되고 응답할 수 있음을 확인한다
**And** LLM 또는 embedding provider key가 필요하지 않다.

**Given** 앱이 시작되거나 실패한다
**When** local logs를 확인한다
**Then** startup, configuration, database connectivity, optional tracing disabled 상태를 확인할 수 있다
**And** 민감한 secret 값은 출력되지 않는다.

**Given** future dev agent가 workspace를 검증해야 한다
**When** 문서화된 smoke test 절차를 따른다
**Then** ingestion 구현 전에 Epic 1 readiness를 확인할 수 있다.

## Epic 2: Document Ingestion and Searchable Knowledge Base

PSJ는 markdown/txt 문서를 공통 schema로 로딩하고, chunking, metadata, source lineage, embedding/vector 저장을 통해 검색 가능한 지식베이스를 만들 수 있다.

### Story 2.1: Document와 Chunk 저장 모델 만들기

As a 개발자,
I want 문서와 chunk를 저장할 최소 DB 모델을 만들고 싶다,
So that ingestion 결과를 source metadata와 함께 추적 가능한 형태로 저장할 수 있다.

**Acceptance Criteria:**

**Given** SQLAlchemy/Alembic 기반이 준비되어 있다
**When** document와 chunk 모델을 추가한다
**Then** `documents`와 `chunks` table이 migration으로 생성된다
**And** 각 chunk는 원본 document와 연결된다.

**Given** 문서 metadata가 필요하다
**When** document record를 저장한다
**Then** source path/name, source type, data mode, ingestion status, created timestamp를 저장할 수 있다
**And** data mode는 `sample`, `official`, `user_provided`, `unknown` 중 하나로 표현된다.

**Given** chunk metadata가 필요하다
**When** chunk record를 저장한다
**Then** chunk text, chunk index, source lineage, token/character range 또는 이에 준하는 위치 정보를 저장할 수 있다
**And** 원본 문서와의 추적 관계가 유지된다.

### Story 2.2: Markdown/TXT loader와 canonical document 변환 만들기

As a 개발자,
I want markdown/txt 파일을 로딩해 canonical document schema로 변환하고 싶다,
So that 이후 chunking, embedding, retrieval이 동일한 입력 형식을 사용할 수 있다.

**Acceptance Criteria:**

**Given** markdown 또는 txt 파일이 있다
**When** loader를 실행한다
**Then** 파일 내용과 기본 metadata가 canonical document object로 변환된다
**And** source path, file name, file type, data mode가 포함된다.

**Given** 지원하지 않는 파일 형식이 입력된다
**When** loader를 실행한다
**Then** unsupported file type 오류가 명확하게 반환된다
**And** 해당 파일은 조용히 누락되거나 성공 처리되지 않는다.

**Given** loader/parser 확장이 필요하다
**When** 코드를 검토한다
**Then** 새로운 file type loader를 추가할 수 있는 구조가 분리되어 있다
**And** 기존 markdown/txt loader를 크게 변경하지 않아도 된다.

### Story 2.3: Chunking과 metadata enrichment 만들기

As a 개발자,
I want canonical document를 검색 가능한 chunk로 나누고 metadata를 보강하고 싶다,
So that retrieval 결과가 원본 문서와 위치 정보를 추적할 수 있다.

**Acceptance Criteria:**

**Given** canonical document가 있다
**When** chunker를 실행한다
**Then** 문서 내용이 설정 가능한 크기의 chunk 목록으로 분할된다
**And** 각 chunk에는 chunk index와 document reference가 포함된다.

**Given** chunk metadata가 필요하다
**When** chunk를 생성한다
**Then** source path, file type, data mode, source lineage가 각 chunk metadata에 포함된다
**And** answer generation 단계에서 citation으로 사용할 수 있는 정보가 보존된다.

**Given** 빈 문서나 매우 짧은 문서가 입력된다
**When** chunker를 실행한다
**Then** 빈 문서는 명확한 오류 또는 skipped 상태로 처리된다
**And** 짧은 문서는 하나의 유효 chunk로 처리될 수 있다.

### Story 2.4: Embedding provider abstraction과 fallback 만들기

As a 개발자,
I want embedding 생성 로직을 provider abstraction 뒤에 두고 key가 없을 때 fallback을 제공하고 싶다,
So that local smoke test가 외부 provider credentials 때문에 막히지 않는다.

**Acceptance Criteria:**

**Given** embedding provider 설정이 있다
**When** embedding을 생성한다
**Then** 설정된 provider를 통해 chunk embedding을 생성할 수 있다
**And** provider-specific 코드는 ingestion service에 직접 섞이지 않는다.

**Given** embedding provider key가 없다
**When** local smoke mode에서 embedding이 필요하다
**Then** deterministic fake/mock embedding 또는 명확한 skip mode를 사용할 수 있다
**And** 이 상태는 로그와 결과에 명확히 표시된다.

**Given** embedding 생성이 실패한다
**When** ingestion을 실행한다
**Then** 실패 원인이 기록된다
**And** partial success/failure 상태가 추적 가능하다.

### Story 2.5: Ingestion service와 CLI smoke command 만들기

As a 개발자,
I want sample markdown/txt 파일을 ingestion하는 service와 CLI command를 갖추고 싶다,
So that 웹 UI 없이 문서를 지식베이스에 적재하는 흐름을 검증할 수 있다.

**Acceptance Criteria:**

**Given** `sample_data/`에 markdown/txt 파일이 있다
**When** ingestion CLI command를 실행한다
**Then** loader, chunker, metadata enrichment, embedding/fallback, DB 저장 흐름이 순서대로 실행된다
**And** 처리된 document와 chunk 수가 출력된다.

**Given** ingestion 중 일부 파일이 실패한다
**When** command가 완료된다
**Then** 성공/실패/unsupported 파일 목록이 명확히 표시된다
**And** 실패한 파일 때문에 전체 결과가 조용히 성공으로 표시되지 않는다.

**Given** 개발자가 ingestion 결과를 검증하고 싶다
**When** DB 또는 debug command를 확인한다
**Then** 저장된 document, chunk, data mode, source lineage를 확인할 수 있다.

### Story 2.6: Source inventory 상태와 ingestion 결과 연결하기

As a 개발자/운영자,
I want source inventory의 지원 상태와 ingestion 결과를 연결하고 싶다,
So that 어떤 source가 지원, 미지원, 보류, 적재 완료 상태인지 추적할 수 있다.

**Acceptance Criteria:**

**Given** source inventory 항목이 있다
**When** ingestion 대상 source를 처리한다
**Then** source status를 supported, unsupported, deferred, ingested, failed 중 적절한 상태로 기록할 수 있다
**And** 상태 변경은 source inventory 또는 DB 기록에서 확인 가능하다.

**Given** unsupported source가 있다
**When** ingestion 대상에 포함된다
**Then** unsupported 상태로 명확히 표시된다
**And** 해당 source가 성공적으로 적재된 것처럼 처리되지 않는다.

**Given** ingestion이 완료된다
**When** 결과 summary를 확인한다
**Then** source별 처리 상태, document 수, chunk 수, 실패 사유를 확인할 수 있다.

### Story 2.7: 공식/공개 데이터 source 조사와 수집 방식 기록하기

As a 개발자/운영자,
I want 법령·고시 관련 공식/공개 데이터 source의 접근 방식과 제공 형식을 조사해 source inventory에 기록하고 싶다,
So that 실제 scraping 또는 API ingestion을 구현하기 전에 어떤 source를 우선 지원할지 판단할 수 있다.

**Acceptance Criteria:**

**Given** 법령·고시 도메인 확장을 위한 후보 source가 있다
**When** source 조사를 수행한다
**Then** 각 source의 이름, URL, 접근 방식, 제공 형식, 인증/API key 필요 여부, 필수 metadata 제공 여부를 기록한다
**And** 조사 결과는 `docs/source-inventory.md` 또는 source inventory 저장 구조에 반영된다.

**Given** source의 제공 형식이 markdown/txt가 아니다
**When** loader 지원 여부를 판단한다
**Then** XML, HTML, JSON, PDF, DOCX, HWP, OCR 필요 여부를 구분해 기록한다
**And** 현재 MVP에서 지원하지 않는 형식은 `deferred` 또는 `unsupported`로 표시한다.

**Given** 공식 데이터가 아직 ingestion되지 않았다
**When** source inventory를 확인한다
**Then** 해당 source는 실제 공식 지식베이스에 포함된 것처럼 표시되지 않는다
**And** 시스템은 sample/local data와 official data를 혼동하지 않는다.

**Given** 하나 이상의 source가 후속 구현 후보로 적합하다
**When** source inventory를 검토한다
**Then** 우선순위와 다음 구현에 필요한 loader/parser 작업이 명확히 드러난다
**And** 실제 scraping/API ingestion 구현은 별도 후속 story로 남는다.

## Epic 3: Evidence-Based RAG Answering and Smoke Tests

사용자는 자연어 질문으로 지식베이스를 검색하고, 출처·근거·메타데이터·데이터 모드가 포함된 답변을 CLI 또는 API로 받을 수 있다.

### Story 3.1: RAG smoke test용 sample knowledge fixture 만들기

As a 개발자,
I want RAG 검색/답변 검증용 sample 문서 fixture를 만들고 싶다,
So that official data 없이도 RAG Core 동작을 안전하게 검증할 수 있다.

**Acceptance Criteria:**

**Given** official domain data가 아직 ingestion되어 있지 않다
**When** RAG smoke test fixture를 준비한다
**Then** `sample_data/`에 최소 2개 markdown 또는 txt 샘플 문서가 존재한다
**And** 각 문서는 테스트용 sample data임을 명확히 표시한다.

**Given** sample 문서가 있다
**When** 문서 내용을 검토한다
**Then** 검색과 답변 검증에 사용할 수 있는 명시적 사실이 포함되어 있다
**And** 어떤 샘플도 공식 법령, 고시, 실제 감정평가 검토 결과처럼 보이지 않는다.

**Given** smoke test 질문이 필요하다
**When** fixture 문서를 추가한다
**Then** 질문, 기대 답변 요지, 기대 citation 또는 source path가 함께 문서화된다
**And** 공식 데이터가 없는 질문에 대해서는 no evidence 또는 insufficient evidence 기대값이 포함된다.

### Story 3.2: Vector retrieval 기본 검색 만들기

As a 개발자,
I want 저장된 chunk를 자연어 query로 검색할 수 있는 retriever를 만들고 싶다,
So that RAG 답변 생성 전에 관련 근거 chunk를 찾을 수 있다.

**Acceptance Criteria:**

**Given** ingestion된 document와 chunk가 있다
**When** 자연어 query로 retriever를 실행한다
**Then** 관련 chunk 후보 목록을 반환한다
**And** 각 결과에는 chunk id, document id, score 또는 relevance indicator가 포함된다.

**Given** vector embedding이 저장되어 있다
**When** retriever가 검색을 수행한다
**Then** pgvector 또는 설정된 vector search 방식을 사용한다
**And** 검색 로직은 API route가 아니라 `rag/` 계층에 위치한다.

**Given** 검색 결과가 없다
**When** retriever를 실행한다
**Then** 빈 결과를 명확히 반환한다
**And** 서버 오류로 처리하지 않는다.

### Story 3.3: Citation과 source metadata 포함 검색 결과 만들기

As a 개발자,
I want 검색 결과에 citation과 source metadata를 포함하고 싶다,
So that 답변이 어떤 문서와 chunk에 근거하는지 추적할 수 있다.

**Acceptance Criteria:**

**Given** retriever가 chunk를 반환한다
**When** 검색 결과를 API 또는 CLI 응답으로 변환한다
**Then** 각 결과에는 source path/name, data mode, chunk index, document id, chunk id가 포함된다
**And** answer generation에서 citation으로 사용할 수 있다.

**Given** source metadata가 일부 누락되어 있다
**When** 검색 결과를 구성한다
**Then** 누락된 필드는 `unknown` 또는 명확한 fallback 값으로 표시된다
**And** 존재하지 않는 공식 출처 URL이나 법령 metadata를 임의 생성하지 않는다.

**Given** sample data로 검색한다
**When** 검색 결과를 확인한다
**Then** data mode가 `sample` 또는 설정된 값으로 명확히 표시된다
**And** official data처럼 보이지 않는다.

### Story 3.4: 근거 기반 answer composer 만들기

As a 사용자,
I want 검색된 근거 chunk를 바탕으로 답변을 받고 싶다,
So that 답변 내용과 근거를 함께 확인할 수 있다.

**Acceptance Criteria:**

**Given** 사용자가 sample 문서에 포함된 사실을 질문한다
**When** 관련 chunk가 검색된다
**Then** answer composer는 검색된 chunk를 근거로 답변 텍스트를 생성한다
**And** 응답에는 citations와 data mode가 포함된다.

**Given** LLM provider 설정이 있다
**When** answer composer가 실행된다
**Then** 설정된 provider를 사용해 답변을 생성할 수 있다
**And** provider-specific 코드는 API route에 직접 섞이지 않는다.

**Given** LLM provider key가 없다
**When** local smoke mode에서 answer composer를 실행한다
**Then** deterministic fallback answer 또는 extractive summary를 반환할 수 있다
**And** fallback 상태가 응답 또는 로그에 명확히 표시된다.

**Given** 검색된 근거가 sample/local data다
**When** 답변을 생성한다
**Then** 답변은 공식 법령 검토 결과처럼 표현되지 않는다
**And** 필요한 경우 “sample/local data 기반”임을 명확히 표시한다.

### Story 3.5: 단일 질문 RAG CLI smoke command 만들기

As a 개발자,
I want CLI에서 단일 자연어 질문을 실행해 RAG 결과를 확인하고 싶다,
So that 웹 UI 없이 ingestion부터 retrieval, answer까지 end-to-end로 검증할 수 있다.

**Acceptance Criteria:**

**Given** sample document가 ingestion되어 있다
**When** CLI에서 sample 문서 내용에 대한 질문을 입력한다
**Then** 검색, answer composition, citation 출력이 순서대로 실행된다
**And** 답변 텍스트와 참조 chunk 목록이 표시된다.

**Given** 검색 결과가 없다
**When** CLI 질문을 실행한다
**Then** 명확한 no evidence 또는 insufficient local evidence 메시지를 출력한다
**And** 존재하지 않는 답변을 만들어내지 않는다.

**Given** 개발자가 RAG 흐름을 디버깅하고 싶다
**When** verbose 또는 debug 옵션을 사용한다
**Then** query, retrieved chunk count, selected citations, fallback 여부를 확인할 수 있다
**And** secret 값은 출력되지 않는다.

### Story 3.6: `POST /chat` 또는 `/query` 기본 RAG API 만들기

As a 개발자/API 사용자,
I want 자연어 질문을 보내고 RAG 답변을 받을 수 있는 기본 API endpoint를 갖추고 싶다,
So that 이후 웹 UI와 CRAG runtime이 같은 응답 계약을 사용할 수 있다.

**Acceptance Criteria:**

**Given** backend API가 실행 중이다
**When** 사용자가 질문을 `POST /chat` 또는 `/query`로 보낸다
**Then** API는 answer, citations, data_mode, insufficient_evidence 여부를 포함한 응답을 반환한다
**And** response shape는 이후 frontend에서 재사용 가능하다.

**Given** 요청 payload가 잘못되었다
**When** API endpoint를 호출한다
**Then** 일관된 error shape로 오류를 반환한다
**And** route handler는 validation과 service 호출 중심으로 얇게 유지된다.

**Given** 관련 chunk가 없다
**When** API endpoint를 호출한다
**Then** HTTP server error가 아니라 정상 응답의 insufficient evidence 상태로 처리한다
**And** 답변은 근거 부족을 명확히 알린다.

### Story 3.7: RAG response safety policy 적용하기

As a 사용자,
I want 시스템이 제공되지 않은 공식 법령 데이터나 업무 문서를 임의로 만들어 답하지 않기를 원한다,
So that sample/local data 기반 답변과 공식 검토 결과를 혼동하지 않을 수 있다.

**Acceptance Criteria:**

**Given** official data가 ingestion되어 있지 않다
**When** 사용자가 공식 법령 검토처럼 보이는 질문을 한다
**Then** 시스템은 official data가 없음을 명확히 표시한다
**And** 공식 출처, 개정일, 시행일, 조항을 임의 생성하지 않는다.

**Given** 사용자가 법률 위반 여부나 감정평가 적정성을 단정적으로 묻는다
**When** 시스템이 답변한다
**Then** 법률 위반, 적법성, 감정평가 적정성을 단정하지 않는다
**And** 참고용 검토 보조 또는 근거 기반 제한적 답변임을 표시한다.

**Given** 답변에 citations가 포함된다
**When** 사용자가 출처를 확인한다
**Then** citations는 실제 검색된 chunk metadata에서만 생성된다
**And** 없는 URL이나 source metadata는 만들어내지 않는다.

### Story 3.8: RAG API/CLI smoke test 자동화하기

As a 개발자,
I want RAG Core의 기본 흐름을 자동 smoke test로 검증하고 싶다,
So that 이후 CRAG와 웹 UI 구현 전에 regression을 줄일 수 있다.

**Acceptance Criteria:**

**Given** sample data와 local fallback provider가 준비되어 있다
**When** smoke test를 실행한다
**Then** sample ingestion, retrieval, answer composition, citation generation 흐름이 검증된다
**And** 외부 LLM/embedding key 없이도 최소 테스트가 통과할 수 있다.

**Given** 검색 근거가 없는 질문이 있다
**When** smoke test를 실행한다
**Then** insufficient evidence 또는 no evidence 응답이 검증된다
**And** hallucinated official answer가 생성되지 않음을 확인한다.

**Given** API response contract가 있다
**When** smoke test가 API endpoint를 호출한다
**Then** answer, citations, data_mode, insufficient_evidence 필드가 존재함을 검증한다
**And** 이후 frontend와 CRAG story가 같은 contract를 신뢰할 수 있다.

## Epic 4: Multi-Turn CRAG Conversation Runtime

사용자는 멀티턴 대화에서 이전 문맥을 유지하며 후속 질문을 할 수 있고, 시스템은 검색 결과를 평가해 query rewrite, re-retrieval, insufficient evidence 응답, retrieval trace를 제공할 수 있다.

### Story 4.1: Conversation과 Message 저장 모델 만들기

As a 개발자,
I want conversation과 message를 저장하는 최소 DB 모델을 만들고 싶다,
So that 멀티턴 대화의 이전 질문과 답변 맥락을 추적할 수 있다.

**Acceptance Criteria:**

**Given** SQLAlchemy/Alembic 기반이 준비되어 있다
**When** conversation과 message 모델을 추가한다
**Then** `conversations`와 `messages` table이 migration으로 생성된다
**And** 각 message는 conversation에 연결된다.

**Given** 사용자가 새 질문을 보낸다
**When** conversation id가 없다
**Then** 새 conversation을 생성할 수 있다
**And** 생성된 conversation id가 응답에 포함된다.

**Given** 사용자가 후속 질문을 보낸다
**When** conversation id가 제공된다
**Then** 해당 conversation에 message가 추가된다
**And** 이전 message history를 조회할 수 있다.

### Story 4.2: Retrieval trace 저장 모델 만들기

As a 개발자,
I want retrieval trace를 저장하는 모델을 만들고 싶다,
So that RAG/CRAG 실행 흐름과 근거 부족 원인을 디버깅할 수 있다.

**Acceptance Criteria:**

**Given** RAG 또는 CRAG 실행이 발생한다
**When** retrieval trace를 저장한다
**Then** original query, retrieved chunk ids, relevance result, insufficient evidence reason을 기록할 수 있다
**And** trace는 conversation/message와 연결될 수 있다.

**Given** query rewrite가 발생한다
**When** retrieval trace를 저장한다
**Then** rewritten query와 re-retrieval 결과를 기록할 수 있다
**And** rewrite가 없으면 해당 필드는 비어 있거나 null로 명확히 표현된다.

**Given** trace를 확인한다
**When** local debug 또는 API 응답 summary를 본다
**Then** 검색 흐름을 이해할 수 있는 요약 정보가 제공된다
**And** 민감한 사용자 원문을 과도하게 저장하지 않는 정책이 반영된다.

### Story 4.3: LangGraph conversation state 기본 흐름 만들기

As a 개발자,
I want LangGraph 기반 conversation state 흐름을 만들고 싶다,
So that 멀티턴 질문에서 이전 대화 맥락을 사용할 수 있다.

**Acceptance Criteria:**

**Given** 사용자가 첫 질문을 보낸다
**When** graph runtime이 실행된다
**Then** conversation state가 생성되고 사용자 message가 기록된다
**And** 기존 RAG retriever/answer composer를 재사용해 응답을 생성한다.

**Given** 사용자가 conversation id와 함께 후속 질문을 보낸다
**When** graph runtime이 실행된다
**Then** 이전 message history를 state에 포함한다
**And** 후속 질문이 이전 맥락을 참조할 수 있다.

**Given** LangGraph node transition이 발생한다
**When** local logging이 활성화되어 있다
**Then** 주요 node transition과 상태 요약이 로그에 남는다
**And** LangSmith가 없어도 local debugging이 가능하다.

### Story 4.4: Retrieval grading 만들기

As a 사용자,
I want 시스템이 검색 결과가 질문에 충분히 관련 있는지 평가하길 원한다,
So that 관련 없는 근거로 답변하지 않도록 할 수 있다.

**Acceptance Criteria:**

**Given** retriever가 chunk 후보를 반환한다
**When** retrieval grading을 수행한다
**Then** 검색 결과가 sufficient, weak, irrelevant 또는 이에 준하는 상태로 평가된다
**And** 평가 결과가 retrieval trace에 기록된다.

**Given** 검색 결과가 충분하다
**When** graph runtime이 다음 단계를 결정한다
**Then** answer composer로 진행한다
**And** citations는 실제 retrieved chunk에서 생성된다.

**Given** 검색 결과가 약하거나 관련 없다
**When** graph runtime이 다음 단계를 결정한다
**Then** query rewrite 또는 insufficient evidence 경로로 이동할 수 있다
**And** server error로 처리하지 않는다.

### Story 4.5: Query rewrite와 re-retrieval 만들기

As a 사용자,
I want 검색 결과가 약할 때 시스템이 질문을 보정하고 다시 검색하길 원한다,
So that 한 번의 검색 실패로 바로 포기하지 않을 수 있다.

**Acceptance Criteria:**

**Given** retrieval grading 결과가 weak 또는 irrelevant다
**When** query rewrite가 실행된다
**Then** 원래 질문을 보존한 상태로 rewritten query가 생성된다
**And** rewritten query는 retrieval trace에 기록된다.

**Given** rewritten query가 생성되었다
**When** re-retrieval이 실행된다
**Then** 새 검색 결과가 retrieval trace에 기록된다
**And** 검색 재시도 횟수는 설정된 제한을 넘지 않는다.

**Given** LLM provider key가 없다
**When** local smoke mode에서 query rewrite가 필요하다
**Then** deterministic rewrite fallback 또는 rewrite skipped 상태를 사용할 수 있다
**And** fallback/skipped 상태가 응답 또는 로그에 명확히 표시된다.

### Story 4.6: Insufficient evidence 응답 경로 만들기

As a 사용자,
I want 근거가 부족할 때 시스템이 모른다고 말하길 원한다,
So that 없는 근거로 그럴듯한 답변을 받지 않는다.

**Acceptance Criteria:**

**Given** initial retrieval과 re-retrieval 후에도 충분한 근거가 없다
**When** graph runtime이 응답을 생성한다
**Then** insufficient evidence 상태의 정상 응답을 반환한다
**And** HTTP server error로 처리하지 않는다.

**Given** official data가 ingestion되어 있지 않다
**When** 사용자가 공식 법령/고시 검토 질문을 한다
**Then** 시스템은 공식 데이터가 없음을 명확히 표시한다
**And** 공식 출처, 개정일, 시행일, 조항을 임의 생성하지 않는다.

**Given** 사용자가 법률 위반 여부나 감정평가 적정성을 단정적으로 묻는다
**When** 근거가 부족하거나 도메인 판단이 필요한 경우
**Then** 시스템은 단정하지 않고 참고용 검토 보조 또는 추가 자료 필요 상태로 응답한다
**And** 그 이유가 trace summary 또는 response message에 남는다.

### Story 4.7: Multi-turn chat API contract 확장하기

As a 개발자/API 사용자,
I want chat API가 conversation id와 retrieval trace summary를 포함하길 원한다,
So that 웹 UI와 디버깅 도구가 멀티턴 상태와 CRAG 흐름을 사용할 수 있다.

**Acceptance Criteria:**

**Given** 사용자가 `POST /chat`에 새 질문을 보낸다
**When** conversation id가 없다
**Then** API는 새 conversation_id를 반환한다
**And** message_id와 answer를 함께 반환한다.

**Given** 사용자가 기존 conversation_id로 후속 질문을 보낸다
**When** API가 요청을 처리한다
**Then** 같은 conversation에 message가 추가된다
**And** 응답은 이전 맥락을 반영할 수 있다.

**Given** CRAG 흐름이 실행된다
**When** API 응답이 반환된다
**Then** answer, citations, data_mode, insufficient_evidence, retrieval_trace_id 또는 trace summary가 포함된다
**And** frontend가 상태 표시를 위해 사용할 수 있는 일관된 shape를 유지한다.

### Story 4.8: 3턴 대화 smoke test 만들기

As a 개발자,
I want 최소 3턴 이상의 멀티턴 CRAG smoke test를 만들고 싶다,
So that conversation state, retrieval grading, rewrite, insufficient evidence 흐름을 검증할 수 있다.

**Acceptance Criteria:**

**Given** sample fixture 문서가 ingestion되어 있다
**When** 3턴 smoke test를 실행한다
**Then** 첫 질문, 후속 질문, 맥락 참조 질문이 같은 conversation에서 처리된다
**And** 각 turn의 message와 trace가 확인 가능하다.

**Given** 한 turn에서 검색 결과가 부족하다
**When** smoke test가 실행된다
**Then** query rewrite, re-retrieval, 또는 insufficient evidence 경로 중 하나가 검증된다
**And** 없는 공식 데이터를 만들어내지 않는다.

**Given** LangSmith 설정이 없다
**When** smoke test를 실행한다
**Then** local logs와 retrieval trace만으로 주요 graph 흐름을 확인할 수 있다
**And** 외부 tracing 설정이 없어도 테스트가 통과할 수 있다.

## Epic 5: Svelte Web Chat Experience

사용자는 웹 화면에서 자연어 멀티턴 RAG 챗봇을 사용할 수 있고, 메시지, 출처/근거, 데이터 모드, 로딩, 오류, 근거 부족 상태를 확인할 수 있다.

### Story 5.1: SvelteKit frontend 초기화와 기본 레이아웃 만들기

As a 사용자,
I want 웹 브라우저에서 챗봇 화면에 접근하고 싶다,
So that CLI/API 없이 RAG 챗봇을 사용할 수 있다.

**Acceptance Criteria:**

**Given** backend RAG API가 준비되어 있다
**When** frontend 프로젝트를 초기화한다
**Then** `frontend/` SvelteKit 앱이 생성된다
**And** local development 실행 방법이 문서화된다.

**Given** 사용자가 웹 앱을 연다
**When** 기본 페이지가 로드된다
**Then** 채팅 중심 레이아웃이 표시된다
**And** 메시지 목록 영역, 입력 영역, 상태 표시 영역이 구분되어 있다.

**Given** frontend가 아직 복잡한 기능을 갖추지 않았다
**When** 코드를 검토한다
**Then** V1에 불필요한 복잡한 global state management가 도입되지 않는다
**And** backend API 호출을 위한 단순한 구조를 가진다.

### Story 5.2: Chat input과 message list 만들기

As a 사용자,
I want 자연어 질문을 입력하고 대화 메시지를 볼 수 있다,
So that 버튼 중심 workflow 없이 챗봇과 대화할 수 있다.

**Acceptance Criteria:**

**Given** 사용자가 채팅 화면을 열었다
**When** 질문을 입력하고 제출한다
**Then** 사용자 메시지가 message list에 표시된다
**And** 입력창은 다음 질문을 받을 준비가 된다.

**Given** 사용자가 키보드로 입력한다
**When** Enter 또는 명확한 제출 동작을 사용한다
**Then** 질문이 전송된다
**And** 빈 질문은 전송되지 않는다.

**Given** 대화가 여러 turn으로 이어진다
**When** 새 메시지가 추가된다
**Then** 메시지 목록은 사용자 메시지와 assistant 응답을 구분해 표시한다
**And** 읽기 쉬운 순서로 유지된다.

### Story 5.3: Backend chat API 연결하기

As a 사용자,
I want 웹 화면에서 질문을 보내고 backend RAG/CRAG 답변을 받고 싶다,
So that 검증된 RAG Core를 브라우저에서 사용할 수 있다.

**Acceptance Criteria:**

**Given** backend `POST /chat` API가 실행 중이다
**When** 사용자가 질문을 제출한다
**Then** frontend는 질문과 conversation_id를 backend에 전송한다
**And** API 응답을 받아 assistant 메시지로 표시한다.

**Given** 첫 질문을 보낸다
**When** backend가 conversation_id를 반환한다
**Then** frontend는 conversation_id를 저장한다
**And** 이후 후속 질문에 같은 conversation_id를 사용한다.

**Given** API 호출이 실패한다
**When** 오류가 발생한다
**Then** 사용자에게 명확한 오류 상태를 표시한다
**And** 오류가 message list를 조용히 깨뜨리지 않는다.

### Story 5.4: Citation과 source panel 표시하기

As a 사용자,
I want 답변의 출처와 근거 chunk를 확인하고 싶다,
So that 답변이 어떤 문서에 기반했는지 판단할 수 있다.

**Acceptance Criteria:**

**Given** API 응답에 citations가 포함되어 있다
**When** assistant 응답을 표시한다
**Then** 각 citation의 source name/path, chunk index, data mode를 표시한다
**And** citation은 실제 API 응답에서 받은 값만 사용한다.

**Given** citation metadata 일부가 `unknown`이다
**When** citation을 표시한다
**Then** unknown 값을 명확히 표시한다
**And** 없는 공식 URL이나 법령 metadata를 frontend에서 임의 생성하지 않는다.

**Given** citation이 여러 개 있다
**When** 사용자가 답변을 확인한다
**Then** 답변 본문과 citation 목록이 구분되어 보인다
**And** 사용자가 근거를 확인하기 쉽다.

### Story 5.5: Data mode와 safety 상태 표시하기

As a 사용자,
I want 답변이 sample, official, user_provided 중 어떤 데이터에 기반했는지 보고 싶다,
So that 샘플 답변과 공식 검토 결과를 혼동하지 않을 수 있다.

**Acceptance Criteria:**

**Given** API 응답에 data_mode가 포함되어 있다
**When** assistant 응답을 표시한다
**Then** data mode가 눈에 띄게 표시된다
**And** `sample` 또는 `unknown`인 경우 official answer처럼 보이지 않는다.

**Given** official data가 없는 상태다
**When** 사용자가 법령/고시 관련 질문을 한다
**Then** frontend는 backend의 official data 없음 또는 insufficient evidence 메시지를 그대로 표시한다
**And** 사용자에게 공식 검토 결과로 오해될 표현을 추가하지 않는다.

**Given** 답변이 참고용 검토 보조 성격이다
**When** 답변을 표시한다
**Then** 법률 위반 여부나 감정평가 적정성 단정으로 보이지 않게 표시한다
**And** 필요한 경우 safety notice 또는 data mode notice를 함께 보여준다.

### Story 5.6: Loading, error, insufficient evidence 상태 표시하기

As a 사용자,
I want 질문 처리 중, 오류, 근거 부족 상태를 명확히 알고 싶다,
So that 시스템이 멈췄는지, 실패했는지, 근거가 부족한지 구분할 수 있다.

**Acceptance Criteria:**

**Given** 질문이 backend로 전송되었다
**When** 응답을 기다리는 중이다
**Then** loading 상태가 표시된다
**And** 사용자는 처리가 진행 중임을 알 수 있다.

**Given** backend가 insufficient_evidence 상태를 반환한다
**When** 응답을 표시한다
**Then** 근거 부족 상태가 명확히 표시된다
**And** 이를 서버 오류나 빈 답변처럼 보이게 하지 않는다.

**Given** API error가 발생한다
**When** 오류를 표시한다
**Then** 사용자에게 이해 가능한 오류 메시지를 보여준다
**And** 필요하면 다시 시도할 수 있는 상태로 유지한다.

### Story 5.7: 3턴 웹 채팅 smoke test 만들기

As a 개발자,
I want 웹 UI에서 최소 3턴 대화를 검증하고 싶다,
So that backend CRAG conversation runtime이 frontend와 연결되어 동작하는지 확인할 수 있다.

**Acceptance Criteria:**

**Given** backend와 frontend가 local에서 실행 중이다
**When** sample fixture 기반 질문을 3턴 이상 입력한다
**Then** 같은 conversation_id로 대화가 이어진다
**And** 각 turn의 사용자 메시지와 assistant 응답이 화면에 표시된다.

**Given** 답변에 citations와 data_mode가 포함되어 있다
**When** 웹 smoke test를 수행한다
**Then** citation과 data mode가 화면에 표시된다
**And** sample data가 official data처럼 보이지 않는다.

**Given** 근거가 없는 질문을 입력한다
**When** backend가 insufficient evidence를 반환한다
**Then** 웹 UI는 근거 부족 상태를 명확히 표시한다
**And** hallucinated official answer를 보여주지 않는다.

## Epic 6: Domain Extension Readiness (Post-MVP)

운영자/개발자는 법령·고시 도메인 확장을 위해 공식/공개 소스 후보를 source inventory로 관리하고, 법령명, 조항, 개정일, 시행일, 수집일, 출처 URL, 최근 X기간 필터, 알림 레벨 같은 도메인 메타데이터를 수용할 준비를 할 수 있다.

### Story 6.1: 법령·고시 domain metadata schema 확장 설계하기

As a 개발자,
I want 법령·고시 데이터에 필요한 domain metadata schema를 설계하고 싶다,
So that 향후 official source ingestion 시 개정일, 시행일, 조항, 출처를 구조적으로 저장할 수 있다.

**Acceptance Criteria:**

**Given** 기존 canonical document schema가 있다
**When** domain metadata 확장을 설계한다
**Then** 법령명/자료명, 조항, 개정일, 시행일, 수집일, 출처 URL, source authority 필드를 정의한다
**And** 기존 sample/local document schema와 호환된다.

**Given** 날짜 metadata가 여러 종류다
**When** schema를 검토한다
**Then** 작성일, 수집일, 개정일, 시행일, 평가기준일을 혼동하지 않도록 구분한다
**And** 각 필드의 의미가 문서화되어 있다.

**Given** metadata가 누락된 source가 있다
**When** schema를 적용한다
**Then** 누락 값은 unknown 또는 null로 표현할 수 있다
**And** 시스템이 누락된 공식 metadata를 임의 생성하지 않는다.

### Story 6.2: 공식 source 후보 우선순위와 지원 상태 확정하기

As a 개발자/운영자,
I want 공식/공개 법령·고시 source 후보의 우선순위와 지원 상태를 확정하고 싶다,
So that 어떤 source부터 ingestion 구현할지 결정할 수 있다.

**Acceptance Criteria:**

**Given** Epic 2.7에서 조사된 source inventory가 있다
**When** source 후보를 검토한다
**Then** 각 source에 priority, support status, access method, expected loader type을 기록한다
**And** unsupported/deferred source는 명확한 사유를 가진다.

**Given** 여러 source가 있다
**When** 우선순위를 정한다
**Then** 접근 안정성, 제공 형식, 필수 metadata 제공 여부, 구현 난이도를 기준으로 판단한다
**And** 실제 ingestion 대상 source가 최소 하나 이상 후보로 선정된다.

**Given** source가 아직 ingestion되지 않았다
**When** source inventory를 확인한다
**Then** 해당 source는 official knowledge base에 포함된 것처럼 표시되지 않는다
**And** 상태는 planned, deferred, unsupported 등으로 명확히 구분된다.

### Story 6.3: 첫 official source loader/parser 구현하기

As a 개발자,
I want 우선순위가 높은 official source 하나에 대한 loader/parser를 구현하고 싶다,
So that 실제 공식/공개 데이터를 canonical document schema로 변환할 수 있다.

**Acceptance Criteria:**

**Given** 우선순위가 확정된 official source가 있다
**When** loader/parser를 구현한다
**Then** 해당 source의 제공 형식(XML/HTML/JSON 등)을 읽어 canonical document로 변환할 수 있다
**And** source authority, source URL, 수집일, 제공 가능한 domain metadata가 포함된다.

**Given** source 구조가 예상과 다르다
**When** loader/parser가 실패한다
**Then** 명확한 오류 또는 failed status를 기록한다
**And** partial/invalid data를 official data로 조용히 저장하지 않는다.

**Given** 필수 metadata가 부족하다
**When** canonical document를 생성한다
**Then** 부족한 필드는 unknown/null로 표시한다
**And** 개정일, 시행일, 조항, 출처 URL을 임의 생성하지 않는다.

### Story 6.4: Official data ingestion smoke test 만들기

As a 개발자,
I want 첫 official source ingestion smoke test를 만들고 싶다,
So that 공식/공개 데이터가 sample data와 구분되어 저장되는지 확인할 수 있다.

**Acceptance Criteria:**

**Given** official source loader/parser가 있다
**When** official ingestion smoke test를 실행한다
**Then** 최소 하나의 official document가 canonical schema와 domain metadata를 포함해 저장된다
**And** data mode는 `official`로 표시된다.

**Given** official source ingestion이 실패한다
**When** smoke test를 실행한다
**Then** 실패 사유가 명확히 기록된다
**And** 실패한 데이터를 official knowledge base에 포함된 것처럼 표시하지 않는다.

**Given** official data와 sample data가 함께 존재한다
**When** 저장된 document와 chunk를 확인한다
**Then** data mode와 source metadata로 둘을 구분할 수 있다
**And** RAG 응답에서 source lineage가 유지된다.

### Story 6.5: 최근 X기간 필터 설계와 검색 조건 연결하기

As a 사용자,
I want 최근 X기간 안에 변경된 자료를 기준으로 질문하고 싶다,
So that 오래된 자료와 최근 변경사항을 구분해 검토할 수 있다.

**Acceptance Criteria:**

**Given** official documents에 개정일 또는 시행일 metadata가 있다
**When** 최근 X기간 필터를 적용한다
**Then** 검색 또는 후처리 단계에서 해당 기간 조건을 사용할 수 있다
**And** 어떤 날짜 필드를 기준으로 필터링했는지 명확히 표시한다.

**Given** 날짜 metadata가 부족하다
**When** 최근 X기간 필터가 요청된다
**Then** 시스템은 필터 적용이 제한됨을 알린다
**And** 부족한 날짜를 임의 생성하지 않는다.

**Given** 사용자가 자연어로 “최근 1년” 같은 표현을 사용한다
**When** query를 처리한다
**Then** 기간 조건을 구조화된 filter 후보로 변환할 수 있다
**And** 불확실한 경우 사용자에게 명확한 제한 또는 확인 필요 상태를 제공한다.

### Story 6.6: 알림 레벨을 작업 우선순위로 정의하기

As a 사용자,
I want 변경사항의 알림 레벨을 법적 판단이 아니라 작업 우선순위로 보고 싶다,
So that 시스템 답변을 위법/적법 판단으로 오해하지 않을 수 있다.

**Acceptance Criteria:**

**Given** 관련 가능성이 있는 변경사항이 검색된다
**When** 알림 레벨을 표시한다
**Then** 레벨은 high/medium/low 또는 이에 준하는 작업 우선순위로 표현된다
**And** 위법, 적법, 법적 책임 판단으로 표현되지 않는다.

**Given** 알림 레벨 산정 근거가 부족하다
**When** 응답을 생성한다
**Then** 시스템은 낮은 신뢰도 또는 추가 확인 필요를 표시한다
**And** 확정적인 판단을 만들지 않는다.

**Given** 사용자가 “왜 high야?”라고 묻는다
**When** 시스템이 설명한다
**Then** 검색된 근거, 날짜 조건, 출처 기반 이유를 설명한다
**And** 전문적/법률적 최종 판단은 사용자 책임임을 유지한다.

### Story 6.7: Domain safety policy와 response copy 정리하기

As a 사용자,
I want 법령·감정평가 관련 답변이 참고용 검토 보조임을 명확히 알 수 있다,
So that 시스템 응답을 최종 법률·전문 판단으로 오해하지 않는다.

**Acceptance Criteria:**

**Given** 사용자가 법령·고시 또는 감정평가 관련 질문을 한다
**When** 시스템이 답변한다
**Then** 답변은 참고용 검토 보조임을 명확히 표현한다
**And** 법률 위반 여부, 적법성, 감정평가 적정성을 단정하지 않는다.

**Given** official source metadata가 부족하다
**When** 답변을 생성한다
**Then** 출처 확인 필요, 근거 부족, 추가 자료 필요 상태를 명확히 표시한다
**And** 부족한 정보를 그럴듯하게 보완하지 않는다.

**Given** domain response copy가 여러 화면/API에서 쓰인다
**When** copy를 검토한다
**Then** backend와 frontend가 일관된 safety wording을 사용할 수 있다
**And** sample, official, user_provided data mode에 따라 오해 가능성이 낮아진다.
