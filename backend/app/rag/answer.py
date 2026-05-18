from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from app.core.config import Settings, get_settings
from app.rag.safety import apply_response_safety_policy


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


class OpenAIAnswerProvider:
    name = "openai"

    def __init__(self, *, api_key: str, model: str, client: Any | None = None) -> None:
        self.model = model
        if client is not None:
            self.client = client
            return
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:  # pragma: no cover - dependency packaging guard
            raise RuntimeError("langchain-openai package is required for LLM_PROVIDER=openai") from exc
        self.client = ChatOpenAI(model=model, api_key=api_key, temperature=0)

    def generate(self, question: str, evidence: list[dict]) -> AnswerProviderResult:
        prompt = _build_grounded_answer_prompt(question, evidence)
        messages = [
            (
                "system",
                "You answer Korean appraisal-law RAG questions using only the provided evidence. "
                "Do not fabricate law articles, dates, source URLs, legal conclusions, or appraisal determinations. "
                "If evidence is insufficient, say so. Always keep a reference-aid/legal-advice disclaimer.",
            ),
            ("user", prompt),
        ]
        response = self.client.invoke(messages)
        answer = getattr(response, "content", None) or "근거 기반 답변을 생성하지 못했습니다."
        if isinstance(answer, list):
            answer = "".join(str(part) for part in answer)
        return AnswerProviderResult(answer=str(answer).strip(), provider=f"langchain-openai:{self.model}", fallback=False)


def get_answer_provider(settings: Settings | None = None) -> AnswerProvider:
    resolved = settings or get_settings()
    provider_name = resolved.llm_provider.lower()
    if provider_name in {"", "none", "extractive", "fallback", "local"}:
        return ExtractiveFallbackAnswerProvider()
    if provider_name == "openai" and resolved.llm_api_key:
        return OpenAIAnswerProvider(api_key=resolved.llm_api_key, model=resolved.llm_model)
    return ExtractiveFallbackAnswerProvider()


def _build_grounded_answer_prompt(question: str, evidence: list[dict]) -> str:
    evidence_blocks: list[str] = []
    for index, item in enumerate(evidence, start=1):
        citation = item.get("citation") or {}
        metadata = item.get("metadata") or {}
        evidence_blocks.append(
            "\n".join(
                [
                    f"[근거 {index}]",
                    f"법령명: {citation.get('law_name') or citation.get('source_name') or 'unknown'}",
                    f"조문: {citation.get('article_number') or metadata.get('article_number') or 'unknown'} {citation.get('article_title') or ''}".strip(),
                    f"시행일: {citation.get('effective_date') or 'unknown'}",
                    f"개정일: {citation.get('revision_date') or 'unknown'}",
                    f"출처기관: {citation.get('source_authority') or 'unknown'}",
                    f"문서종류: {citation.get('document_kind') or metadata.get('document_kind') or 'unknown'}",
                    "본문:",
                    item.get("text", ""),
                ]
            )
        )
    return (
        "질문에 대해 아래 근거만 사용해 한국어로 답변하세요.\n"
        "규칙:\n"
        "1. 근거에 없는 내용은 추정하지 말고 '제공된 근거만으로는 확인할 수 없습니다'라고 말하세요.\n"
        "2. 법률 자문, 위법 판단, 감정평가 적정성 최종 판단을 하지 마세요.\n"
        "3. 답변에는 관련 법령명과 조문번호를 명시하세요.\n\n"
        f"질문: {question}\n\n"
        + "\n\n".join(evidence_blocks)
    )


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
        safe_answer = apply_response_safety_policy(question, provider_result.answer, evidence)
        return AnswerResult(
            answer=safe_answer,
            status="insufficient_evidence",
            provider=provider_result.provider,
            fallback=provider_result.fallback,
            citations=[],
            data_mode="unknown",
            is_official=False,
        )

    resolved_provider = provider or get_answer_provider()
    provider_result = resolved_provider.generate(question, evidence)
    answer = provider_result.answer
    if data_mode == "sample" and "sample/local data" not in answer:
        answer = f"Based on sample/local data, {answer}"
    answer = apply_response_safety_policy(question, answer, evidence)
    return AnswerResult(
        answer=answer,
        status="answered",
        provider=provider_result.provider,
        fallback=provider_result.fallback,
        citations=citations,
        data_mode=data_mode,
        is_official=is_official,
    )
