from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AnswerProviderResult:
    answer: str
    provider: str
    fallback: bool = False


class AnswerProvider(Protocol):
    name: str

    def generate(self, question: str, evidence: list[dict]) -> AnswerProviderResult:
        ...


@dataclass(frozen=True)
class AnswerResult:
    answer: str
    status: str
    provider: str
    fallback: bool
    citations: list[dict]
    data_mode: str
    is_official: bool


class ExtractiveFallbackAnswerProvider:
    name = "extractive-fallback"

    def generate(self, question: str, evidence: list[dict]) -> AnswerProviderResult:
        evidence_text = " ".join(item.get("text", "") for item in evidence).strip()
        if not evidence_text:
            return AnswerProviderResult(
                answer="Insufficient evidence in the available local/sample context.",
                provider=self.name,
                fallback=True,
            )
        data_modes = {item.get("data_mode", "unknown") for item in evidence}
        prefix = "Based on sample/local data, " if "sample" in data_modes else "Based on retrieved evidence, "
        return AnswerProviderResult(answer=prefix + evidence_text, provider=self.name, fallback=True)


def _resolve_data_mode(evidence: list[dict]) -> str:
    modes = [item.get("data_mode") or "unknown" for item in evidence]
    if not modes:
        return "unknown"
    unique_modes = sorted(set(modes))
    return unique_modes[0] if len(unique_modes) == 1 else "mixed"


def compose_answer(
    question: str,
    evidence: list[dict],
    *,
    provider: AnswerProvider | None = None,
) -> AnswerResult:
    citations = [item["citation"] for item in evidence if item.get("citation")]
    data_mode = _resolve_data_mode(evidence)
    is_official = bool(evidence) and all(item.get("is_official") is True for item in evidence)

    if not evidence:
        fallback_provider = ExtractiveFallbackAnswerProvider()
        provider_result = fallback_provider.generate(question, evidence)
        return AnswerResult(
            answer=provider_result.answer,
            status="insufficient_evidence",
            provider=provider_result.provider,
            fallback=provider_result.fallback,
            citations=[],
            data_mode="unknown",
            is_official=False,
        )

    resolved_provider = provider or ExtractiveFallbackAnswerProvider()
    provider_result = resolved_provider.generate(question, evidence)
    answer = provider_result.answer
    if data_mode == "sample" and "sample/local data" not in answer:
        answer = f"Based on sample/local data, {answer}"
    return AnswerResult(
        answer=answer,
        status="answered",
        provider=provider_result.provider,
        fallback=provider_result.fallback,
        citations=citations,
        data_mode=data_mode,
        is_official=is_official,
    )
