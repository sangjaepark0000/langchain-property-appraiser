from app.domain.safety_copy import (
    DOMAIN_PROHIBITED_TERMS,
    DomainSafetyContext,
    build_domain_safety_notice,
    build_missing_official_metadata_notice,
)


def test_domain_safety_notice_marks_response_as_reference_aid_only():
    notice = build_domain_safety_notice(DomainSafetyContext(topic="appraisal", data_mode="official"))

    assert "참고용 검토 보조" in notice
    assert "최종 법률 또는 전문 판단" in notice
    assert all(term not in notice for term in DOMAIN_PROHIBITED_TERMS)


def test_missing_official_metadata_notice_requires_source_confirmation_without_fabrication():
    notice = build_missing_official_metadata_notice(["source_url", "effective_date"])

    assert "출처 확인 필요" in notice
    assert "근거 부족" in notice
    assert "추가 자료 필요" in notice
    assert "source_url" in notice
    assert "effective_date" in notice
    assert "임의로 보완하지 않습니다" in notice


def test_domain_safety_notice_for_sample_data_does_not_look_official():
    notice = build_domain_safety_notice(DomainSafetyContext(topic="law", data_mode="sample", insufficient_evidence=True))

    assert "sample" in notice
    assert "official data로 간주하지 마세요" in notice
    assert "근거 부족" in notice
    assert all(term not in notice for term in DOMAIN_PROHIBITED_TERMS)
