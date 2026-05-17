# Story 4.2: Retrieval trace 저장 모델 만들기

Status: review

## Story

As a 개발자,
I want retrieval trace를 저장하는 모델을 만들고 싶다,
so that RAG/CRAG 실행 흐름과 근거 부족 원인을 디버깅할 수 있다.

## Acceptance Criteria

1. RAG/CRAG retrieval trace는 original query, retrieved chunk ids, relevance result, insufficient evidence reason을 기록하고 conversation/message와 연결될 수 있다.
2. query rewrite가 발생하면 rewritten query와 re-retrieval 결과를 기록하고 rewrite가 없으면 null로 명확히 표현한다.
3. trace debug/API summary는 검색 흐름을 이해할 수 있는 요약을 제공하고 민감한 사용자 원문을 과도하게 저장하지 않는 정책을 반영한다.

## Tasks / Subtasks

- [x] RetrievalTrace SQLAlchemy 모델 추가
- [x] Alembic migration 추가
- [x] trace service 추가
- [x] query redaction/summary 정책 추가
- [x] tests 추가

## Dev Notes

- Trace와 conversation/message 연결은 nullable로 두어 기존 RAG CLI/API도 사용 가능하게 한다.
- 원문 query 전체 저장 대신 query preview/hash를 저장한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 100 passed
- Docker PostgreSQL Alembic upgrade head → `retrieval_traces`, version `20260517_0006` verified

### Completion Notes List

- Added RetrievalTrace model and migration.
- Added trace service with query preview/hash policy instead of storing excessive raw query text.
- Supports optional conversation/message links, rewrite metadata, chunk ids, relevance result, insufficient evidence reason, and summary.

### File List

- `backend/app/models/retrieval_trace.py`
- `backend/alembic/versions/20260517_0006_retrieval_traces.py`
- `backend/alembic/env.py`
- `backend/app/services/retrieval_trace_service.py`
- `backend/tests/test_story_4_2_retrieval_trace.py`
