from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from app.core.config import Settings, get_settings
from app.rag.safety import apply_response_safety_policy

try:  # pragma: no cover - import guard for environments without langsmith extras
    from langsmith import traceable
except Exception:  # pragma: no cover
    def traceable(*args, **kwargs):  # type: ignore[no-redef]
        def decorator(func):
            return func
        return decorator


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
                answer="사용 가능한 근거가 부족합니다.",
                provider=self.name,
                fallback=True,
            )
        data_modes = {item.get("data_mode", "unknown") for item in evidence}
        prefix = "샘플/로컬 데이터 기준으로, " if "sample" in data_modes else "검색된 근거 기준으로, "
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

    @traceable(name="generate_openai_grounded_answer", run_type="llm")
    def generate(self, question: str, evidence: list[dict]) -> AnswerProviderResult:
        prompt = _build_grounded_answer_prompt(question, evidence)
        messages = [
            (
                "system",
                "You are a Korean appraisal-document review assistant. "
                "Your job is not to dump retrieved text, but to synthesize practical review points from evidence. "
                "Use only the provided evidence. Do not fabricate law articles, dates, source URLs, legal conclusions, or appraisal determinations. "
                "If evidence is insufficient, say so. Always keep a reference-aid/legal-advice disclaimer.",
            ),
            ("user", prompt),
        ]
        response = self.client.invoke(messages, config={"run_name": "appraisal_law_answer"})
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
        "당신은 감정평가 서류 검토 도우미입니다. 질문에 대해 아래 근거만 사용해 한국어로 답변하세요.\n"
        "목표:\n"
        "- 검색된 문장을 그대로 나열하지 말고, 사용자가 서류에서 무엇을 확인해야 하는지 '말이 되는 검토 의견'으로 종합하세요.\n"
        "- 법령 근거가 있으면 조문을 근거로 확인 포인트를 연결하세요.\n"
        "- 샘플/사용자 문서 근거와 공식 법령 근거가 함께 있으면 두 출처의 역할을 구분하세요.\n\n"
        "답변 형식:\n"
        "1. 결론: 질문에 대한 짧은 답을 먼저 제시하세요.\n"
        "2. 확인 포인트: 서류에서 점검할 항목을 3~6개 bullet로 정리하세요.\n"
        "3. 근거: 각 포인트 옆에 가능한 경우 법령명과 조문번호를 붙이세요.\n"
        "4. 한계/주의: 근거로 확인할 수 없는 부분과 참고용 답변이라는 점을 짧게 적으세요.\n\n"
        "엄격한 규칙:\n"
        "- 근거에 없는 내용은 추정하지 말고 '제공된 근거만으로는 확인할 수 없습니다'라고 말하세요.\n"
        "- 법률 자문, 위법 판단, 감정평가 적정성 최종 판단을 하지 마세요.\n"
        "- 관련 없는 근거가 섞여 있으면 억지로 사용하지 말고 제외하거나 한계로 설명하세요.\n"
        "- 근거 원문을 길게 복붙하지 마세요.\n\n"
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
    if data_mode == "sample" and "샘플" not in answer:
        answer = f"샘플/로컬 데이터 기준으로, {answer}"
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
