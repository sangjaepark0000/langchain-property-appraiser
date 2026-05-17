# Story 4.6: Insufficient evidence 응답 경로 만들기

Status: review

## Story

As a 사용자,
I want 근거가 부족할 때 시스템이 모른다고 말하길 원한다,
so that 없는 근거로 그럴듯한 답변을 받지 않는다.

## Acceptance Criteria

1. initial retrieval과 re-retrieval 후에도 근거가 충분하지 않으면 insufficient evidence 상태의 정상 응답을 반환하고 HTTP/server error로 처리하지 않는다.
2. official data가 없을 때 공식 법령/고시 검토 질문은 공식 데이터 부재를 명확히 표시하고 공식 출처/개정일/시행일/조항을 임의 생성하지 않는다.
3. 법률 위반/감정평가 적정성 단정 질문은 단정하지 않고 참고용 검토 보조/추가 자료 필요 상태로 응답하며 이유가 trace summary 또는 response message에 남는다.

## Tasks / Subtasks

- [x] insufficient evidence policy/result detail 추가
- [x] RAG query/graph 응답에 reason 노출
- [x] trace summary에 insufficient evidence details 기록
- [x] API/CLI 정상 응답 검증
- [x] tests 추가

## Dev Notes

- Safety policy는 deterministic guard를 유지한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 115 passed

### Completion Notes List

- Added insufficient evidence reason policy for official/domain determination questions.
- RAG query, graph result, trace summary, and API response expose insufficient evidence reason.
- Official/legal/appraisal insufficient paths return normal responses without fabricated sources/articles/dates.

### File List

- `backend/app/rag/insufficient.py`
- `backend/app/rag/query.py`
- `backend/app/graph/conversation.py`
- `backend/app/schemas/query.py`
- `backend/app/api/routes.py`
- `backend/tests/test_story_4_6_insufficient_evidence.py`
