# Story 5.7: 3턴 웹 채팅 smoke test 만들기

Status: review

## Story

As a 개발자,
I want 웹 UI에서 최소 3턴 대화를 검증하고 싶다,
so that backend CRAG conversation runtime이 frontend와 연결되어 동작하는지 확인할 수 있다.

## Acceptance Criteria

1. backend/frontend local flow에서 sample fixture 기반 3턴 이상 대화가 같은 conversation_id로 이어지고 각 turn의 사용자/assistant 메시지가 확인된다.
2. citations와 data_mode가 화면 표시 계약에 포함되고 sample data가 official data처럼 보이지 않는다.
3. 근거 없는 질문에서 insufficient evidence가 명확히 표시되고 hallucinated official answer를 보여주지 않는다.

## Tasks / Subtasks

- [x] web chat smoke script 추가
- [x] backend 3-turn flow와 frontend contract files 함께 검증
- [x] citations/data mode/insufficient UI contract 검증
- [x] README 문서화
- [x] tests 추가

## Dev Notes

- Avoid requiring browser automation dependency until frontend package lock/test stack is introduced.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 141 passed

### Completion Notes List

- Added `scripts/web_chat_smoke.py` combining backend 3-turn `/chat` flow with frontend contract validation.
- Smoke verifies same conversation_id, user/assistant message persistence, citations/data mode/insufficient UI contracts, and no fabricated official answer.
- Documented smoke command in frontend README without adding browser automation dependency.

### File List

- `backend/scripts/web_chat_smoke.py`
- `backend/tests/test_story_5_7_web_chat_smoke.py`
- `frontend/README.md`
