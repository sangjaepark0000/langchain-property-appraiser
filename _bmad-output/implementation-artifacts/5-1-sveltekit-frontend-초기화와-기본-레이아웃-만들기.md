# Story 5.1: SvelteKit frontend 초기화와 기본 레이아웃 만들기

Status: ready-for-dev

## Story

As a 사용자,
I want 웹 브라우저에서 챗봇 화면에 접근하고 싶다,
so that CLI/API 없이 RAG 챗봇을 사용할 수 있다.

## Acceptance Criteria

1. `frontend/` SvelteKit 앱이 생성되고 local development 실행 방법이 문서화된다.
2. 기본 페이지는 채팅 중심 레이아웃을 표시하고 메시지 목록, 입력 영역, 상태 표시 영역이 구분되어 있다.
3. V1에 불필요한 복잡한 global state management가 도입되지 않고 backend API 호출을 위한 단순한 구조를 가진다.

## Tasks / Subtasks

- [ ] SvelteKit frontend skeleton 추가
- [ ] 기본 chat layout 구현
- [ ] 단순 API client 구조 추가
- [ ] dev docs 추가
- [ ] tests 추가

## Dev Notes

- Keep frontend minimal.
- Prefer native Svelte state; no external global state manager.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

### Completion Notes List

### File List
