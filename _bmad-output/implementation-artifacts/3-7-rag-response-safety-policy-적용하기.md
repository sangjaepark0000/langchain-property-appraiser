# Story 3.7: RAG response safety policy 적용하기

Status: review

## Story

As a 사용자,
I want 시스템이 제공되지 않은 공식 법령 데이터나 업무 문서를 임의로 만들어 답하지 않기를 원한다,
so that sample/local data 기반 답변과 공식 검토 결과를 혼동하지 않을 수 있다.

## Acceptance Criteria

1. official data가 ingestion되어 있지 않은 상태에서 공식 법령 검토 질문을 하면 official data가 없음을 명확히 표시하고 공식 출처/개정일/시행일/조항을 임의 생성하지 않는다.
2. 법률 위반 여부나 감정평가 적정성을 단정적으로 묻는 경우 단정하지 않고 참고용/근거 기반 제한적 답변임을 표시한다.
3. citations는 실제 검색된 chunk metadata에서만 생성하고 없는 URL/source metadata를 만들어내지 않는다.

## Tasks / Subtasks

- [x] safety policy helper 추가
- [x] answer composer에 policy 적용
- [x] official/legal/appraisal 질문 감지
- [x] citation fabrication 방지 테스트
- [x] API 응답에도 policy 반영 확인

## Dev Notes

- LLM safety가 아니라 deterministic response guard로 구현한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 82 passed

### Completion Notes List

- Added deterministic RAG response safety policy.
- Official/legal/appraisal determination questions receive non-fabrication and limited-assistance notices.
- Citations remain based only on retrieved metadata.

### File List

- `backend/app/rag/safety.py`
- `backend/app/rag/answer.py`
- `backend/tests/test_story_3_7_rag_safety_policy.py`
