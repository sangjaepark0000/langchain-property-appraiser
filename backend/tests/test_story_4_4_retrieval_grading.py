from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.conversation import Conversation  # noqa: F401
from app.models.message import Message  # noqa: F401
from app.models.retrieval_trace import RetrievalTrace
from app.rag.retriever import RetrievalResult


def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def seed_chunk(session, *, embedding=None):
    doc = Document(
        source_id="alpha",
        source_path="sample_data/alpha.md",
        source_name="alpha.md",
        source_type="markdown",
        data_mode="sample",
        ingestion_status="ingested",
        metadata_={},
    )
    session.add(doc)
    session.flush()
    chunk = Chunk(
        document_id=doc.id,
        chunk_index=0,
        text="Fictional Parcel Alpha has a blue roof.",
        metadata_={"embedding": embedding or [1.0, 0.0], "data_mode": "sample"},
        source_lineage={"chunk_index": 0},
        embedding=embedding or [1.0, 0.0],
    )
    session.add(chunk)
    session.commit()
    return chunk


def test_grade_retrieval_results_classifies_sufficient_weak_irrelevant():
    from app.rag.grading import grade_retrieval_results

    assert grade_retrieval_results([RetrievalResult(1, 1, "x", 0.85, "high")]).status == "sufficient"
    assert grade_retrieval_results([RetrievalResult(1, 1, "x", 0.45, "medium")]).status == "weak"
    assert grade_retrieval_results([]).status == "irrelevant"
    assert grade_retrieval_results([RetrievalResult(1, 1, "x", 0.1, "low")]).status == "irrelevant"


def test_answer_question_records_retrieval_trace_with_grading():
    from app.rag.query import answer_question

    session = make_session()
    chunk = seed_chunk(session)

    result = answer_question(session, "alpha", query_vector=[1.0, 0.0])

    trace = session.query(RetrievalTrace).one()
    assert result.grading.status == "sufficient"
    assert trace.relevance_result == "sufficient"
    assert trace.retrieved_chunk_ids == [chunk.id]
    assert trace.summary["max_score"] == 1.0
    session.close()


def test_graph_continues_to_answer_when_grading_is_sufficient():
    from app.graph.conversation import run_conversation_graph

    session = make_session()
    seed_chunk(session)

    result = run_conversation_graph(session, question="alpha", query_vector=[1.0, 0.0])

    assert result.answer.status == "answered"
    assert result.grading.status == "sufficient"
    assert result.answer.citations
    session.close()


def test_graph_returns_insufficient_evidence_when_grading_is_irrelevant_without_server_error():
    from app.graph.conversation import run_conversation_graph

    session = make_session()
    seed_chunk(session, embedding=[1.0, 0.0])

    result = run_conversation_graph(session, question="unrelated", query_vector=[0.0, 1.0], min_retrieval_score=0.0)

    assert result.answer.status == "insufficient_evidence"
    assert result.grading.status == "irrelevant"
    assert result.answer.citations == []
    trace = session.query(RetrievalTrace).order_by(RetrievalTrace.id.desc()).first()
    assert trace.relevance_result == "irrelevant"
    session.close()
