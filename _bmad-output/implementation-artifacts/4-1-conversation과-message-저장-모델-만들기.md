# Story 4.1: Conversation과 Message 저장 모델 만들기

Status: ready-for-dev

## Story

As a 개발자,
I want conversation과 message를 저장하는 최소 DB 모델을 만들고 싶다,
so that 멀티턴 대화의 이전 질문과 답변 맥락을 추적할 수 있다.

## Acceptance Criteria

1. SQLAlchemy/Alembic 기반에서 `conversations`와 `messages` table이 migration으로 생성되고 각 message는 conversation에 연결된다.
2. conversation id가 없으면 새 conversation을 생성할 수 있고 생성된 conversation id가 응답/결과에 포함된다.
3. conversation id가 제공되면 해당 conversation에 message가 추가되고 이전 message history를 조회할 수 있다.

## Tasks / Subtasks

- [ ] Conversation/Message SQLAlchemy 모델 추가
- [ ] Alembic migration 추가
- [ ] conversation service 추가
- [ ] 새 conversation 생성/메시지 추가 구현
- [ ] history 조회 구현
- [ ] 테스트 추가

## Dev Notes

- API route 확장은 후속 Story 4.7 범위다.
- 현재는 service/model/migration 중심으로 구현한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
