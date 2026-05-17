# Story 3.2: Vector retrieval 기본 검색 만들기

Status: review

## Story

As a 개발자,
I want 저장된 chunk를 자연어 query로 검색할 수 있는 retriever를 만들고 싶다,
so that RAG 답변 생성 전에 관련 근거 chunk를 찾을 수 있다.

## Acceptance Criteria

1. ingestion된 document와 chunk가 있을 때 자연어 query로 관련 chunk 후보 목록을 반환하고 각 결과에는 chunk id, document id, score/relevance indicator가 포함된다.
2. vector embedding이 저장되어 있을 때 configured vector search 방식을 사용하고 검색 로직은 `rag/` 계층에 위치한다.
3. 검색 결과가 없을 때 빈 결과를 명확히 반환하고 서버 오류로 처리하지 않는다.

## Tasks / Subtasks

- [x] Retrieval result schema 추가
- [x] cosine similarity 기반 configured vector retriever 추가
- [x] stored chunk metadata embedding 지원
- [x] empty result 처리
- [x] 테스트 추가

## Dev Notes

- pgvector column migration은 후속 최적화로 두고, 현재는 `chunks.metadata.embedding`에 저장된 벡터를 읽는 configured vector search fallback을 구현한다.
- API route는 추가하지 않는다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 63 passed

### Completion Notes List

- Added RAG-layer vector retriever using configured vector search over stored chunk metadata embeddings.
- Added cosine similarity, relevance labels, result schema, and empty-result handling.
- Avoided schema migration by reading vectors from `chunks.metadata.embedding`.

### File List

- `backend/app/rag/retriever.py`
- `backend/tests/test_story_3_2_retriever.py`
