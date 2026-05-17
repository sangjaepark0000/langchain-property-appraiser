"""allow ingested document status

Revision ID: 20260517_0005
Revises: 20260517_0004
Create Date: 2026-05-17
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260517_0005"
down_revision: str | None = "20260517_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

NEW_VALUES = "'loaded', 'ingested', 'skipped', 'unsupported', 'failed'"
OLD_VALUES = "'loaded', 'skipped', 'unsupported', 'failed'"


def upgrade() -> None:
    op.execute("ALTER TABLE documents DROP CONSTRAINT IF EXISTS ck_documents_ingestion_status")
    op.execute(
        f"ALTER TABLE documents ADD CONSTRAINT ck_documents_ingestion_status "
        f"CHECK (ingestion_status IN ({NEW_VALUES}))"
    )


def downgrade() -> None:
    op.execute("UPDATE documents SET ingestion_status = 'loaded' WHERE ingestion_status = 'ingested'")
    op.execute("ALTER TABLE documents DROP CONSTRAINT IF EXISTS ck_documents_ingestion_status")
    op.execute(
        f"ALTER TABLE documents ADD CONSTRAINT ck_documents_ingestion_status "
        f"CHECK (ingestion_status IN ({OLD_VALUES}))"
    )
