# Story 2.7: 공식/공개 데이터 source 조사와 수집 방식 기록하기

Status: review

## Story

As a 개발자/운영자,
I want 법령·고시 관련 공식/공개 데이터 source의 접근 방식과 제공 형식을 조사해 source inventory에 기록하고 싶다,
so that 실제 scraping 또는 API ingestion을 구현하기 전에 어떤 source를 우선 지원할지 판단할 수 있다.

## Acceptance Criteria

1. 각 source의 이름, URL, 접근 방식, 제공 형식, 인증/API key 필요 여부, 필수 metadata 제공 여부를 `docs/source-inventory.md`에 기록한다.
2. XML, HTML, JSON, PDF, DOCX, HWP, OCR 필요 여부를 구분하고 현재 MVP 미지원 형식은 `deferred` 또는 `unsupported`로 표시한다.
3. 공식 데이터가 아직 ingestion되지 않았음을 명확히 하며 sample/local data와 official data를 혼동하지 않는다.
4. 우선순위와 다음 구현에 필요한 loader/parser 작업이 명확히 드러난다.

## Research Sources

- 국가법령정보 공동활용 OPEN API: https://open.law.go.kr/LSO/openApi/guideList.do
- 국토교통부 감정평가 실무기준 고시 상세: https://www.molit.go.kr/USR/I0204/m_45/dtl.jsp?idx=17932
- 국토교통부 Open API 가이드라인: https://www.molit.go.kr/USR/WPGE0201/m_23746/DTL.jsp
- 공공데이터포털 국토교통부 개별공시지가정보: https://www.data.go.kr/data/15124014/openapi.do?recommendDataYn=Y

## Tasks / Subtasks

- [x] 공식 법령/API source 조사
- [x] 국토교통부 고시/행정규칙 source 조사
- [x] 공공데이터포털 부동산 공시가격 source 조사
- [x] source inventory 업데이트
- [x] 문서 테스트 추가

## Dev Notes

- 실제 scraping/API ingestion 구현은 하지 않는다.
- 공식 source는 아직 `ingested`로 표시하면 안 된다.

## Dev Agent Record

### Agent Model Used

TBD

### Debug Log References

- `cd backend && .venv/bin/pytest` → 55 passed

### Completion Notes List

- Researched official/public source candidates with minimal web search.
- Updated source inventory with access method, formats, auth/key expectation, priority, and next loader work.
- Kept official sources deferred, not ingested, to avoid confusing sample/local data with official data.

### File List

- `docs/source-inventory.md`
- `backend/tests/test_story_2_7_source_inventory_research.py`
