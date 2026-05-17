# Story 6.2: 공식 source 후보 우선순위와 지원 상태 확정하기

Status: review

## Story

As a 개발자/운영자,
I want 공식/공개 법령·고시 source 후보의 우선순위와 지원 상태를 확정하고 싶다,
so that 어떤 source부터 ingestion 구현할지 결정할 수 있다.

## Acceptance Criteria

1. Epic 2.7 source inventory의 각 source에 priority, support status, access method, expected loader type을 기록한다.
2. unsupported/deferred source는 명확한 사유를 가진다.
3. 접근 안정성, 제공 형식, 필수 metadata 제공 여부, 구현 난이도를 기준으로 판단한다.
4. 실제 ingestion 대상 source가 최소 하나 이상 후보로 선정된다.
5. 수동 보완 가능성, 에이전트 한계, 사전 작업을 source별로 기록한다.
6. ingestion되지 않은 source는 official knowledge base에 포함된 것처럼 표시하지 않는다.

## Tasks / Subtasks

- [x] priority scoring rubric 추가
- [x] official source 후보별 priority/support status 확정
- [x] first loader target 선정
- [x] manual supplementation/agent limitation/prerequisite 기록
- [x] tests 추가

## Dev Notes

- Use existing source inventory facts; avoid costly web searches unless blocked.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 149 passed

### Completion Notes List

- Added official source prioritization rubric to source inventory.
- Ranked official source candidates and selected `official-law-open-api` as first_loader_target while keeping it deferred until loader/API validation.
- Recorded expected loader type, manual supplementation path, agent limitation, prerequisite work, and unsupported/deferred rationale for each candidate.
- Preserved rule that deferred official sources must not display as official knowledge base.

### File List

- `docs/source-inventory.md`
- `backend/tests/test_story_6_2_source_priority.py`
