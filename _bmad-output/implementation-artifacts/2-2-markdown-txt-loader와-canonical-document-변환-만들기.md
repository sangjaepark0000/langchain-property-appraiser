# Story 2.2: Markdown/TXT loader와 canonical document 변환 만들기

Status: ready-for-dev

## Story

As a 개발자,
I want markdown/txt 파일을 로딩해 canonical document schema로 변환하고 싶다,
so that 이후 chunking, embedding, retrieval이 동일한 입력 형식을 사용할 수 있다.

## Acceptance Criteria

1. Given markdown 또는 txt 파일이 있다, When loader를 실행한다, Then 파일 내용과 기본 metadata가 canonical document object로 변환된다, And source path, file name, file type, data mode가 포함된다.
2. Given 지원하지 않는 파일 형식이 입력된다, When loader를 실행한다, Then unsupported file type 오류가 명확하게 반환된다, And 해당 파일은 조용히 누락되거나 성공 처리되지 않는다.
3. Given loader/parser 확장이 필요하다, When 코드를 검토한다, Then 새로운 file type loader를 추가할 수 있는 구조가 분리되어 있다, And 기존 markdown/txt loader를 크게 변경하지 않아도 된다.

## Tasks / Subtasks

- [ ] CanonicalDocument schema/dataclass 추가
- [ ] markdown/txt loader 구현
- [ ] unsupported file type error 구현
- [ ] 확장 가능한 loader registry/factory 구조 구현
- [ ] 테스트 추가

## Dev Notes

- `docs/canonical-document-schema.md`의 fields와 data_mode를 따른다.
- Unsupported는 silent success 금지.
- DB 저장/ingestion service는 후속 story 범위다.

## Dev Agent Record

### Agent Model Used

TBD by dev agent

### Debug Log References

### Completion Notes List

### File List
