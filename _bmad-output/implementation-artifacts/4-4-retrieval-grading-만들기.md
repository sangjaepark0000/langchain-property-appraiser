# Story 4.4: Retrieval grading 만들기

Status: review

## Story

As a 사용자,
I want 시스템이 검색 결과가 질문에 충분히 관련 있는지 평가하길 원한다,
so that 관련 없는 근거로 답변하지 않도록 할 수 있다.

## Acceptance Criteria

1. retriever chunk 후보를 sufficient, weak, irrelevant 또는 이에 준하는 상태로 평가하고 retrieval trace에 기록한다.
2. 충분한 검색 결과면 graph runtime은 answer composer로 진행하고 citations는 실제 retrieved chunk에서 생성된다.
3. 검색 결과가 약하거나 관련 없으면 query rewrite 또는 insufficient evidence 경로로 이동할 수 있고 server error로 처리하지 않는다.

## Tasks / Subtasks

- [x] retrieval grading module 추가
- [x] trace recording에 grading 결과 연결
- [x] graph runtime에 grading node 추가
- [x] weak/irrelevant path를 insufficient evidence로 안전 처리
- [x] tests 추가

## Dev Notes

- Query rewrite는 Story 4.5 범위라 여기서는 weak/irrelevant를 안전한 insufficient evidence 경로로 둔다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 107 passed

### Completion Notes List

- Added retrieval grading with sufficient/weak/irrelevant classifications.
- RAG query records retrieval trace with grading status, max score, and insufficient evidence reason.
- Conversation graph exposes grading and safely returns insufficient evidence for irrelevant retrieval.

### File List

- `backend/app/rag/grading.py`
- `backend/app/rag/query.py`
- `backend/app/graph/conversation.py`
- `backend/app/services/retrieval_trace_service.py`
- `backend/app/models/retrieval_trace.py`
- `backend/scripts/rag_query.py`
- `backend/tests/test_story_4_4_retrieval_grading.py`
