from app.domain.alert_priority import AlertPriorityInput, explain_alert_priority, score_alert_priority


def test_alert_level_is_work_priority_not_legal_judgment():
    result = score_alert_priority(
        AlertPriorityInput(relevance="high", source_authority="국가법령정보센터", date_filter_matched=True, citation_count=2)
    )

    assert result.level == "high"
    assert result.label == "작업 우선순위: high"
    assert result.confidence == "medium"
    forbidden = ["위법", "적법", "법적 책임", "확정 판단"]
    assert all(term not in result.explanation for term in forbidden)
    assert "전문가 검토" in result.explanation


def test_alert_priority_requires_more_review_when_basis_is_weak():
    result = score_alert_priority(AlertPriorityInput(relevance="low", source_authority="unknown", date_filter_matched=False, citation_count=0))

    assert result.level == "low"
    assert result.confidence == "low"
    assert result.needs_review is True
    assert "추가 확인 필요" in result.explanation
    assert "확정" not in result.explanation


def test_explain_why_high_uses_evidence_date_and_source_reasons():
    result = score_alert_priority(
        AlertPriorityInput(
            relevance="high",
            source_authority="국가법령정보센터",
            date_filter_matched=True,
            citation_count=3,
            date_field_used="revision_date",
        )
    )

    explanation = explain_alert_priority(result)

    assert "검색 근거" in explanation
    assert "revision_date" in explanation
    assert "국가법령정보센터" in explanation
    assert "최종 법률 또는 전문 판단이 아닙니다" in explanation
