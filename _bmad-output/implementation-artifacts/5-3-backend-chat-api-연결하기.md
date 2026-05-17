# Story 5.3: Backend chat API 연결하기

Status: ready-for-dev

## Story

As a 사용자,
I want 웹 화면에서 질문을 보내고 backend RAG/CRAG 답변을 받고 싶다,
so that 검증된 RAG Core를 브라우저에서 사용할 수 있다.

## Acceptance Criteria

1. 질문 제출 시 frontend는 question과 conversation_id를 backend `POST /chat`에 전송하고 응답을 assistant 메시지로 표시한다.
2. 첫 질문에서 반환된 conversation_id를 저장하고 이후 후속 질문에 같은 conversation_id를 사용한다.
3. API 호출 실패 시 사용자에게 명확한 오류 상태를 표시하고 message list를 조용히 깨뜨리지 않는다.

## Tasks / Subtasks

- [ ] API client contract 강화
- [ ] page submit flow와 conversation id 유지 확인
- [ ] error 상태와 assistant 오류 메시지 처리
- [ ] tests 추가

## Dev Notes

- Keep static/simple; e2e can be added later.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
