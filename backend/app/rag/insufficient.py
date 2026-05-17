from __future__ import annotations

from app.rag.safety import asks_for_determination, asks_for_official_data


def insufficient_evidence_reason(question: str, grading_reason: str | None = None) -> str:
    reasons: list[str] = []
    if grading_reason:
        reasons.append(grading_reason)
    if asks_for_official_data(question):
        reasons.append("official data is not available")
    if asks_for_determination(question):
        reasons.append("limited evidence-based assistance; not a legal conclusion or appraisal determination")
    if not reasons:
        reasons.append("retrieved evidence is insufficient")
    return "; ".join(dict.fromkeys(reasons))
