from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.document import INGESTION_STATUS_VALUES


ROOT = Path(__file__).resolve().parents[2]
MIGRATION = ROOT / "backend" / "alembic" / "versions" / "20260517_0005_ingestion_status_ingested.py"


def test_document_ingestion_status_allows_ingested_in_model_and_migration():
    from app.models.document import Document

    assert "ingested" in INGESTION_STATUS_VALUES
    constraint_text = "\n".join(str(constraint.sqltext) for constraint in Document.__table__.constraints if hasattr(constraint, "sqltext"))
    assert "ingested" in constraint_text

    migration_text = MIGRATION.read_text(encoding="utf-8")
    assert "ck_documents_ingestion_status" in migration_text
    assert "'ingested'" in migration_text
    assert "UPDATE documents SET ingestion_status = 'loaded' WHERE ingestion_status = 'ingested'" in migration_text


def test_ingestion_persistence_uses_ingested_status(tmp_path):
    from app.models.document import Document
    from app.services.ingest_service import ingest_paths

    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    source = tmp_path / "sample.md"
    source.write_text("hello", encoding="utf-8")

    ingest_paths([source], persist=True, session=session)

    document = session.query(Document).one()
    assert document.ingestion_status == "ingested"
    session.close()


def test_conversation_messages_relationship_orders_by_created_at_and_id():
    from app.models.conversation import Conversation

    relationship = Conversation.__mapper__.relationships["messages"]
    order_by_text = ", ".join(str(item) for item in relationship.order_by)

    assert "messages.created_at" in order_by_text
    assert "messages.id" in order_by_text
