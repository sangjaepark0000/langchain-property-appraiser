# Story 3.3: Citation과 source metadata 포함 검색 결과 만들기

Status: review

## Story

As a 개발자,
I want 검색 결과에 citation과 source metadata를 포함하고 싶다,
so that 답변이 어떤 문서와 chunk에 근거하는지 추적할 수 있다.

## Acceptance Criteria

1. 검색 결과 변환 시 source path/name, data mode, chunk index, document id, chunk id가 포함되고 answer generation citation으로 사용할 수 있다.
2. 누락 metadata는 `unknown` 또는 명확한 fallback으로 표시하고 존재하지 않는 공식 출처 URL/법령 metadata를 임의 생성하지 않는다.
3. sample data 검색 결과는 data mode가 `sample` 또는 설정값으로 명확히 표시되고 official data처럼 보이지 않는다.

## Tasks / Subtasks

- [x] Citation/source metadata result schema 추가
- [x] retriever 결과 hydration/serialization 구현
- [x] metadata fallback 처리
- [x] sample data mode 명시 테스트

## Dev Notes

- API route는 아직 추가하지 않고 RAG layer serializer로 구현한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 67 passed

### Completion Notes List

- Added RAG-layer citation hydration for retrieval results.
- Included source path/name/url, data mode, chunk index, document id, chunk id.
- Added unknown fallbacks and explicit `is_official` flag without fabricating official URLs.

### File List

- `backend/app/rag/citations.py`
- `backend/tests/test_story_3_3_retrieval_citations.py`
