---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - "_bmad-output/planning-artifacts/prd.md"
  - "_bmad-output/planning-artifacts/prd-validation-report.md"
  - "_bmad-output/brainstorming/brainstorming-session-2026-05-15-151738.md"
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-05-16'
project_name: 'langchain-property-appraiser'
user_name: 'PSJ'
date: '2026-05-16'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

이 프로젝트는 LangChain/LangGraph 기반 RAG 챗봇 웹 애플리케이션이다. V1의 목적은 감정평가 도메인 완성보다, 문서 ingestion부터 근거 기반 멀티턴 답변까지 이어지는 RAG Core를 학습하고 검증하는 것이다.

아키텍처는 네 가지 큰 영역으로 나눠 생각한다.

1. **Document Ingestion**
   - markdown/txt 문서를 로딩한다.
   - 공통 문서 schema로 변환한다.
   - chunking, metadata 부여, embedding, vector store 적재를 수행한다.

2. **RAG/CRAG Chat Runtime**
   - 사용자의 자연어 질문을 처리한다.
   - 관련 chunk를 검색한다.
   - 검색 결과가 부족하면 query rewrite 또는 근거 부족 응답으로 처리한다.
   - 최소 3턴 이상의 대화 문맥을 유지한다.

3. **Source, Data Mode, Safety**
   - 답변에는 출처와 근거 chunk를 포함한다.
   - 테스트/샘플 데이터와 공식 데이터를 구분한다.
   - 법률 위반, 감정평가 적정성, 법적 책임을 단정하지 않는다.
   - 공식 데이터가 없으면 공식 검토 결과처럼 응답하지 않는다.

4. **Web Chat UI**
   - Svelte 기반 채팅 화면을 제공한다.
   - 메시지, 답변, 출처, 데이터 모드, 로딩, 오류, 근거 부족 상태를 표시한다.
   - RAG Core가 먼저 API/CLI에서 검증된 뒤 웹 UI에 연결된다.

### Key Architectural Concerns

- RAG Core와 Web UI를 분리해 먼저 백엔드/API 수준에서 검증한다.
- V1에서는 markdown/txt ingestion과 API/CLI smoke test를 먼저 완성한 뒤 Svelte UI를 연결한다.
- 문서, chunk, 출처 metadata의 구조를 초기에 일관되게 잡는다.
- 근거 부족은 오류가 아니라 정상적인 안전 응답 경로로 처리한다.
- 채팅 UI는 답변뿐 아니라 출처, 데이터 모드, 근거 부족 상태를 함께 보여준다.
- LangSmith 같은 tracing 도구는 선택 사항이며, 없어도 로컬 로그로 동작해야 한다.
- 향후 법령/고시 도메인 확장을 고려하되, V1에서는 범용 RAG 챗봇 구조를 우선한다.

### Complexity Assessment

- Primary domain: Full-stack RAG web application
- Complexity level: High
- Main complexity drivers:
  - 문서 처리와 채팅 실행 흐름의 분리
  - 멀티턴 대화 상태
  - CRAG 기반 검색 품질 보정
  - 출처/근거/데이터 모드 표시
  - 법률·감정평가 도메인 관련 안전 응답 정책

## Starter Template Evaluation

### Primary Technology Domain

이 프로젝트는 full-stack RAG web application이다. 단, V1 구현 순서는 백엔드/RAG Core 우선이다.

### Starter Options Considered

1. **Backend-first FastAPI project**
   - FastAPI 기반 API 서버를 먼저 구성한다.
   - LangChain/LangGraph RAG Core, ingestion, retrieval, CRAG smoke test를 먼저 검증한다.
   - Svelte UI는 이후 별도 `frontend/`로 추가한다.
   - 이 프로젝트의 학습 목표와 phase 구조에 가장 잘 맞는다.

2. **Separated full-stack structure**
   - `backend/` FastAPI
   - `frontend/` SvelteKit
   - 처음부터 프론트/백엔드 경계가 명확하다.
   - 다만 RAG Core 검증 전에 UI 설정 부담이 생길 수 있다.

3. **SvelteKit-first structure**
   - SvelteKit 앱을 먼저 만들고 API를 나중에 붙인다.
   - 채팅 UI 시작은 빠르지만, LangChain/LangGraph 중심의 백엔드 학습 목표와는 덜 맞는다.

### Selected Starter: Backend-first FastAPI, then SvelteKit

**Rationale for Selection:**

V1의 핵심 목표는 감정평가 도메인 완성이 아니라 RAG Core와 LangGraph CRAG 흐름을 검증하는 것이다. 따라서 웹 UI보다 FastAPI 기반 backend와 CLI/API smoke test를 먼저 만든다. 이후 검증된 API를 SvelteKit 채팅 UI에 연결한다.

**Verified Current Package/CLI References:**

- FastAPI latest checked via PyPI: `0.136.1`
- Uvicorn latest checked via PyPI: `0.47.0`
- LangChain latest checked via PyPI: `1.3.1`
- LangGraph latest checked via PyPI: `1.2.0`
- Svelte CLI `sv` latest checked via npm: `0.15.3`
- Legacy `create-svelte` latest checked via npm: `7.0.1`

### Initialization Approach

**Backend initialization:**

```bash
mkdir -p backend
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install fastapi uvicorn langchain langgraph
```

**Frontend initialization, later phase:**

```bash
npx sv create frontend
```

### Architectural Decisions Provided by Starter

**Language & Runtime:**

- Backend: Python / FastAPI
- Frontend: SvelteKit, added after RAG Core validation

**Build Tooling:**

- Backend starts minimal with Python virtual environment and explicit dependencies.
- Frontend uses the official Svelte CLI when Phase 3 begins.

**Code Organization:**

Initial structure:

```text
backend/
  app/
    api/
    core/
    ingestion/
    rag/
    graph/
    models/
    services/
  tests/
frontend/   # added later
docs/
```

**Development Experience:**

- RAG Core can be tested without browser UI.
- CLI/API smoke tests come before Svelte integration.
- Frontend remains a thin client over the FastAPI chat/query API.

**Note:** Project initialization using this approach should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions:**

- Backend-first FastAPI architecture
- PostgreSQL + pgvector as the primary database/vector store from V1
- SQLAlchemy + Alembic for schema modeling and migrations
- Docker Compose for local PostgreSQL/pgvector development
- REST API between frontend and backend
- No authentication in V1 learning phase

**Important Decisions:**

- Keep document, chunk, source metadata, conversation, message, and retrieval trace concepts separate.
- Keep LangChain vector store integration optional; application-owned SQLAlchemy models define the core schema.
- Treat insufficient evidence as a normal response state.
- Keep embedding provider configurable through environment variables.
- Keep LangSmith optional.
- Keep official legal/regulatory source ingestion post-MVP.

**Deferred Decisions:**

- Authentication and user accounts
- Real user document upload and retention policy
- Official law/gazette crawling automation
- Cloud deployment and CI/CD
- Advanced index tuning and retrieval optimization
- Local embedding model selection

### Data Architecture

V1부터 PostgreSQL을 기본 relational database로 사용한다. Vector storage는 PostgreSQL 확장인 pgvector를 사용한다.

**Selected stack:**

- PostgreSQL
- pgvector
- SQLAlchemy
- Alembic
- psycopg
- Optional: `langchain-postgres` for LangChain integration

PostgreSQL을 바로 사용하는 이유는 다음과 같다.

- documents, chunks, conversations, messages, retrieval traces, source inventory를 한 DB 안에서 일관되게 관리할 수 있다.
- chunk metadata와 vector embedding의 연결을 단순하게 유지할 수 있다.
- SQLite/local vector store에서 PostgreSQL/pgvector로 마이그레이션하는 비용을 줄인다.
- RAG 디버깅에 필요한 retrieval trace와 source lineage를 relational schema로 추적하기 쉽다.

V1에서 유지할 핵심 개념 모델:

- documents
- chunks
- conversations
- messages
- retrieval_traces
- source_inventory

초기 구현 story에서는 이 개념 모델을 기반으로 최소 SQLAlchemy model과 Alembic migration을 만든다. 상세 index 전략과 고급 retrieval 최적화는 실제 query/retrieval 패턴이 확인된 뒤 조정한다.

LangChain의 PostgreSQL vector store 통합은 사용할 수 있지만, core schema의 소유권은 애플리케이션 SQLAlchemy model에 둔다.

### Authentication & Security

V1은 인증을 포함하지 않는다. 프로젝트는 local learning/development application으로 시작한다.

Security priorities for V1:

- API key, DB URL, LangSmith key는 코드에 하드코딩하지 않는다.
- `.env`와 environment variables로 설정한다.
- 설정 관리는 `pydantic-settings`를 사용한다.
- 테스트/샘플 데이터와 공식 데이터를 구분한다.
- 실제 민감 사용자 문서는 retention, deletion, external LLM/tracing 정책이 정의되기 전까지 처리하지 않는다.
- LangSmith는 optional이며, 기본적으로 민감 원문이 trace에 남지 않도록 한다.

Authentication, user accounts, authorization, and multi-user isolation are deferred.

### API & Communication Patterns

Backend는 REST API를 제공한다.

Initial API surface:

- `POST /ingest`
- `POST /chat`
- `GET /conversations/{id}`
- Optional local-only debug endpoint for retrieval traces

API responses should include:

- answer text
- source/citation references
- data mode
- insufficient evidence status
- session/conversation id
- retrieval trace summary where appropriate

### Frontend Architecture

Frontend는 RAG Core가 API/CLI smoke test로 검증된 뒤 추가한다.

SvelteKit frontend는 thin chat client로 유지한다.

- chat input
- message list
- answer display
- source/citation display
- data mode display
- loading/error/insufficient evidence states

복잡한 global state management는 V1에서 사용하지 않는다.

### Infrastructure & Deployment

V1은 local-first이다.

하지만 PostgreSQL + pgvector를 바로 사용하므로 local development DB는 Docker Compose로 실행한다.

Initial infrastructure decisions:

- FastAPI backend runs locally.
- PostgreSQL + pgvector runs through Docker Compose.
- SvelteKit frontend runs locally after Phase 3 begins.
- Secrets are configured through `.env`.
- Local logs are the baseline observability mechanism.
- LangSmith is enabled only when configured.

Deferred:

- production Dockerization
- cloud hosting
- CI/CD
- production monitoring
- scaling strategy

### Decision Impact Analysis

**Implementation Sequence:**

1. Create backend project skeleton.
2. Add environment configuration with `pydantic-settings`.
3. Add Docker Compose for PostgreSQL + pgvector.
4. Add SQLAlchemy and Alembic.
5. Create initial models/migrations for documents, chunks, conversations, messages, retrieval traces, and source inventory.
6. Implement markdown/txt ingestion.
7. Implement embedding and pgvector-backed retrieval.
8. Implement REST chat API and CRAG runtime.
9. Add SvelteKit frontend after backend smoke tests pass.

**Cross-Component Dependencies:**

- API response design depends on source metadata, data mode, and insufficient evidence model.
- RAG retrieval depends on documents/chunks schema and pgvector setup.
- LangGraph CRAG traceability depends on messages and retrieval_traces persistence.
- Frontend state display depends on backend returning citations, data mode, and insufficient evidence status.

## Implementation Patterns & Consistency Rules

이 단계의 목적은 이후 AI agents가 같은 구조와 스타일로 구현하도록 최소 규칙을 정하는 것이다.

### Naming Rules

- DB table, DB column, API JSON field, Python variable은 `snake_case`를 사용한다.
- Python class와 Pydantic schema class는 `PascalCase`를 사용한다.
- 예시:
  - `document_id`
  - `source_url`
  - `retrieval_trace_id`
  - `ChatRequest`
  - `ChatResponse`

### Backend Folder Rules

Backend는 다음 책임 경계를 따른다.

```text
backend/
  app/
    api/        # FastAPI routes
    core/       # config, logging, settings
    db/         # database engine/session setup
    models/     # SQLAlchemy models
    schemas/    # Pydantic request/response schemas
    ingestion/  # loaders, parsers, chunking
    rag/        # embeddings, retrieval, answer composition
    graph/      # LangGraph CRAG flow
    services/   # use-case coordination
  alembic/      # migrations
  tests/
```

Rules:

- Route handlers stay thin.
- Business logic belongs in `services/`, `rag/`, or `graph/`.
- SQLAlchemy models and Pydantic schemas stay separate.

### API Response Rules

Chat API responses should consistently include:

- `conversation_id`
- `message_id`
- `answer`
- `citations`
- `data_mode`
- `insufficient_evidence`
- `retrieval_trace_id`, if available

Errors should use a consistent shape:

```json
{
  "error": {
    "code": "unsupported_file_type",
    "message": "Human-readable message",
    "details": {}
  }
}
```

### Evidence and Safety Rules

- Insufficient evidence is a normal response state, not a server error.
- Unsupported document formats must be explicit errors, not silent skips.
- Source metadata must be preserved through ingestion, retrieval, answer generation, and API response.
- Official source URL, revision date, effective date, and legal/appraisal conclusions must not be fabricated.
- `data_mode` must be explicit, such as `sample`, `official`, `user_provided`, or `unknown`.

### Trace Rules

Retrieval traces should capture enough information to debug RAG behavior:

- original query
- rewritten query, if any
- retrieved chunk ids
- grading/relevance result
- insufficient evidence reason, if any

### Enforcement Guidelines

All implementation agents must follow these rules unless the architecture document is updated first.

Avoid:

- returning raw LangChain objects from API routes
- mixing SQLAlchemy models and Pydantic schemas in one file
- silently ignoring unsupported input
- treating “no relevant chunks found” as an exception
- generating fake official metadata

## Project Structure & Boundaries

### Complete Project Directory Structure

```text
langchain-property-appraiser/
├── README.md
├── .env.example
├── docker-compose.yml
├── docs/
│   ├── source-inventory.md
│   └── canonical-document-schema.md
├── sample_data/
│   ├── README.md
│   └── *.md
├── backend/
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── ingest.py
│   │   │   └── chat.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   │   ├── document.py
│   │   │   ├── chunk.py
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   ├── retrieval_trace.py
│   │   │   └── source_inventory.py
│   │   ├── schemas/
│   │   │   ├── common.py
│   │   │   ├── ingest.py
│   │   │   └── chat.py
│   │   ├── ingestion/
│   │   │   ├── loaders.py
│   │   │   ├── chunker.py
│   │   │   └── metadata.py
│   │   ├── rag/
│   │   │   ├── embeddings.py
│   │   │   ├── retriever.py
│   │   │   └── answer.py
│   │   ├── graph/
│   │   │   └── crag_graph.py
│   │   └── services/
│   │       ├── ingest_service.py
│   │       └── chat_service.py
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   ├── scripts/
│   │   ├── ingest_file.py
│   │   └── chat_once.py
│   └── tests/
└── frontend/
    └── # SvelteKit added after RAG Core validation
```

### Architectural Boundaries

**API Boundaries:**

- `app/api/` contains FastAPI route handlers only.
- Route handlers validate request/response shape and call services.
- REST endpoints start with `POST /ingest`, `POST /chat`, and `GET /conversations/{conversation_id}`.

**Service Boundaries:**

- `app/services/` coordinates use cases such as ingestion and chat.
- Services call `ingestion/`, `rag/`, `graph/`, and `db/` modules but should not contain low-level parsing or retrieval algorithms.

**RAG and Graph Boundaries:**

- `app/rag/` owns embeddings, retrieval, and answer composition.
- `app/graph/` owns LangGraph orchestration only.
- Retrieval, embedding, and answer logic should not be implemented directly inside `graph/`.

**Data Boundaries:**

- `app/models/` contains SQLAlchemy database models.
- `app/schemas/` contains Pydantic API schemas.
- `app/db/` contains engine/session/base setup.
- Alembic migrations live under `backend/alembic/`.

### Requirements to Structure Mapping

- Knowledge source management → `docs/source-inventory.md`, `app/models/source_inventory.py`
- Canonical document schema → `docs/canonical-document-schema.md`, `app/models/document.py`, `app/models/chunk.py`
- Ingestion → `app/ingestion/`, `app/services/ingest_service.py`, `app/api/ingest.py`
- Retrieval/RAG → `app/rag/`, `app/models/retrieval_trace.py`
- CRAG multi-turn chat → `app/graph/crag_graph.py`, `app/services/chat_service.py`, `app/api/chat.py`
- Conversations/messages → `app/models/conversation.py`, `app/models/message.py`
- Web chat UI → `frontend/`, added after backend smoke tests pass
- CLI smoke tests → `backend/scripts/ingest_file.py`, `backend/scripts/chat_once.py`
- Sample/test documents → `sample_data/`

### Integration Points

**Internal Communication:**

- API routes call services.
- Services coordinate DB access, ingestion, RAG, and graph modules.
- Graph nodes call reusable functions from `rag/` and services rather than duplicating logic.

**External Integrations:**

- PostgreSQL + pgvector runs through Docker Compose for local development.
- LLM and embedding providers are configured through environment variables.
- LangSmith is optional and enabled only when configured.

**Data Flow:**

1. Documents enter through CLI script or `POST /ingest`.
2. Ingestion loads, chunks, enriches metadata, embeds, and stores chunks.
3. Chat requests enter through CLI script or `POST /chat`.
4. LangGraph coordinates retrieval, grading, rewrite if needed, and answer generation.
5. API returns answer, citations, data mode, insufficient evidence state, and trace id.

### File Organization Patterns

**Configuration Files:**

- Root `.env.example` documents required environment variables.
- `docker-compose.yml` defines local PostgreSQL + pgvector.
- `backend/app/core/config.py` loads settings through `pydantic-settings`.

**Test Organization:**

- `backend/tests/` mirrors `backend/app/` where practical.
- RAG smoke tests should cover ingestion, retrieval with citations, insufficient evidence, and multi-turn context.

**Development Workflow Integration:**

- Backend RAG Core is validated first with `backend/scripts/` and API smoke tests.
- Frontend is added only after backend chat/ingestion paths work.
- Deployment structure remains deferred; local development is the first-class workflow for V1.

## Architecture Validation Results

### Coherence Validation

Architecture decisions are coherent.

- Backend-first FastAPI direction matches the PRD phase strategy.
- PostgreSQL + pgvector supports both relational RAG metadata and vector retrieval.
- SQLAlchemy + Alembic fits the PostgreSQL decision.
- Docker Compose fits local-first development with PostgreSQL/pgvector.
- SvelteKit is deferred until backend RAG Core is validated.
- LangGraph is isolated to orchestration while RAG logic remains reusable in `app/rag/`.

### Requirements Coverage Validation

Functional requirements are architecturally supported.

- Knowledge source management is covered by `source_inventory` and `docs/source-inventory.md`.
- Ingestion and retrieval are covered by `app/ingestion/`, `app/rag/`, documents/chunks models, and pgvector.
- Multi-turn CRAG is covered by `app/graph/`, conversations/messages models, and retrieval traces.
- Web chat is supported later through SvelteKit frontend and REST API.
- Safety requirements are supported through data mode, citations, insufficient evidence state, and no fabricated official metadata.
- Developer workflow is supported through CLI scripts, smoke tests, local logs, and optional LangSmith.

Non-functional requirements are mostly addressed.

- Security: secrets via env, no hardcoded keys, no real sensitive docs before policies.
- Reliability: unsupported input and insufficient evidence have explicit paths.
- Observability: retrieval traces, local logs, optional LangSmith.
- Maintainability: clear module boundaries.
- Usability: API response supports UI states.

### Implementation Readiness Validation

The architecture is ready to guide implementation with minor gaps.

- Critical stack decisions are made.
- Project structure is concrete.
- Naming and response patterns are defined.
- Component boundaries are clear.
- First implementation path is clear: backend skeleton, config, Docker Compose, DB models/migrations, ingestion, retrieval, chat API.

### Gap Analysis Results

**Minor gaps:**

- Embedding provider is configurable but not finally selected.
- Detailed SQLAlchemy column-level schema is not defined yet.
- Production deployment and CI/CD are deferred.
- Authentication and user accounts are deferred.
- Real user document retention/deletion policy is deferred.
- Official legal/regulatory ingestion is deferred.

No critical implementation-blocking gaps remain for the backend-first RAG Core phase.

### Important Implementation Cautions

- Keep the first implementation story small: PostgreSQL + pgvector, minimal migration, and sample document ingestion before full RAG behavior.
- Decide or document the backend Python version before implementation. The local environment reports Python 3.14, but Python 3.12 or 3.13 may be safer for package compatibility.
- Do not make a real embedding provider a hard blocker for the first story; allow mock/skip behavior when provider keys are absent.
- Use `sample_data/` first. Do not pull official legal/regulatory data into the first implementation slice.
- Preserve `citations`, `data_mode`, and `insufficient_evidence` in backend responses from the beginning because the later UI depends on them.

### Architecture Completeness Checklist

**Requirements Analysis**

- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**Architectural Decisions**

- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed for V1/local-first scope

**Implementation Patterns**

- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**Project Structure**

- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY WITH MINOR GAPS

**Confidence Level:** High for backend-first RAG Core implementation.

**Key Strengths:**

- Clear backend-first sequence
- PostgreSQL/pgvector chosen early
- Strong source metadata and traceability focus
- Explicit safety model for insufficient evidence and data mode
- Clean separation between API, service, RAG, graph, DB, and schema layers

**Areas for Future Enhancement:**

- Final embedding provider selection
- Detailed DB schema and indexes
- Authentication/user management
- Real document retention/deletion policy
- Official legal source ingestion
- Production deployment and monitoring

### Implementation Handoff

AI agents should:

- Follow the architecture document before making structural decisions.
- Keep FastAPI route handlers thin.
- Keep SQLAlchemy models and Pydantic schemas separate.
- Preserve source metadata through the full RAG pipeline.
- Treat insufficient evidence as a normal response state.
- Use PostgreSQL + pgvector through Docker Compose for local development.

**First Implementation Priority:**

Create the backend project skeleton, `.env.example`, Docker Compose for PostgreSQL + pgvector, `pydantic-settings` config, SQLAlchemy/Alembic setup, and initial model/migration placeholders.
