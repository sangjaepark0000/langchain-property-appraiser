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


def test_openai_embedding_provider_uses_configured_model_dimensions_without_live_api():
    from app.rag.embeddings import OpenAIEmbeddingProvider

    class FakeEmbeddings:
        def __init__(self) -> None:
            self.kwargs = None

        def create(self, **kwargs):
            self.kwargs = kwargs

            class Item:
                embedding = [0.1, 0.2, 0.3]

            class Response:
                data = [Item()]

            return Response()

    class FakeClient:
        def __init__(self) -> None:
            self.embeddings = FakeEmbeddings()

    client = FakeClient()
    provider = OpenAIEmbeddingProvider(api_key="test-key", model="text-embedding-3-small", dimensions=1536, client=client)

    result = provider.embed_text("hello")

    assert result.provider == "langchain-openai:text-embedding-3-small"
    assert result.vector == [0.1, 0.2, 0.3]
    assert result.status == "success"
    assert result.fallback is False
    assert client.embeddings.kwargs == {
        "model": "text-embedding-3-small",
        "input": "hello",
        "dimensions": 1536,
    }


def test_embedding_factory_uses_openai_when_key_is_configured():
    from app.core.config import Settings
    from app.rag.embeddings import OpenAIEmbeddingProvider, get_embedding_provider

    provider = get_embedding_provider(
        Settings(
            EMBEDDING_PROVIDER="openai",
            EMBEDDING_API_KEY="test-key",
            EMBEDDING_MODEL="text-embedding-3-small",
            EMBEDDING_DIMENSIONS=1536,
        )
    )

    assert isinstance(provider, OpenAIEmbeddingProvider)
    assert provider.model == "text-embedding-3-small"
    assert provider.dimensions == 1536


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
