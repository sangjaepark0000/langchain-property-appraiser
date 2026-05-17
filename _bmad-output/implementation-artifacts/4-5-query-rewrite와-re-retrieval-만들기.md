# Story 4.5: Query rewrite와 re-retrieval 만들기

Status: review

## Story

As a 사용자,
I want 검색 결과가 약할 때 시스템이 질문을 보정하고 다시 검색하길 원한다,
so that 한 번의 검색 실패로 바로 포기하지 않을 수 있다.

## Acceptance Criteria

1. retrieval grading 결과가 weak 또는 irrelevant면 원래 질문을 보존한 상태로 rewritten query가 생성되고 retrieval trace에 기록된다.
2. rewritten query로 re-retrieval을 실행하고 새 검색 결과가 retrieval trace에 기록되며 retry count는 설정된 제한을 넘지 않는다.
3. LLM provider key가 없으면 deterministic rewrite fallback 또는 rewrite skipped 상태를 사용하고 fallback/skipped 상태가 응답 또는 로그에 명확히 표시된다.

## Tasks / Subtasks

- [x] query rewrite provider/fallback 추가
- [x] RAG query re-retrieval orchestration 추가
- [x] retrieval trace rewritten fields 연결
- [x] retry limit 설정 추가
- [x] graph result/assistant metadata에 rewrite 상태 포함
- [x] tests 추가

## Dev Notes

- Real LLM rewrite는 후속 provider integration으로 두고 deterministic local fallback을 기본 사용한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 111 passed

### Completion Notes List

- Added deterministic query rewrite fallback preserving original query.
- RAG query now re-retrieves after weak/irrelevant initial grading within retry limit.
- Retrieval traces record rewritten query, re-retrieved chunk ids, rewrite status/fallback, and attempt count.
- Conversation graph exposes rewrite state and persists it in assistant message metadata.

### File List

- `backend/app/rag/rewrite.py`
- `backend/app/rag/query.py`
- `backend/app/graph/conversation.py`
- `backend/tests/test_story_4_5_query_rewrite.py`
