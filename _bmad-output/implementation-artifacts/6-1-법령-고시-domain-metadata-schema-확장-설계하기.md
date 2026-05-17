# Story 6.1: 법령·고시 domain metadata schema 확장 설계하기

Status: ready-for-dev

## Story

As a 개발자,
I want 법령·고시 데이터에 필요한 domain metadata schema를 설계하고 싶다,
so that 향후 official source ingestion 시 개정일, 시행일, 조항, 출처를 구조적으로 저장할 수 있다.

## Acceptance Criteria

1. 법령명/자료명, 조항, 개정일, 시행일, 수집일, 출처 URL, source authority 필드를 정의하고 기존 sample/local document schema와 호환된다.
2. 작성일, 수집일, 개정일, 시행일, 평가기준일을 혼동하지 않도록 의미를 문서화한다.
3. 누락 값은 unknown 또는 null로 표현하고 시스템이 누락된 공식 metadata를 임의 생성하지 않는다.
4. 수동 보완 가능성, 현재 에이전트만으로 어려운 점, 사전 작업으로 해소 가능한 점을 문서화한다.

## Tasks / Subtasks

- [ ] domain metadata schema 문서 추가
- [ ] canonical document schema와 연결
- [ ] missing metadata/fabrication 금지 규칙 명시
- [ ] manual supplementation / agent limitation / prerequisite notes 추가
- [ ] tests 추가

## Dev Notes

- Do not add DB columns in this story unless needed; schema contract first.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
