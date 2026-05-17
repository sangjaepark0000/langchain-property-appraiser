from __future__ import annotations

OFFICIAL_QUERY_TERMS = (
    "official",
    "regulation",
    "article",
    "law",
    "법령",
    "고시",
    "국토교통부",
    "조항",
    "시행일",
)
DETERMINATION_TERMS = (
    "legally valid",
    "legal violation",
    "appropriate",
    "적법",
    "위반",
    "적정",
    "타당",
)


def asks_for_official_data(question: str) -> bool:
    lowered = question.lower()
    return any(term.lower() in lowered for term in OFFICIAL_QUERY_TERMS)


def asks_for_determination(question: str) -> bool:
    lowered = question.lower()
    return any(term.lower() in lowered for term in DETERMINATION_TERMS)


def apply_response_safety_policy(question: str, answer: str, evidence: list[dict]) -> str:
    data_modes = {item.get("data_mode", "unknown") for item in evidence}
    has_official = "official" in data_modes
    notices: list[str] = []
    if asks_for_official_data(question) and not has_official:
        notices.append(
            "Official data is not available in the retrieved evidence; no official source, article, effective date, or revision date is asserted."
        )
    if asks_for_determination(question):
        notices.append(
            "This is limited evidence-based assistance, not a legal conclusion or appraisal appropriateness determination."
        )
    if not notices:
        return answer
    return answer + " " + " ".join(notices)
