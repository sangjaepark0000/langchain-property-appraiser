"""create documents and chunks

Revision ID: 20260517_0002
Revises: 20260517_0001
Create Date: 2026-05-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260517_0002"
down_revision: str | None = "20260517_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.String(length=255), nullable=False),
        sa.Column("source_path", sa.Text(), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("source_name", sa.String(length=512), nullable=False),
        sa.Column("source_type", sa.String(length=100), nullable=False),
        sa.Column("data_mode", sa.String(length=50), nullable=False),
        sa.Column("ingestion_status", sa.String(length=50), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "data_mode IN ('sample', 'official', 'user_provided', 'unknown')",
            name="ck_documents_data_mode",
        ),
        sa.CheckConstraint(
            "ingestion_status IN ('loaded', 'skipped', 'unsupported', 'failed')",
            name="ck_documents_ingestion_status",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_documents_data_mode"), "documents", ["data_mode"], unique=False)
    op.create_index(op.f("ix_documents_ingestion_status"), "documents", ["ingestion_status"], unique=False)
    op.create_index(op.f("ix_documents_source_id"), "documents", ["source_id"], unique=False)

    op.create_table(
        "chunks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("source_lineage", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("char_start", sa.Integer(), nullable=True),
        sa.Column("char_end", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_chunks_document_id_chunk_index", "chunks", ["document_id", "chunk_index"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_chunks_document_id_chunk_index", table_name="chunks")
    op.drop_table("chunks")
    op.drop_index(op.f("ix_documents_source_id"), table_name="documents")
    op.drop_index(op.f("ix_documents_ingestion_status"), table_name="documents")
    op.drop_index(op.f("ix_documents_data_mode"), table_name="documents")
    op.drop_table("documents")
