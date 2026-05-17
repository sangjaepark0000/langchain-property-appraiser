# Story 3.4: 근거 기반 answer composer 만들기

Status: review

## Story

As a 사용자,
I want 검색된 근거 chunk를 바탕으로 답변을 받고 싶다,
so that 답변 내용과 근거를 함께 확인할 수 있다.

## Acceptance Criteria

1. sample 문서 근거 chunk로 답변 텍스트를 생성하고 응답에는 citations와 data mode가 포함된다.
2. LLM provider 설정 시 provider abstraction을 통해 답변을 생성하며 provider-specific 코드는 API route에 섞이지 않는다.
3. LLM provider key가 없으면 deterministic fallback/extractive summary를 반환하고 fallback 상태를 명확히 표시한다.
4. sample/local data 기반 답변은 공식 법령 검토 결과처럼 표현하지 않고 sample/local 기반임을 명확히 표시한다.

## Tasks / Subtasks

- [x] answer result schema 추가
- [x] LLM provider protocol/fallback 추가
- [x] extractive answer composer 추가
- [x] citations/data mode 포함
- [x] insufficient evidence 처리
- [x] 테스트 추가

## Dev Notes

- API route는 후속 Story 3.6 범위다.
- LLM 없는 local smoke mode를 기본 동작으로 둔다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 71 passed

### Completion Notes List

- Added answer provider abstraction and deterministic extractive fallback.
- Added AnswerResult with citations, data mode, official flag, provider, and fallback status.
- Added insufficient evidence response and sample/local answer labeling.

### File List

- `backend/app/rag/answer.py`
- `backend/tests/test_story_3_4_answer_composer.py`
