# Story 3.6: `POST /chat` 또는 `/query` 기본 RAG API 만들기

Status: ready-for-dev

## Story

As a 개발자/API 사용자,
I want 자연어 질문을 보내고 RAG 답변을 받을 수 있는 기본 API endpoint를 갖추고 싶다,
so that 이후 웹 UI와 CRAG runtime이 같은 응답 계약을 사용할 수 있다.

## Acceptance Criteria

1. `POST /query`는 answer, citations, data_mode, insufficient_evidence 여부를 포함한 재사용 가능한 응답 shape를 반환한다.
2. 잘못된 요청 payload는 일관된 error shape로 반환하고 route handler는 validation과 service 호출 중심으로 얇게 유지된다.
3. 관련 chunk가 없어도 HTTP server error가 아니라 정상 응답의 insufficient evidence 상태로 처리한다.

## Tasks / Subtasks

- [ ] request/response schema 추가
- [ ] API route 추가
- [ ] thin route + RAG service 호출
- [ ] validation error handler 추가
- [ ] insufficient evidence API 테스트 추가

## Dev Notes

- `/query`를 기본 endpoint로 구현한다.
- `/chat` alias는 후속 확장 가능하다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
