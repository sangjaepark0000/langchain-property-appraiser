# Story 4.7: Multi-turn chat API contract 확장하기

Status: review

## Story

As a 개발자/API 사용자,
I want chat API가 conversation id와 retrieval trace summary를 포함하길 원한다,
so that 웹 UI와 디버깅 도구가 멀티턴 상태와 CRAG 흐름을 사용할 수 있다.

## Acceptance Criteria

1. `POST /chat` 신규 질문은 새 conversation_id, message_id, answer를 반환한다.
2. 기존 conversation_id 후속 질문은 같은 conversation에 message를 추가하고 이전 맥락을 반영할 수 있다.
3. 응답에는 answer, citations, data_mode, insufficient_evidence, retrieval_trace_id 또는 trace summary가 포함되고 frontend가 사용할 일관된 shape를 유지한다.

## Tasks / Subtasks

- [x] chat request/response schema 추가
- [x] /chat route 추가
- [x] conversation graph 호출 연결
- [x] message_id/trace summary 반환
- [x] tests 추가

## Dev Notes

- 기존 `/query` contract는 유지한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 118 passed

### Completion Notes List

- Added POST /chat multi-turn API contract.
- New chat requests return conversation_id, user message_id, answer, citations, data_mode, insufficient evidence fields, and retrieval trace summary.
- Follow-up requests append to existing conversation.

### File List

- `backend/app/schemas/chat.py`
- `backend/app/api/routes.py`
- `backend/tests/test_story_4_7_chat_api.py`
