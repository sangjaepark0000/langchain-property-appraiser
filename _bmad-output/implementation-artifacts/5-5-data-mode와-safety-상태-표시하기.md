# Story 5.5: Data mode와 safety 상태 표시하기

Status: ready-for-dev

## Story

As a 사용자,
I want 답변이 sample, official, user_provided 중 어떤 데이터에 기반했는지 보고 싶다,
so that 샘플 답변과 공식 검토 결과를 혼동하지 않을 수 있다.

## Acceptance Criteria

1. API 응답 data_mode를 눈에 띄게 표시하고 sample/unknown은 official answer처럼 보이지 않는다.
2. official data 없음/insufficient evidence 메시지는 backend 내용을 그대로 표시하고 공식 검토 결과로 오해될 표현을 추가하지 않는다.
3. 답변이 참고용 검토 보조임을 safety/data mode notice로 표시해 법률 위반/감정평가 적정성 단정처럼 보이지 않게 한다.

## Tasks / Subtasks

- [ ] DataModeNotice component 추가
- [ ] assistant message에 data_mode/insufficient evidence metadata 연결
- [ ] sample/unknown notice와 safety notice 표시
- [ ] tests 추가

## Dev Notes

- Do not invent official status.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
