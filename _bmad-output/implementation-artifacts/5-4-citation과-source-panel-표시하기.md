# Story 5.4: Citation과 source panel 표시하기

Status: review

## Story

As a 사용자,
I want 답변의 출처와 근거 chunk를 확인하고 싶다,
so that 답변이 어떤 문서에 기반했는지 판단할 수 있다.

## Acceptance Criteria

1. API 응답 citations의 source name/path, chunk index, data mode를 표시하고 실제 응답 값만 사용한다.
2. citation metadata 일부가 `unknown`이면 unknown을 명확히 표시하고 없는 공식 URL/법령 metadata를 임의 생성하지 않는다.
3. 답변 본문과 citation 목록을 구분해 여러 citation을 확인하기 쉽게 표시한다.

## Tasks / Subtasks

- [x] Citation type 정리
- [x] CitationPanel component 추가
- [x] assistant message에 citations 연결
- [x] unknown fallback 표시
- [x] tests 추가

## Dev Notes

- No fabricated URLs/articles.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 133 passed

### Completion Notes List

- Added `CitationPanel` for source name/path, chunk index, and data mode.
- Assistant messages now carry citations from backend responses and render answer body separately from sources.
- Unknown citation fields are displayed as `unknown`; frontend does not fabricate official URLs/articles.

### File List

- `frontend/src/lib/components/CitationPanel.svelte`
- `frontend/src/lib/components/MessageList.svelte`
- `frontend/src/routes/+page.svelte`
- `backend/tests/test_story_5_4_frontend_citations.py`
