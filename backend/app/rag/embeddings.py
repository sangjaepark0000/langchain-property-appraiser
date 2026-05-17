from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Protocol

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EmbeddingResult:
    provider: str
    vector: list[float]
    status: str
    error: str | None = None
    fallback: bool = False


class EmbeddingProvider(Protocol):
    name: str

    def embed_text(self, text: str) -> EmbeddingResult:
        ...


class FakeEmbeddingProvider:
    name = "fake"

    def __init__(self, dimensions: int = 16, *, fallback: bool = True) -> None:
        self.dimensions = dimensions
        self.fallback = fallback

    def embed_text(self, text: str) -> EmbeddingResult:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values: list[float] = []
        for i in range(self.dimensions):
            byte = digest[i % len(digest)]
            values.append(round((byte / 255.0) * 2.0 - 1.0, 6))
        return EmbeddingResult(provider=self.name, vector=values, status="success", fallback=self.fallback)


class MissingProviderEmbeddingProvider:
    name = "missing-provider"

    def __init__(self, provider_name: str) -> None:
        self.provider_name = provider_name

    def embed_text(self, text: str) -> EmbeddingResult:
        return EmbeddingResult(
            provider=self.provider_name,
            vector=[],
            status="skipped",
            error=f"Embedding provider '{self.provider_name}' is not configured in local mode.",
        )


def get_embedding_provider(settings: Settings | None = None) -> EmbeddingProvider:
    resolved = settings or get_settings()
    provider_name = resolved.embedding_provider.lower()
    if provider_name in {"none", "fake", "mock", "local"}:
        return FakeEmbeddingProvider(fallback=provider_name != "fake")
    if not resolved.embedding_api_key:
        logger.info("Embedding provider %s requested without key; using deterministic fake fallback", provider_name)
        return FakeEmbeddingProvider(fallback=True)
    return MissingProviderEmbeddingProvider(provider_name)


def embed_texts(texts: list[str], provider: EmbeddingProvider | None = None) -> list[EmbeddingResult]:
    resolved_provider = provider or get_embedding_provider()
    results: list[EmbeddingResult] = []
    for text in texts:
        try:
            results.append(resolved_provider.embed_text(text))
        except Exception as exc:  # pragma: no cover - defensive boundary for provider plugins
            logger.exception("Embedding generation failed")
            results.append(
                EmbeddingResult(
                    provider=resolved_provider.name,
                    vector=[],
                    status="failed",
                    error=str(exc),
                )
            )
    return results
