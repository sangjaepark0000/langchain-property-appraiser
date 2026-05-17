# Story 1.5: Source inventory와 canonical schema 문서 초안 만들기

Status: ready-for-dev

## Story

As a 개발자/운영자,
I want source inventory와 canonical document schema의 초기 문서 초안을 만들고 싶다,
so that supported, unsupported, sample, official, user-provided data를 처음부터 구분해 추적할 수 있다.

## Acceptance Criteria

1. Given repository documentation folder가 있다, When 문서 초안을 추가한다, Then `docs/source-inventory.md`와 `docs/canonical-document-schema.md`가 존재한다, And 각 문서는 목적과 예상 필드를 설명한다.
2. Given 아직 지원하지 않는 source가 있다, When source inventory에 기록한다, Then 해당 source를 unsupported 또는 deferred로 표시할 수 있다, And unsupported source가 조용히 ingested된 것처럼 처리되지 않는다.
3. Given data mode가 이후 RAG 답변에 중요하다, When canonical schema 문서 초안을 검토한다, Then `sample`, `official`, `user_provided`, `unknown` 같은 data mode 개념이 포함되어 있다.

## Tasks / Subtasks

- [ ] `docs/source-inventory.md` 작성 (AC: 1, 2)
  - [ ] 목적, 범위, source status 정의
  - [ ] supported/unsupported/deferred/ingested/failed 상태 설명
  - [ ] source별 예상 필드와 초기 inventory table 추가
  - [ ] unsupported/deferred가 성공 ingestion처럼 처리되지 않는 규칙 명시
- [ ] `docs/canonical-document-schema.md` 작성 (AC: 1, 3)
  - [ ] canonical document/chunk 개념 설명
  - [ ] 필수/선택 metadata 필드 정의
  - [ ] data mode: `sample`, `official`, `user_provided`, `unknown` 정의
  - [ ] lineage/citation 보존 규칙 명시
- [ ] 테스트 추가 (AC: 1, 2, 3)
  - [ ] 두 문서 존재 검증
  - [ ] 필수 status/data mode 용어 검증
  - [ ] unsupported/deferred silent ingestion 금지 문구 검증

## Dev Notes

### Architecture Guardrails

- Knowledge source management는 `docs/source-inventory.md`와 후속 `app/models/source_inventory.py`로 연결된다.
- Canonical document schema는 `docs/canonical-document-schema.md`와 후속 document/chunk model로 연결된다.
- `data_mode`는 명시적이어야 하며 `sample`, `official`, `user_provided`, `unknown` 등을 사용한다.
- Unsupported input은 silent skip 금지. 명시적 오류 또는 unsupported/deferred 상태로 기록해야 한다.

### Scope Boundaries

Do:
- 문서 초안과 문서 검증 테스트만 추가한다.

Do not:
- DB model/table, ingestion loader, parser, API를 구현하지 않는다.
- 실제 공식 법령/고시 데이터 ingestion을 구현하지 않는다.

## Dev Agent Record

### Agent Model Used

TBD by dev agent

### Debug Log References

### Completion Notes List

### File List
