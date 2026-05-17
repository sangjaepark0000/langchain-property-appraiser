# Story 4.3: LangGraph conversation state 기본 흐름 만들기

Status: review

## Story

As a 개발자,
I want LangGraph 기반 conversation state 흐름을 만들고 싶다,
so that 멀티턴 질문에서 이전 대화 맥락을 사용할 수 있다.

## Acceptance Criteria

1. 첫 질문 실행 시 conversation state가 생성되고 user message가 기록되며 기존 RAG retriever/answer composer를 재사용해 응답을 생성한다.
2. conversation id가 제공된 후속 질문 실행 시 이전 message history를 state에 포함하고 같은 conversation에 message를 추가한다.
3. 주요 node transition과 상태 요약이 local logging에 남고 LangSmith 없이도 local debugging이 가능하다.

## Tasks / Subtasks

- [x] Conversation graph state schema 추가
- [x] LangGraph runtime 구성
- [x] message history 로드/기록 노드 추가
- [x] RAG query 재사용 노드 추가
- [x] local transition logging 추가
- [x] tests 추가

## Dev Notes

- API contract 확장은 Story 4.7 범위다.
- 현재는 service/runtime 계층으로 구현한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 103 passed

### Completion Notes List

- Added LangGraph conversation runtime with start, load_history, rag_answer, and persist_assistant nodes.
- First question creates conversation and records user/assistant messages.
- Follow-up question loads prior history and appends messages to the existing conversation.
- Added local node transition logging without LangSmith dependency.

### File List

- `backend/app/graph/__init__.py`
- `backend/app/graph/conversation.py`
- `backend/tests/test_story_4_3_conversation_graph.py`
