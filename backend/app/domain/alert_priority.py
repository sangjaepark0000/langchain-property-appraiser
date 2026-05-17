from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AlertPriorityInput:
    relevance: str
    source_authority: str = "unknown"
    date_filter_matched: bool = False
    citation_count: int = 0
    date_field_used: str | None = None


@dataclass(frozen=True)
class AlertPriorityResult:
    level: str
    label: str
    confidence: str
    needs_review: bool
    reasons: list[str] = field(default_factory=list)
    explanation: str = ""
    source_authority: str = "unknown"
    date_field_used: str | None = None


def score_alert_priority(input_: AlertPriorityInput) -> AlertPriorityResult:
    score = 0
    reasons: list[str] = []
    if input_.relevance == "high":
        score += 3
        reasons.append("검색 근거의 관련도가 높습니다")
    elif input_.relevance == "medium":
        score += 2
        reasons.append("검색 근거의 관련도가 중간입니다")
    else:
        score += 0
        reasons.append("검색 근거의 관련도가 낮거나 불확실합니다")

    if input_.citation_count > 0:
        score += min(input_.citation_count, 2)
        reasons.append(f"출처 {input_.citation_count}개가 연결되었습니다")
    else:
        reasons.append("출처 근거가 부족합니다")

    if input_.source_authority != "unknown":
        score += 1
        reasons.append(f"출처 기관: {input_.source_authority}")
    else:
        reasons.append("출처 기관 metadata가 부족합니다")

    if input_.date_filter_matched:
        score += 1
        reasons.append(f"날짜 조건과 일치합니다 ({input_.date_field_used or 'date field unknown'})")
    else:
        reasons.append("날짜 조건 근거가 부족하거나 적용되지 않았습니다")

    if score >= 6:
        level = "high"
    elif score >= 3:
        level = "medium"
    else:
        level = "low"

    confidence = "medium" if input_.citation_count > 0 and input_.source_authority != "unknown" else "low"
    needs_review = confidence == "low"
    explanation = _build_explanation(level, confidence, needs_review, reasons)
    return AlertPriorityResult(
        level=level,
        label=f"작업 우선순위: {level}",
        confidence=confidence,
        needs_review=needs_review,
        reasons=reasons,
        explanation=explanation,
        source_authority=input_.source_authority,
        date_field_used=input_.date_field_used,
    )


def explain_alert_priority(result: AlertPriorityResult) -> str:
    reason_text = "; ".join(result.reasons)
    date_text = f" 날짜 조건 기준: {result.date_field_used}." if result.date_field_used else ""
    return (
        f"{result.label}로 표시한 이유: 검색 근거와 출처 metadata를 작업 우선순위 관점에서 종합했습니다. "
        f"검색 근거: {reason_text}.{date_text} "
        f"출처: {result.source_authority}. 이 표시는 최종 법률 또는 전문 판단이 아닙니다."
    )


def _build_explanation(level: str, confidence: str, needs_review: bool, reasons: list[str]) -> str:
    review = " 추가 확인 필요." if needs_review else " 전문가 검토로 최종 확인이 필요합니다."
    return (
        f"작업 우선순위 {level}, 신뢰도 {confidence}. "
        f"근거: {'; '.join(reasons)}. "
        "규정상 결론이 아니라 검토 순서 안내입니다."
        f"{review}"
    )
