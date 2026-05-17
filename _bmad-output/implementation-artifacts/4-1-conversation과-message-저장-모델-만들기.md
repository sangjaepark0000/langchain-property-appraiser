# Story 4.1: Conversation과 Message 저장 모델 만들기

Status: review

## Story

As a 개발자,
I want conversation과 message를 저장하는 최소 DB 모델을 만들고 싶다,
so that 멀티턴 대화의 이전 질문과 답변 맥락을 추적할 수 있다.

## Acceptance Criteria

1. SQLAlchemy/Alembic 기반에서 `conversations`와 `messages` table이 migration으로 생성되고 각 message는 conversation에 연결된다.
2. conversation id가 없으면 새 conversation을 생성할 수 있고 생성된 conversation id가 응답/결과에 포함된다.
3. conversation id가 제공되면 해당 conversation에 message가 추가되고 이전 message history를 조회할 수 있다.

## Tasks / Subtasks

- [x] Conversation/Message SQLAlchemy 모델 추가
- [x] Alembic migration 추가
- [x] conversation service 추가
- [x] 새 conversation 생성/메시지 추가 구현
- [x] history 조회 구현
- [x] 테스트 추가

## Dev Notes

- API route 확장은 후속 Story 4.7 범위다.
- 현재는 service/model/migration 중심으로 구현한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 93 passed
- Docker PostgreSQL Alembic upgrade head → `conversations`, `messages`, version `20260517_0004` verified

### Completion Notes List

- Added Conversation and Message SQLAlchemy models with cascade relationship.
- Added Alembic migration for `conversations` and `messages`.
- Added conversation service for creating/appending messages and reading history.

### File List

- `backend/app/models/conversation.py`
- `backend/app/models/message.py`
- `backend/alembic/versions/20260517_0004_conversations_messages.py`
- `backend/alembic/env.py`
- `backend/app/services/conversation_service.py`
- `backend/tests/test_story_4_1_conversations.py`
