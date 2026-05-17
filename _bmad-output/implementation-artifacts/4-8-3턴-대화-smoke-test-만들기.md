# Story 4.8: 3턴 대화 smoke test 만들기

Status: review

## Story

As a 개발자,
I want 최소 3턴 이상의 멀티턴 CRAG smoke test를 만들고 싶다,
so that conversation state, retrieval grading, rewrite, insufficient evidence 흐름을 검증할 수 있다.

## Acceptance Criteria

1. sample fixture 문서를 ingestion한 뒤 3턴 smoke test는 첫 질문, 후속 질문, 맥락 참조 질문을 같은 conversation에서 처리하고 각 turn의 message/trace를 확인한다.
2. 한 turn에서 검색 결과 부족 시 query rewrite, re-retrieval, 또는 insufficient evidence 경로 중 하나를 검증하고 없는 공식 데이터를 만들어내지 않는다.
3. LangSmith 설정 없이 local logs와 retrieval trace만으로 주요 graph 흐름을 확인할 수 있고 외부 tracing 설정 없이 통과한다.

## Tasks / Subtasks

- [x] multi-turn smoke script 추가
- [x] sample ingestion + 3 chat calls 자동화
- [x] messages/traces 검증
- [x] insufficient/rewrite path 검증
- [x] README 문서화
- [x] tests 추가

## Dev Notes

- SQLite + local fallback providers only.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 120 passed

### Completion Notes List

- Added `scripts/multiturn_smoke.py` for local 3-turn CRAG smoke.
- Smoke ingests sample fixture, runs `/chat` for three turns in one conversation, verifies 6 messages and 3 retrieval traces.
- Smoke validates insufficient evidence/rewrite path without LangSmith or fabricated official legal sources.

### File List

- `backend/scripts/multiturn_smoke.py`
- `backend/tests/test_story_4_8_multiturn_smoke.py`
- `backend/README.md`
