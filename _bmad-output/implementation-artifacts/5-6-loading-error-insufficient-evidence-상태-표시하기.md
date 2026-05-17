# Story 5.6: Loading, error, insufficient evidence 상태 표시하기

Status: ready-for-dev

## Story

As a 사용자,
I want 질문 처리 중, 오류, 근거 부족 상태를 명확히 알고 싶다,
so that 시스템이 멈췄는지, 실패했는지, 근거가 부족한지 구분할 수 있다.

## Acceptance Criteria

1. backend 응답 대기 중 loading 상태가 표시된다.
2. insufficient_evidence 응답은 서버 오류/빈 답변이 아니라 근거 부족 상태로 명확히 표시된다.
3. API error는 이해 가능한 오류 메시지를 보여주고 다시 시도 가능한 상태로 유지한다.

## Tasks / Subtasks

- [ ] StatusPanel component 추가
- [ ] loading/error/insufficient 상태 enum 또는 문자열 관리
- [ ] page status flow 정리
- [ ] tests 추가

## Dev Notes

- Avoid confusing insufficient evidence with transport/server errors.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
