# Story 5.2: Chat input과 message list 만들기

Status: ready-for-dev

## Story

As a 사용자,
I want 자연어 질문을 입력하고 대화 메시지를 볼 수 있다,
so that 버튼 중심 workflow 없이 챗봇과 대화할 수 있다.

## Acceptance Criteria

1. 질문 입력/제출 시 사용자 메시지가 message list에 표시되고 입력창은 다음 질문 준비 상태가 된다.
2. Enter 또는 명확한 제출 동작으로 질문이 전송되고 빈 질문은 전송되지 않는다.
3. 여러 turn에서 사용자 메시지와 assistant 응답을 구분해 읽기 쉬운 순서로 표시한다.

## Tasks / Subtasks

- [ ] ChatInput component 추가
- [ ] MessageList component 추가
- [ ] page에서 component 조합
- [ ] empty submit guard와 reset 유지
- [ ] tests 추가

## Dev Notes

- Backend integration remains simple; richer API behavior continues in Story 5.3.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
