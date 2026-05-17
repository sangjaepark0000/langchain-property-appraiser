from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class QueryRewriteResult:
    original_query: str
    rewritten_query: str | None
    status: str
    fallback: bool
    attempts: int = 0


class QueryRewriteProvider(Protocol):
    name: str

    def rewrite(self, query: str, history: list[str]) -> QueryRewriteResult:
        ...


class DeterministicRewriteProvider:
    name = "deterministic-rewrite-fallback"

    def rewrite(self, query: str, history: list[str]) -> QueryRewriteResult:
        context = " ".join(item.strip() for item in history if item.strip())
        if not context:
            return QueryRewriteResult(original_query=query, rewritten_query=None, status="skipped", fallback=True, attempts=1)
        rewritten = f"{query} Context: {context}"
        return QueryRewriteResult(original_query=query, rewritten_query=rewritten, status="rewritten", fallback=True, attempts=1)


def rewrite_query(
    query: str,
    *,
    history: list[str] | None = None,
    provider: QueryRewriteProvider | None = None,
) -> QueryRewriteResult:
    resolved_provider = provider or DeterministicRewriteProvider()
    return resolved_provider.rewrite(query, history or [])
