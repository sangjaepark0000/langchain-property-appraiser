# Story 6.7: Domain safety policy와 response copy 정리하기

Status: ready-for-dev

## Story

As a 사용자,
I want 법령·감정평가 관련 답변이 참고용 검토 보조임을 명확히 알 수 있다,
so that 시스템 응답을 최종 법률·전문 판단으로 오해하지 않는다.

## Acceptance Criteria

1. 법령·고시/감정평가 질문 답변은 참고용 검토 보조임을 명확히 표현하고 법률 위반/적법성/감정평가 적정성을 단정하지 않는다.
2. official source metadata가 부족하면 출처 확인 필요, 근거 부족, 추가 자료 필요 상태를 명확히 표시하고 부족한 정보를 보완하지 않는다.
3. domain response copy가 여러 화면/API에서 쓰일 수 있도록 재사용 가능한 policy/copy module과 문서로 정리된다.

## Tasks / Subtasks

- [ ] reusable domain safety copy module 추가
- [ ] official metadata 부족 copy 추가
- [ ] prohibited language tests 추가
- [ ] docs 추가

## Dev Notes

- Centralize copy so frontend/API can reuse later.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
