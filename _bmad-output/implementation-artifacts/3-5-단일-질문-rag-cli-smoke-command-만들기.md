# Story 3.5: 단일 질문 RAG CLI smoke command 만들기

Status: review

## Story

As a 개발자,
I want CLI에서 단일 자연어 질문을 실행해 RAG 결과를 확인하고 싶다,
so that 웹 UI 없이 ingestion부터 retrieval, answer까지 end-to-end로 검증할 수 있다.

## Acceptance Criteria

1. sample document가 ingestion되어 있을 때 CLI 질문은 retrieval, answer composition, citation 출력을 순서대로 실행하고 답변 텍스트와 참조 chunk 목록을 표시한다.
2. 검색 결과가 없을 때 명확한 no evidence/insufficient local evidence 메시지를 출력하고 답변을 만들어내지 않는다.
3. verbose/debug 옵션은 query, retrieved chunk count, selected citations, fallback 여부를 출력하고 secret 값은 출력하지 않는다.

## Tasks / Subtasks

- [x] ingestion persistence에 embedding metadata 저장 보강
- [x] RAG query service 추가
- [x] CLI smoke command 추가
- [x] no evidence 처리
- [x] verbose/debug 출력 테스트

## Dev Notes

- API endpoint는 Story 3.6 범위다.
- local fake embedding fallback을 사용한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 75 passed

### Completion Notes List

- Persisted embedding vectors into chunk metadata during ingestion.
- Added RAG query service wiring retriever, citation hydration, and answer composer.
- Added single-question CLI with answer, citations, insufficient evidence, and debug output.

### File List

- `backend/app/services/ingest_service.py`
- `backend/app/rag/query.py`
- `backend/scripts/ingest_file.py`
- `backend/scripts/rag_query.py`
- `backend/README.md`
- `backend/tests/test_story_3_5_rag_cli.py`
