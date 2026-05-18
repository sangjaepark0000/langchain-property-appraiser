from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document


ROOT = Path(__file__).resolve().parents[2]
MIGRATION = ROOT / "backend" / "alembic" / "versions" / "20260517_0003_chunk_embedding_pgvector.py"
RESIZE_MIGRATION = ROOT / "backend" / "alembic" / "versions" / "20260518_0007_chunk_embedding_1536_dimensions.py"


def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_chunk_model_has_embedding_vector_column_with_sqlite_fallback():
    session = make_session()
    doc = Document(
        source_id="alpha",
        source_path="sample_data/alpha.md",
        source_name="alpha.md",
        source_type="markdown",
        data_mode="sample",
        ingestion_status="loaded",
        metadata_={},
    )
    session.add(doc)
    session.flush()
    chunk = Chunk(
        document_id=doc.id,
        chunk_index=0,
        text="alpha",
        metadata_={},
        source_lineage={},
        embedding=[1.0, 0.0],
    )
    session.add(chunk)
    session.commit()

    loaded = session.query(Chunk).one()
    assert loaded.embedding == [1.0, 0.0]
    session.close()


def test_ingestion_persists_embedding_to_metadata_and_vector_column(tmp_path):
    from app.services.ingest_service import ingest_paths

    session = make_session()
    source = tmp_path / "alpha.md"
    source.write_text("Fictional Parcel Alpha has a blue roof.", encoding="utf-8")

    ingest_paths([source], persist=True, session=session)

    chunk = session.query(Chunk).one()
    assert chunk.embedding == chunk.metadata_["embedding"]
    assert len(chunk.embedding) == 1536
    session.close()


def test_retriever_uses_vector_column_when_available_before_metadata_fallback():
    from app.rag.retriever import VectorRetriever

    session = make_session()
    doc = Document(
        source_id="alpha",
        source_path="sample_data/alpha.md",
        source_name="alpha.md",
        source_type="markdown",
        data_mode="sample",
        ingestion_status="loaded",
        metadata_={},
    )
    session.add(doc)
    session.flush()
    session.add(
        Chunk(
            document_id=doc.id,
            chunk_index=0,
            text="alpha vector wins",
            metadata_={"embedding": [0.0, 1.0]},
            source_lineage={},
            embedding=[1.0, 0.0],
        )
    )
    session.commit()

    result = VectorRetriever(session).search("alpha", query_vector=[1.0, 0.0])[0]

    assert result.text == "alpha vector wins"
    assert result.score == 1.0
    session.close()


def test_pgvector_migration_declares_extension_column_and_index():
    text = MIGRATION.read_text(encoding="utf-8")

    assert "CREATE EXTENSION IF NOT EXISTS vector" in text
    assert "embedding vector(16)" in text
    assert "hnsw" in text.lower()
    assert "vector_cosine_ops" in text


def test_pgvector_resize_migration_updates_embedding_dimension_for_openai_small():
    text = RESIZE_MIGRATION.read_text(encoding="utf-8")

    assert "DROP COLUMN IF EXISTS embedding" in text
    assert "embedding vector(1536)" in text
    assert "embedding vector(16)" in text
    assert "ix_chunks_embedding_hnsw" in text


def test_embedding_dimension_setting_defaults_to_openai_small_size():
    from app.core.config import Settings

    assert Settings().embedding_dimensions == 1536
