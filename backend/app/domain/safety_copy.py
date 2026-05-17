from __future__ import annotations

from dataclasses import dataclass


DOMAIN_PROHIBITED_TERMS = (
    "위법입니다",
    "적법합니다",
    "법적 책임이 있습니다",
    "감정평가가 부적정합니다",
    "확정 판정",
)


@dataclass(frozen=True)
class DomainSafetyContext:
    topic: str
    data_mode: str
    insufficient_evidence: bool = False


def build_domain_safety_notice(context: DomainSafetyContext) -> str:
    parts = [
        "이 응답은 참고용 검토 보조이며 최종 법률 또는 전문 판단이 아닙니다.",
        "법령·고시·감정평가 관련 결론은 원문과 전문가 검토로 확인하세요.",
        f"data_mode={context.data_mode}.",
    ]
    if context.data_mode != "official":
        parts.append(f"{context.data_mode} 자료는 official data로 간주하지 마세요.")
    if context.insufficient_evidence:
        parts.append("근거 부족 상태이므로 출처 확인 및 추가 자료가 필요합니다.")
    return " ".join(parts)


def build_missing_official_metadata_notice(missing_fields: list[str]) -> str:
    fields = ", ".join(missing_fields) if missing_fields else "unknown metadata"
    return (
        f"출처 확인 필요: {fields} metadata가 부족합니다. "
        "근거 부족 상태이며 추가 자료 필요. "
        "부족한 공식 metadata는 임의로 보완하지 않습니다."
    )
