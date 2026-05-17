# Story 5.5: Data mode와 safety 상태 표시하기

Status: review

## Story

As a 사용자,
I want 답변이 sample, official, user_provided 중 어떤 데이터에 기반했는지 보고 싶다,
so that 샘플 답변과 공식 검토 결과를 혼동하지 않을 수 있다.

## Acceptance Criteria

1. API 응답 data_mode를 눈에 띄게 표시하고 sample/unknown은 official answer처럼 보이지 않는다.
2. official data 없음/insufficient evidence 메시지는 backend 내용을 그대로 표시하고 공식 검토 결과로 오해될 표현을 추가하지 않는다.
3. 답변이 참고용 검토 보조임을 safety/data mode notice로 표시해 법률 위반/감정평가 적정성 단정처럼 보이지 않게 한다.

## Tasks / Subtasks

- [x] DataModeNotice component 추가
- [x] assistant message에 data_mode/insufficient evidence metadata 연결
- [x] sample/unknown notice와 safety notice 표시
- [x] tests 추가

## Dev Notes

- Do not invent official status.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 136 passed

### Completion Notes List

- Added data mode/safety notice for assistant responses.
- Assistant messages carry backend data_mode and insufficient evidence reason.
- sample/unknown data is explicitly marked as not an official determination/reference aid only.

### File List

- `frontend/src/lib/components/DataModeNotice.svelte`
- `frontend/src/lib/components/MessageList.svelte`
- `frontend/src/routes/+page.svelte`
- `backend/tests/test_story_5_5_frontend_data_mode_safety.py`
