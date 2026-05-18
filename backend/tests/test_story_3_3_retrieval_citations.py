import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document
from app.rag.retriever import RetrievalResult


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


def add_retrieval_fixture(session, *, metadata=None, source_lineage=None, data_mode="sample"):
    doc = Document(
        source_id="alpha",
        source_path="sample_data/sample-property-alpha.md",
        source_name="sample-property-alpha.md",
        source_type="markdown",
        data_mode=data_mode,
        ingestion_status="loaded",
        metadata_=metadata or {},
    )
    session.add(doc)
    session.flush()
    chunk = Chunk(
        document_id=doc.id,
        chunk_index=3,
        text="Fictional Parcel Alpha has a blue roof.",
        metadata_=metadata or {},
        source_lineage=source_lineage or {"source_id": "alpha", "chunk_index": 3},
        char_start=10,
        char_end=50,
    )
    session.add(chunk)
    session.commit()
    return doc, chunk


def test_hydrated_retrieval_result_contains_citation_fields(db_session):
    from app.rag.citations import hydrate_retrieval_results

    doc, chunk = add_retrieval_fixture(db_session)
    raw = RetrievalResult(chunk_id=chunk.id, document_id=doc.id, text=chunk.text, score=0.9, relevance="high")

    hydrated = hydrate_retrieval_results(db_session, [raw])[0]

    assert hydrated["chunk_id"] == chunk.id
    assert hydrated["document_id"] == doc.id
    assert hydrated["chunk_index"] == 3
    assert hydrated["source_path"] == "sample_data/sample-property-alpha.md"
    assert hydrated["source_name"] == "sample-property-alpha.md"
    assert hydrated["data_mode"] == "sample"
    assert hydrated["citation"]["source_path"] == "sample_data/sample-property-alpha.md"
    assert hydrated["citation"]["chunk_index"] == 3


def test_missing_metadata_uses_unknown_without_fabricating_official_url(db_session):
    from app.rag.citations import hydrate_retrieval_results

    doc, chunk = add_retrieval_fixture(db_session, metadata={}, source_lineage={})
    doc.source_path = None
    doc.source_name = ""
    db_session.commit()
    raw = RetrievalResult(chunk_id=chunk.id, document_id=doc.id, text=chunk.text, score=0.5, relevance="medium")

    hydrated = hydrate_retrieval_results(db_session, [raw])[0]

    assert hydrated["source_path"] == "unknown"
    assert hydrated["source_name"] == "unknown"
    assert hydrated["source_url"] == "unknown"
    assert "law.go.kr" not in str(hydrated)
    assert "molit.go.kr" not in str(hydrated)


def test_sample_result_is_explicitly_marked_not_official(db_session):
    from app.rag.citations import hydrate_retrieval_results

    doc, chunk = add_retrieval_fixture(db_session, data_mode="sample")
    raw = RetrievalResult(chunk_id=chunk.id, document_id=doc.id, text=chunk.text, score=0.9, relevance="high")

    hydrated = hydrate_retrieval_results(db_session, [raw])[0]

    assert hydrated["data_mode"] == "sample"
    assert hydrated["is_official"] is False
    assert hydrated["citation"]["data_mode"] == "sample"


def test_official_law_citation_includes_legal_metadata(db_session):
    from app.rag.citations import hydrate_retrieval_results

    metadata = {
        "source_name": "감정평가 및 감정평가사에 관한 법률 시행규칙",
        "source_authority": "국가법령정보센터",
        "corpus_group": "appraisal_act_framework",
        "law_level": "enforcement_rule",
        "document_kind": "current_consolidated_rule",
        "chunk_type": "article",
        "article_number": "제27조",
        "article_title": None,
        "change_type": "deleted",
        "revision_marker": "2026. 3. 12.",
        "domain_metadata": {
            "law_name": "감정평가 및 감정평가사에 관한 법률 시행규칙",
            "article_number": "제27조",
            "article_title": None,
            "effective_date": "2026-03-12",
            "revision_date": "2026-03-12",
            "source_authority": "국가법령정보센터",
        },
    }
    doc, chunk = add_retrieval_fixture(db_session, metadata=metadata, data_mode="official")
    raw = RetrievalResult(chunk_id=chunk.id, document_id=doc.id, text=chunk.text, score=0.9, relevance="high")

    citation = hydrate_retrieval_results(db_session, [raw])[0]["citation"]

    assert citation["law_name"] == "감정평가 및 감정평가사에 관한 법률 시행규칙"
    assert citation["article_number"] == "제27조"
    assert citation["effective_date"] == "2026-03-12"
    assert citation["revision_date"] == "2026-03-12"
    assert citation["source_authority"] == "국가법령정보센터"
    assert citation["document_kind"] == "current_consolidated_rule"
    assert citation["change_type"] == "deleted"
    assert citation["revision_marker"] == "2026. 3. 12."


def test_missing_chunk_result_is_skipped(db_session):
    from app.rag.citations import hydrate_retrieval_results

    raw = RetrievalResult(chunk_id=9999, document_id=9999, text="missing", score=0.1, relevance="low")

    assert hydrate_retrieval_results(db_session, [raw]) == []
