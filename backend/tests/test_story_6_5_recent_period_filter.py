from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document
from app.rag.recent_filter import RecentPeriodFilter, apply_recent_period_filter, parse_recent_period_filter
from app.rag.retriever import RetrievalResult, VectorRetriever


def test_parse_recent_period_filter_from_korean_natural_language():
    parsed = parse_recent_period_filter("최근 1년 안에 개정된 고시 알려줘", today=date(2026, 5, 17))

    assert parsed is not None
    assert parsed.amount == 1
    assert parsed.unit == "year"
    assert parsed.since == date(2025, 5, 17)
    assert parsed.preferred_date_fields == ("revision_date", "effective_date")
    assert parsed.status == "parsed"


def test_parse_recent_period_filter_marks_uncertain_expression():
    parsed = parse_recent_period_filter("최근 변경사항 알려줘", today=date(2026, 5, 17))

    assert parsed is not None
    assert parsed.status == "needs_clarification"
    assert parsed.limitation_reason


def test_apply_recent_period_filter_keeps_results_by_revision_or_effective_date_and_reports_field():
    engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    new_doc = _doc(session, "new", "official", "2026-01-10", None)
    old_doc = _doc(session, "old", "official", "2024-01-10", None)
    missing_doc = _doc(session, "missing", "official", None, None)
    session.flush()
    new_chunk = _chunk(session, new_doc.id, [1.0, 0.0])
    old_chunk = _chunk(session, old_doc.id, [0.9, 0.0])
    missing_chunk = _chunk(session, missing_doc.id, [0.8, 0.0])
    session.commit()
    results = [
        RetrievalResult(new_chunk.id, new_doc.id, "new", 1.0, "high"),
        RetrievalResult(old_chunk.id, old_doc.id, "old", 0.9, "high"),
        RetrievalResult(missing_chunk.id, missing_doc.id, "missing", 0.8, "high"),
    ]

    filtered = apply_recent_period_filter(session, results, RecentPeriodFilter(amount=1, unit="year", since=date(2025, 5, 17)))

    assert [result.chunk_id for result in filtered.results] == [new_chunk.id]
    assert filtered.applied is True
    assert filtered.date_field_used == "revision_date"
    assert old_chunk.id in filtered.excluded_chunk_ids
    assert missing_chunk.id in filtered.missing_date_chunk_ids
    assert "missing date metadata" in filtered.limitation_reason


def test_retriever_accepts_recent_period_filter_as_post_filter():
    engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    new_doc = _doc(session, "new", "official", "2026-01-10", None)
    old_doc = _doc(session, "old", "official", "2024-01-10", None)
    session.flush()
    _chunk(session, new_doc.id, [1.0, 0.0])
    _chunk(session, old_doc.id, [1.0, 0.0])
    session.commit()

    results = VectorRetriever(session).search(
        "recent official",
        query_vector=[1.0, 0.0],
        recent_filter=RecentPeriodFilter(amount=1, unit="year", since=date(2025, 5, 17)),
    )

    assert len(results) == 1
    assert results[0].document_id == new_doc.id


def _doc(session, source_id: str, data_mode: str, revision_date: str | None, effective_date: str | None):
    domain_metadata = {
        "source_title": source_id,
        "revision_date": revision_date,
        "effective_date": effective_date,
        "source_url": "unknown",
        "source_authority": "unknown",
    }
    doc = Document(
        source_id=source_id,
        source_path=None,
        source_name=source_id,
        source_type="official_law_xml",
        data_mode=data_mode,
        ingestion_status="ingested",
        metadata_={"domain_metadata": domain_metadata},
    )
    session.add(doc)
    return doc


def _chunk(session, document_id: int, embedding: list[float]):
    chunk = Chunk(
        document_id=document_id,
        chunk_index=0,
        text="official text",
        metadata_={"embedding": embedding},
        source_lineage={"source_id": "official-law-open-api"},
        embedding=embedding,
    )
    session.add(chunk)
    session.flush()
    return chunk
