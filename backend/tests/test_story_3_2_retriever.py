import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document


@pytest.fixture
def db_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


def add_doc_with_chunk(session, text: str, embedding: list[float], *, source_id: str = "sample"):
    doc = Document(
        source_id=source_id,
        source_path=f"sample_data/{source_id}.md",
        source_name=f"{source_id}.md",
        source_type="markdown",
        data_mode="sample",
        ingestion_status="ingested",
        metadata_={"source_id": source_id},
    )
    session.add(doc)
    session.flush()
    chunk = Chunk(
        document_id=doc.id,
        chunk_index=0,
        text=text,
        metadata_={"embedding": embedding, "source_path": doc.source_path, "data_mode": "sample"},
        source_lineage={"source_id": source_id, "chunk_index": 0},
    )
    session.add(chunk)
    session.commit()
    return doc, chunk


def test_retriever_returns_ranked_chunk_candidates(db_session):
    from app.rag.retriever import VectorRetriever

    doc_a, chunk_a = add_doc_with_chunk(db_session, "alpha blue roof", [1.0, 0.0], source_id="alpha")
    add_doc_with_chunk(db_session, "beta north road", [0.0, 1.0], source_id="beta")

    retriever = VectorRetriever(db_session)
    results = retriever.search("alpha", query_vector=[1.0, 0.0], limit=2)

    assert results[0].chunk_id == chunk_a.id
    assert results[0].document_id == doc_a.id
    assert results[0].score > results[1].score
    assert results[0].relevance == "high"


def test_retriever_uses_embedding_provider_when_query_vector_not_supplied(db_session):
    from app.rag.embeddings import EmbeddingResult, EmbeddingProvider
    from app.rag.retriever import VectorRetriever

    class QueryProvider(EmbeddingProvider):
        name = "query-provider"

        def embed_text(self, text: str) -> EmbeddingResult:
            return EmbeddingResult(provider=self.name, vector=[0.0, 1.0], status="success")

    _, chunk = add_doc_with_chunk(db_session, "beta north road", [0.0, 1.0], source_id="beta")

    results = VectorRetriever(db_session, embedding_provider=QueryProvider()).search("road")

    assert results[0].chunk_id == chunk.id
    assert results[0].score == 1.0


def test_retriever_returns_empty_list_when_no_vector_chunks(db_session):
    from app.rag.retriever import VectorRetriever

    doc = Document(
        source_id="no-vector",
        source_path="sample_data/no-vector.md",
        source_name="no-vector.md",
        source_type="markdown",
        data_mode="sample",
        ingestion_status="ingested",
        metadata_={},
    )
    db_session.add(doc)
    db_session.flush()
    db_session.add(
        Chunk(
            document_id=doc.id,
            chunk_index=0,
            text="no vector here",
            metadata_={},
            source_lineage={},
        )
    )
    db_session.commit()

    assert VectorRetriever(db_session).search("anything", query_vector=[1.0, 0.0]) == []


def test_retriever_returns_empty_list_when_query_embedding_fails(db_session):
    from app.rag.embeddings import EmbeddingResult, EmbeddingProvider
    from app.rag.retriever import VectorRetriever

    class FailingProvider(EmbeddingProvider):
        name = "failing"

        def embed_text(self, text: str) -> EmbeddingResult:
            return EmbeddingResult(provider=self.name, vector=[], status="failed", error="nope")

    add_doc_with_chunk(db_session, "alpha blue roof", [1.0, 0.0], source_id="alpha")

    assert VectorRetriever(db_session, embedding_provider=FailingProvider()).search("alpha") == []
