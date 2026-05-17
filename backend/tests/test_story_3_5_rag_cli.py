from pathlib import Path
import subprocess
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_ingestion_persistence_stores_embedding_in_chunk_metadata(tmp_path):
    from app.services.ingest_service import ingest_paths

    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    source = tmp_path / "alpha.md"
    source.write_text("Fictional Parcel Alpha has a blue roof.", encoding="utf-8")

    ingest_paths([source], persist=True, session=session)

    chunk = session.query(Chunk).one()
    assert "embedding" in chunk.metadata_
    assert isinstance(chunk.metadata_["embedding"], list)
    session.close()


def test_rag_query_service_returns_answer_and_citations():
    from app.rag.query import answer_question

    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    doc = Document(
        source_id="alpha",
        source_path="sample_data/sample-property-alpha.md",
        source_name="sample-property-alpha.md",
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
            text="Fictional Parcel Alpha has a blue roof.",
            metadata_={"embedding": [1.0, 0.0], "data_mode": "sample"},
            source_lineage={"chunk_index": 0},
        )
    )
    session.commit()

    result = answer_question(session, "alpha", query_vector=[1.0, 0.0])

    assert result.answer.status == "answered"
    assert "blue roof" in result.answer.answer
    assert result.retrieved_count == 1
    assert result.answer.citations


def test_rag_cli_outputs_answer_citations_and_debug(tmp_path):
    db_path = tmp_path / "rag.db"
    source = tmp_path / "alpha.md"
    source.write_text("Fictional Parcel Alpha has a blue roof.", encoding="utf-8")

    env = {"DATABASE_URL": f"sqlite+pysqlite:///{db_path}"}
    ingest = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "ingest_file.py"), str(source)],
        cwd=BACKEND_ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=20,
    )
    assert ingest.returncode == 0, ingest.stderr

    query = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "rag_query.py"), "Fictional Parcel Alpha", "--debug"],
        cwd=BACKEND_ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=20,
    )

    assert query.returncode == 0
    assert "answer=" in query.stdout
    assert "citations=" in query.stdout
    assert "retrieved_count=" in query.stdout
    assert "fallback=" in query.stdout
    assert "secret" not in query.stdout.lower()


def test_rag_cli_returns_insufficient_evidence_when_no_results(tmp_path):
    db_path = tmp_path / "empty.db"
    env = {"DATABASE_URL": f"sqlite+pysqlite:///{db_path}"}

    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "rag_query.py"), "unknown question"],
        cwd=BACKEND_ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=20,
    )

    assert result.returncode == 0
    assert "insufficient" in result.stdout.lower()
