# Story 6.3: 첫 official source loader/parser 구현하기

Status: review

## Story

As a 개발자,
I want 우선순위가 높은 official source 하나에 대한 loader/parser를 구현하고 싶다,
so that 실제 공식/공개 데이터를 canonical document schema로 변환할 수 있다.

## Acceptance Criteria

1. 우선순위 source `official-law-open-api`의 XML 형식을 읽어 canonical document로 변환하고 source authority, source URL, 수집일, domain metadata를 포함한다.
2. source 구조가 예상과 다르면 명확한 오류 또는 failed status를 기록하고 partial/invalid data를 official data로 조용히 저장하지 않는다.
3. 필수 metadata가 부족하면 unknown/null로 표시하고 개정일, 시행일, 조항, 출처 URL을 임의 생성하지 않는다.
4. live API credential 없이도 recorded/local XML fixture로 테스트 가능하며, API key 연결은 사전 작업으로 남긴다.

## Tasks / Subtasks

- [x] official law XML parser 추가
- [x] loader registry XML 등록
- [x] invalid XML/shape failure 처리
- [x] missing metadata unknown/null 처리
- [x] fixtures/tests 추가

## Dev Notes

- Do not live-call official API in tests.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 153 passed

### Completion Notes List

- Added official law XML loader/parser for recorded/local XML fixtures.
- Registered `.xml` loader and maps official-law-open-api style XML to CanonicalDocument with `domain_metadata`.
- Invalid XML shape raises explicit parse error rather than partial official ingestion.
- Missing metadata remains `unknown`/null; source URL/dates/articles are not fabricated.
- Live API credentials remain prerequisite work, not required for tests.

### File List

- `backend/app/ingestion/official_law.py`
- `backend/app/ingestion/loaders.py`
- `backend/tests/test_story_6_3_official_law_loader.py`
- `backend/tests/fixtures/official_law/sample_law.xml`
- `backend/tests/fixtures/official_law/missing_metadata.xml`
- `backend/tests/fixtures/official_law/invalid_shape.xml`
