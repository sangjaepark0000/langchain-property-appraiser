# Story 3.1: RAG smoke test용 sample knowledge fixture 만들기

Status: ready-for-dev

## Story

As a 개발자,
I want RAG 검색/답변 검증용 sample 문서 fixture를 만들고 싶다,
so that official data 없이도 RAG Core 동작을 안전하게 검증할 수 있다.

## Acceptance Criteria

1. `sample_data/`에 최소 2개 markdown 또는 txt 샘플 문서가 있고 각 문서는 테스트용 sample data임을 명확히 표시한다.
2. 샘플 문서는 검색과 답변 검증에 사용할 수 있는 명시적 사실을 포함하고 공식 법령/고시/실제 감정평가 검토 결과처럼 보이지 않는다.
3. smoke test 질문, 기대 답변 요지, 기대 citation/source path가 문서화되고 official data 없는 질문은 no evidence/insufficient evidence 기대값을 포함한다.

## Tasks / Subtasks

- [ ] sample knowledge 문서 2개 이상 추가
- [ ] sample disclaimer 명시
- [ ] expected Q&A fixture 문서/JSON 추가
- [ ] no evidence expectation 추가
- [ ] 테스트 추가

## Dev Notes

- 공식 법령/고시처럼 보이는 표현은 피한다.
- sample data만 사용하며 `data_mode=sample`을 명확히 유지한다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
