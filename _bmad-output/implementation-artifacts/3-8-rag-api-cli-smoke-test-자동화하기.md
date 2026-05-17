# Story 3.8: RAG API/CLI smoke test 자동화하기

Status: review

## Story

As a 개발자,
I want RAG Core의 기본 흐름을 자동 smoke test로 검증하고 싶다,
so that 이후 CRAG와 웹 UI 구현 전에 regression을 줄일 수 있다.

## Acceptance Criteria

1. sample data와 local fallback provider로 sample ingestion, retrieval, answer composition, citation generation 흐름을 외부 key 없이 검증한다.
2. 검색 근거가 없는 질문은 insufficient evidence/no evidence를 검증하고 hallucinated official answer가 생성되지 않음을 확인한다.
3. API response contract는 answer, citations, data_mode, insufficient_evidence 필드를 검증해 frontend/CRAG가 신뢰할 수 있게 한다.

## Tasks / Subtasks

- [x] automated RAG smoke script 추가
- [x] CLI path smoke 검증
- [x] API contract smoke 검증
- [x] no evidence smoke 검증
- [x] README 문서화

## Dev Notes

- 외부 LLM/embedding key 없이 sqlite와 fake fallback만 사용한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 84 passed
- `python scripts/rag_smoke.py --database-url sqlite+pysqlite:///...` covered by test

### Completion Notes List

- Added automated RAG smoke script covering sample ingestion, CLI query, API contract, no evidence, and official hallucination checks.
- Smoke flow runs with sqlite and local fallback providers, no external keys.
- Documented smoke command.

### File List

- `backend/scripts/rag_smoke.py`
- `backend/app/rag/retriever.py`
- `backend/README.md`
- `backend/tests/test_story_3_8_rag_smoke.py`
