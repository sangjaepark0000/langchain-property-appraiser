# Story 5.4: Citation과 source panel 표시하기

Status: ready-for-dev

## Story

As a 사용자,
I want 답변의 출처와 근거 chunk를 확인하고 싶다,
so that 답변이 어떤 문서에 기반했는지 판단할 수 있다.

## Acceptance Criteria

1. API 응답 citations의 source name/path, chunk index, data mode를 표시하고 실제 응답 값만 사용한다.
2. citation metadata 일부가 `unknown`이면 unknown을 명확히 표시하고 없는 공식 URL/법령 metadata를 임의 생성하지 않는다.
3. 답변 본문과 citation 목록을 구분해 여러 citation을 확인하기 쉽게 표시한다.

## Tasks / Subtasks

- [ ] Citation type 정리
- [ ] CitationPanel component 추가
- [ ] assistant message에 citations 연결
- [ ] unknown fallback 표시
- [ ] tests 추가

## Dev Notes

- No fabricated URLs/articles.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
