from pathlib import Path
import subprocess
import sys

from sqlalchemy import inspect


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_document_and_chunk_models_are_registered_with_metadata():
    from app.db.base import Base
    from app.models.chunk import Chunk
    from app.models.document import Document

    assert Document.__tablename__ == "documents"
    assert Chunk.__tablename__ == "chunks"
    assert "documents" in Base.metadata.tables
    assert "chunks" in Base.metadata.tables


def test_document_model_has_required_columns_and_constraints():
    from app.models.document import Document

    columns = {column.name for column in Document.__table__.columns}
    attrs = set(Document.__mapper__.attrs.keys())
    for expected in [
        "id",
        "source_id",
        "source_path",
        "source_name",
        "source_type",
        "data_mode",
        "ingestion_status",
        "created_at",
    ]:
        assert expected in columns
    assert "metadata" in columns
    assert "metadata_" in attrs


def test_chunk_model_has_required_columns_relationship_and_fk():
    from app.models.chunk import Chunk

    columns = {column.name for column in Chunk.__table__.columns}
    attrs = set(Chunk.__mapper__.attrs.keys())
    for expected in [
        "id",
        "document_id",
        "chunk_index",
        "text",
        "source_lineage",
        "char_start",
        "char_end",
        "created_at",
    ]:
        assert expected in columns
    assert "metadata" in columns
    assert "metadata_" in attrs

    foreign_keys = {fk.column.table.name for fk in Chunk.__table__.foreign_keys}
    assert "documents" in foreign_keys


def test_alembic_migration_creates_documents_and_chunks_tables():
    versions_text = "\n".join(path.read_text() for path in (BACKEND_ROOT / "alembic" / "versions").glob("*.py"))

    assert '"documents"' in versions_text
    assert '"chunks"' in versions_text
    assert "ForeignKeyConstraint" in versions_text
    assert "data_mode" in versions_text
    assert "ingestion_status" in versions_text


def test_metadata_can_create_model_tables_in_sqlite_for_shape_validation():
    from sqlalchemy import create_engine

    from app.db.base import Base
    import app.models.chunk  # noqa: F401
    import app.models.document  # noqa: F401

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    inspector = inspect(engine)

    assert "documents" in inspector.get_table_names()
    assert "chunks" in inspector.get_table_names()


def test_alembic_upgrade_head_against_unavailable_db_still_fails_clearly():
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(BACKEND_ROOT / "alembic.ini"), "upgrade", "head"],
        cwd=BACKEND_ROOT,
        env={"DATABASE_URL": "postgresql+psycopg://app:app@127.0.0.1:1/langchain_property_appraiser"},
        text=True,
        capture_output=True,
        timeout=10,
    )

    assert result.returncode != 0
    assert "connection" in (result.stdout + result.stderr).lower() or "connect" in (result.stdout + result.stderr).lower()
