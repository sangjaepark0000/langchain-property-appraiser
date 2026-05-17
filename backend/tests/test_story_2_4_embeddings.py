def test_fake_embedding_provider_is_deterministic():
    from app.rag.embeddings import FakeEmbeddingProvider

    provider = FakeEmbeddingProvider(dimensions=8)

    assert provider.embed_text("same").vector == provider.embed_text("same").vector
    assert len(provider.embed_text("same").vector) == 8
    assert provider.embed_text("same").status == "success"
    assert provider.embed_text("same").provider == "fake"


def test_embedding_factory_uses_fake_fallback_without_key(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "openai")
    monkeypatch.delenv("EMBEDDING_API_KEY", raising=False)

    from app.core.config import Settings
    from app.rag.embeddings import FakeEmbeddingProvider, get_embedding_provider

    provider = get_embedding_provider(Settings())

    assert isinstance(provider, FakeEmbeddingProvider)
    result = provider.embed_text("hello")
    assert result.status == "success"
    assert result.fallback is True


def test_embedding_failure_result_captures_reason():
    from app.rag.embeddings import EmbeddingResult

    result = EmbeddingResult(provider="test", vector=[], status="failed", error="boom")

    assert result.status == "failed"
    assert result.error == "boom"


def test_embedding_chunks_tracks_partial_failures():
    from app.rag.embeddings import EmbeddingResult, EmbeddingProvider, embed_texts

    class SometimesFails(EmbeddingProvider):
        name = "sometimes-fails"

        def embed_text(self, text: str) -> EmbeddingResult:
            if text == "bad":
                return EmbeddingResult(provider=self.name, vector=[], status="failed", error="bad input")
            return EmbeddingResult(provider=self.name, vector=[1.0], status="success")

    results = embed_texts(["ok", "bad"], SometimesFails())

    assert [result.status for result in results] == ["success", "failed"]
    assert results[1].error == "bad input"
